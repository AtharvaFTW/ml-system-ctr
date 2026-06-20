from codecs import ignore_errors
from sklearn.metrics import roc_auc_score, log_loss, precision_score, recall_score
from pathlib import Path
import pandas as pd
import xgboost as xgb
import mlflow


from src.utils.logger import get_logger

logger = get_logger(__name__)

def load_test_data():
    """
    Load the test data for evaluation of trained model.

    Retruns:
        X_test: The indenpendent features for the test set.
        y_test: The dependent features a.k.a truth labels for the test set.
    """
    try:
        test_data = pd.read_parquet(Path(r"data/processed/test.parquet"))
        logger.info(f"Test Data shape: {test_data.shape}")

        X_test = test_data.drop(columns = ["label", "event_timestamp"], errors = "ignore")
        y_test = test_data["label"]

    except Exception as e:
        logger.error(f"❌ Loading test data failed: {e}")
        raise

    return X_test, y_test

def compute_metrics(model: xgb.XGBClassifier ,X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """
    Compute the metrics for the trained model.

    Args:
        model: trained XGBClassifier on CTR dataset.
        X_test: The indenpendent features for the test set.
        y_test: The dependent features a.k.a truth labels for the test set.
    
    Returns:
        dict: a dictionary of all the computed metrics.
    """
    try:
        logger.info("Computing metrics...")
        y_pred_proba = model.predict_proba(X_test)[:,1] # probability the ad will be clicked
        y_pred = model.predict(X_test)

        auc = roc_auc_score(y_test, y_pred_proba)
        loss = log_loss(y_test, y_pred_proba)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)

        metrics = {
            "auc_score" : auc,
            "log_loss" : loss,
            "precision_score" : precision,
            "recall_score" : recall
            }

        logger.info(f"Computed metrics: {metrics}")
        
    except Exception as e:
        logger.error(f"❌ Metric computation failed: {e}")
        raise

    return metrics

def run_evaluation(model, run_id) -> dict:
    """
    Orchestrates full evaluation run with MLFlow logging.

    Args:
        model: trained XGBClassifier on CTR dataset.
        run_id: mlflow run_id from model training.
    
    Returns:
        dict: computed metrics

    """
    try:
        logger.info("Firing the evaluation pipeline...")
        X_test, y_test = load_test_data()
        metrics = compute_metrics(model, X_test, y_test)

        with mlflow.start_run(run_id = run_id, nested= True):
            mlflow.log_metric("test_auc", metrics["auc_score"])
            mlflow.log_metric("test_loss", metrics["log_loss"])
            mlflow.log_metric("test_precision", metrics["precision_score"])
            mlflow.log_metric("test_recall", metrics["recall_score"])
        
        logger.info("✅ Evaluation pipeline successful !")

    except Exception as e:
        logger.error(f"❌ Evaluation pipeline failed: {e}")
        raise
    
    return metrics