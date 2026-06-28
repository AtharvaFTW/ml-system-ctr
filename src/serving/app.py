from psycopg.generators import BAD
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from datetime import datetime, timezone
import requests
import os

from src.serving.schemas import ModelInfoResponse, PredictRequest, PredictResponse
from src.features.feature_pipeline import get_serving_features
from src.serving import model_loader
from src.utils.logger import get_logger

logger = get_logger(__name__)
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_loader.load()
    logger.info("Model loaded")

    yield

    model_loader.unload()
    logger.info("Model unloaded")


app = FastAPI(lifespan = lifespan)


@app.get("/health")
def health():
    if model_loader.get_model() is None:
        return {"status" : "degraded" , "model" : "unavailable"}
    
    return{"status" : "ok" , "model" : "available"}


@app.post("/predict", response_model= PredictResponse)
def predict(request: PredictRequest):
    logger.info("Received a prediction request.")

    try:
        logger.info("Fetching the model from memory...")
        model = model_loader.get_model()

        if model is None:
            detail = "Model not loaded"
            logger.error(detail)
            raise HTTPException(status_code = 503, detail= detail)
        
        logger.info("✔ Model loaded successfully!")
        entity_rows = [{"click_event_id" : request.click_event_id}]
        df = get_serving_features(entity_rows)
        df = df.drop(columns = ["click_event_id"])
        feature_cols = [f"I{i}" for i in range(1,14)] + [f"C{i}" for i in range(1,27)]
        df = df[feature_cols]
        logger.info("Predicting...")
        proba_df = model.predict_proba(df)
        click_proba = float(proba_df[0][1])

        prediction = 1 if click_proba > 0.5 else 0
        logger.info(f"✅ Prediction : {prediction}")

    except Exception as e:
        logger.error(f"❌ Failed to predict : {e}")
        raise

    return PredictResponse(click_probability= click_proba, prediction = prediction)


@app.get("/model/info", response_model = ModelInfoResponse)
def model_info():

    if not model_loader.get_info():
        return {"status": "error"}

    return model_loader.get_info()


@app.post("/train")
def train():
    logger.info("Recieved a model training request.")
    BASE_URL = os.getenv("AIRFLOW_BASE_URL")

   

    try:
        token_response = requests.post(
            f"{BASE_URL}/auth/token",
            json = {"username": os.getenv("AIRFLOW_USERNAME"), "password": os.getenv("AIRFLOW_PASSWORD")}
        )
        token_response.raise_for_status()
        token = token_response.json()["access_token"]

        url = f"{BASE_URL}/api/v2/dags/training_pipeline/dagRuns"
        response = requests.post(
            url,
            headers = {"Authorization" : f"Bearer {token}"},
            json = {"conf": {}, "logical_date": datetime.now(timezone.utc).isoformat()}
        )

        response.raise_for_status()
        data = response.json()

    except Exception as e:
        logger.error(f"❌ training_pipeline DAG failed: {e}")
        raise
    
    logger.info(f"training_pipeline DAG initiated with id : {data["dag_run_id"]}")
    return {"status": "triggered" , "dag_run_id" : data["dag_run_id"]}
