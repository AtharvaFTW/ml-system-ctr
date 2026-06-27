from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta


default_args = {
    "owner" : "airflow",
    "retries" : 1,
    "retry_delay" : timedelta(minutes= 5) 
}

def validate_data(**context):
    from src.data.pipeline import run_pipeline

    run_pipeline(n_rows= 100000)
    

def retrieve_features(**context):
    from src.features.feature_pipeline import push_features_to_store
    push_features_to_store()
    

def train_model(**context):
    from src.training.train import run_training

    model, run_id = run_training()

    context['ti'].xcom_push(key = 'run_id', value = run_id)


def evaluate_model(**context):
    import mlflow

    from src.training.evaluate import run_evaluation

    run_id = context['ti'].xcom_pull(key = "run_id", task_ids = "train_model")
    model = mlflow.xgboost.load_model(f"runs:/{run_id}/model")

    test_metrics = run_evaluation(model, run_id)

    context['ti'].xcom_push(key = "test_metrics", value = test_metrics)


def register_model_to_mlflow(**context):
    from src.training.register import register_model

    run_id = context['ti'].xcom_pull(key = "run_id", task_ids = "train_model")
    test_metrics = context['ti'].xcom_pull(key = "test_metrics", task_ids = "evaluate_model")
    register_model(run_id, test_metrics)


with DAG(
    dag_id = "training_pipeline",
    default_args = default_args,
    description = "CTR prediction training pipeline",
    schedule= None,
    start_date = datetime(2024,1,1),
    catchup= False,
    tags = ["ctr", "training"],
) as dag:
 
    t1 = PythonOperator(
        task_id = "validate_data",
        python_callable = validate_data
    )

    t2 = PythonOperator(
        task_id = "retrieve_features",
        python_callable = retrieve_features
    )

    t3 = PythonOperator(
        task_id = "train_model",
        python_callable = train_model
    )

    t4 = PythonOperator(
        task_id = "evaluate_model",
        python_callable = evaluate_model
    )

    t5 = PythonOperator(
        task_id = "register_model_to_mlflow",
        python_callable = register_model_to_mlflow
    )

    t1 >> t2 >> t3 >> t4 >> t5