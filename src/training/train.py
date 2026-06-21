from xgboost import XGBClassifier
from sklearn.utils.validation import check_is_fitted
from sklearn.exceptions import NotFittedError
from pathlib import Path
from mlflow.client import MlflowClient
import xgboost as xgb
import pandas as pd
import numpy as np
import mlflow

from src.utils.logger import get_logger

logger = get_logger(__name__)

def load_training_data():
    """
    Load train, val parquet files.
    Split and return the Independent Features (X) and Dependent Features (y).
    
    Returns:
        X_train: The indenpendent features for the train set.
        X_val: The indenpendent features for the val set.
        y_train: The dependent features a.k.a truth labels for the train set.
        y_val: The dependent features for the val set.
    """
    try:
        train_df = pd.read_parquet(Path(r"data/processed/train.parquet"))
        val_df = pd.read_parquet(Path(r"data/processed/val.parquet"))

        logger.info(f" Training data shape: {train_df.shape}")
        logger.info(f" Validation data shape: {val_df.shape}")

        X_train = train_df.drop(columns = ["label", "event_timestamp"], errors = "ignore")
        y_train = train_df["label"]

        X_val = val_df.drop(columns = ["label", "event_timestamp"], errors = "ignore")
        y_val = val_df["label"]

    except Exception as e:
        logger.error(f"❌ Data loading failed: {e}")
        raise

    return X_train, X_val, y_train , y_val


def compute_scale_pos_weight(y_train) -> float:
    """
    Compute scale_pos_weight from class distribution

    Args: 
        y_train: The dependent features a.k.a truth labels for the train set.

    Returns:
        scale_weight: calculated scale_pos_weight.
    """
    try:
        num_neg = (y_train == 0).sum()
        num_pos = (y_train == 1).sum()

        scale_weight = num_neg / num_pos

        logger.info(f"Calculated scale_pos_weight: {scale_weight}")

    except Exception as e:
        logger.error(f"❌ scale_pos_weight calculation failed: {e}")
        raise
    
    return scale_weight


def train_xgboost(X_train: pd.DataFrame, y_train: pd.Series, X_val: pd.DataFrame, y_val: pd.Series, scale_pos_weight: float, hyperparams: dict) -> xgb.XGBClassifier:
    """
    Train XGBoost mdoel with given hyperparams.

    Args:
        X_train: The indenpendent features for the train set.
        X_val: The indenpendent features for the val set.
        y_train: The dependent features a.k.a truth labels for the train set.
        y_val: The dependent features for the val set.
    
    Returns:
        xgb.XGBClassifier: Trained XGB Classifier Model.
    """

    logger.info("Initializing the XGBClassifier...")
    try:
        model = xgb.XGBClassifier(
            n_estimators = hyperparams["N_ESTIMATORS"],
            learning_rate = hyperparams["LEARNING_RATE"],
            scale_pos_weight = scale_pos_weight,
            max_depth = hyperparams["MAX_DEPTH"],
            eval_metric = hyperparams["EVAL_METRICS_LIST"],
            early_stopping_rounds = hyperparams["EARLY_STOPPING"],
            random_state = hyperparams["RANDOM_STATE"],
            tree_method = hyperparams["TREE_METHOD"],
            enable_categorical = hyperparams["ENABLE_CATEGORICAL"]
        )

        logger.info("Training the XGBClassifier...")
        model.fit(
            X_train,
            y_train,
            eval_set = [(X_train, y_train), (X_val, y_val)],
            verbose = True
        )
        
        check_is_fitted(model)
        logger.info(f"✔ Model trained successfully !")

    except NotFittedError as nfe:
        logger.error(f"❌ Model training failed: {nfe}")
        raise

    except Exception as e:
        logger.error(f"❌ Model training failed: {e}")
        raise

    return model

def run_training():
    """Orchestrates full training run with MLFlow tracking"""
    # HYPERPARAMETERS
    hyperparams = {
        "N_ESTIMATORS" : 1000,
        "LEARNING_RATE" : 0.1,
        "MAX_DEPTH" : 6,
        "EVAL_METRICS_LIST" : [ "auc", "aucpr","logloss"],
        "EARLY_STOPPING" : 20,
        "RANDOM_STATE" : 42,
        "TREE_METHOD" : "hist",
        "ENABLE_CATEGORICAL" : False
    }
    
    try:
        logger.info("Firing the training pipeline...")
        with mlflow.start_run() as run:

            run_id = run.info.run_id
            mlflow.log_params(hyperparams)
            X_train, X_val, y_train, y_val = load_training_data()
            calculated_weight = compute_scale_pos_weight(y_train)
            model = train_xgboost(X_train, y_train, X_val, y_val, calculated_weight, hyperparams)
            mlflow.xgboost.log_model(model, "model")

            eval_results = model.evals_result()

            for metric_name, values in eval_results["validation_1"].items():
                mlflow.log_metric(f"val_{metric_name}", values[-1])

            for metric_name, values in eval_results["validation_0"].items():
                mlflow.log_metric(f"train_{metric_name}", values[-1])

            mlflow.log_metric("best_iteration", model.best_iteration)
            mlflow.log_metric("val_auc_best", eval_results["validation_1"]["auc"][model.best_iteration])
            logger.info("✅ Trainig pipleline completed successfully !")

    except Exception as e:
        logger.error(f"❌ Training pipeline failed: {e}")
        raise

    return model , run_id

if __name__ == "__main__":
    run_training()