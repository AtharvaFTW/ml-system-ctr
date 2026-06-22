
from fastapi import FastAPI
from mlflow import pyfunc

from src.utils.mlflow_helpers import _get_champion_version
app = FastAPI()

champ = _get_champion_version()

@app.get("/")
def home():
    
    if not champ:
        return {"status": "ok", "model": "not loaded"}
        
    return {"status": "ok", "model": "loaded"}
    

def predict():
    model_uri = f"models:/ctr_model/{champ}"
    model = pyfunc.load_model(model_uri)

def model_info():
    pass

def train():
    pass
