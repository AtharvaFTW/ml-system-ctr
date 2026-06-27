import mlflow.xgboost
from mlflow.client import MlflowClient

from src.utils.mlflow_helpers import _get_champion_version
from src.utils.logger import get_logger

logger = get_logger(__name__)

_model = None
_model_info = {}


def load():
    try:
        logger.info("Loading the model...")
        client = MlflowClient()

        global _model, _model_info

        model_name = "ctr_model"
        champ = _get_champion_version()

        if champ is None:
            logger.error("Couldn't find the model")
            raise ValueError("Couldn't find the model")

        model_uri = f"models:/{model_name}/{champ}"
        _model = mlflow.xgboost.load_model(model_uri)

        version = client.get_model_version(name = model_name, version = champ)

        run = client.get_run(version.run_id)

        _model_info = {
            "model_name" : model_name,
            "version" : str(version.version),
            "tags" : version.tags["stage"],
            "test_auc": run.data.metrics["test_auc"]
        }
    except Exception as e:
        logger.error(f"Failed to load the model: {e}")
        raise

def unload():
    global _model , _model_info
    _model = None
    _model_info = {}

def get_model():
    return _model

def get_info():
    return _model_info

if __name__ == "__main__":
    load()
    model = get_model()
    print(type(model))