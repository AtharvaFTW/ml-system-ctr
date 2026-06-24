from mlflow.client import MlflowClient
import mlflow

client = MlflowClient()


def _get_champion_version():

    results = client.search_model_versions(filter_string= "name = 'ctr_model' and tags.stage = 'champion'")

    if not results:
        return None

    return results[0].version