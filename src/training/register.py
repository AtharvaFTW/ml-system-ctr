import mlflow 
from mlflow.client import MlflowClient


from src.utils.logger import get_logger

logger = get_logger(__name__)

client = MlflowClient()

def get_champion_auc():
    """
    Fetch the current champion's AUC-ROC score.

    """
    try:
        logger.info("Fetching the current champion AUC-ROC score...")
        results = client.search_registered_models(filter_string ="tags.stage = 'champion'")
        
        if not results:
            logger.info("No current champion found!")
            return 0.0
        
        champion_version = results[0].latest_versions[0]
        run_id = champion_version.run_id

        run = client.get_run(run_id)
        current_auc = float(run.data.metrics["test_auc"])

        logger.info(f"Current champion AUC-ROC score: {current_auc}")
    
    except Exception as e:
        logger.error(f"❌ Champion AUC-ROC fetch failed: {e}")
        raise

    return current_auc 
    
def register_model(run_id, metrics) -> str:
    """
    Register the model.

    Args: 
        run_id: Challenger run_id (tracked during training)
        metrics: Challenger metrics
    
    Returns:
        str: model version for challenger
    """
    try:
        logger.info("Registering the model...")
        model_version = mlflow.register_model(f"runs:/{run_id}/model", "ctr_model")
        client.set_registered_model_tag("ctr_model", "stage", "challenger")
        client.set_model_version_tag("ctr_model", model_version.version, "test_auc", metrics["auc_score"])

        logger.info("✔ Model registered successfully!")
    except Exception as e:
        logger.error(f"❌ Model registration failed: {e}")
        raise
    return model_version.version

def update_champion(model_name, version, metrics) -> None:
    """
    Compare the score of the challenger and the current champion model and update the champion.

    model_name: ctr_model in this case.
    version: challenger model version
    metrics: challenger model metrics
    """
    try:
        champion_auc = get_champion_auc()
        challenger_auc = metrics["auc_score"]

        logger.info("Comparing the challenger AUC with champion AUC...")
        if challenger_auc > champion_auc:
            results = client.search_registered_models (filter_string = "tags.stage = 'champion'")
            if results:
                champion_ver = results[0].latest_versions[0].version
                client.set_model_version_tag(model_name, champion_ver, "stage", "retired")

            
            client.set_model_version_tag(model_name, version, "stage", "champion")
            logger.info(f"✔ Challenger promoted as new Champion! AUC: {challenger_auc}")

        else:
            client.set_model_version_tag(model_name, version, "stage", "retired")
            logger.info(f"Challenger couldn't beat the champion.")
            logger.info(f"Challenger {challenger_auc} | Champion {champion_auc}")

    except Exception as e:
        logger.error(f"Failed to compare the challenger to the champion: {e}")
        raise


if __name__ == "__main__":
    update_champion()
    