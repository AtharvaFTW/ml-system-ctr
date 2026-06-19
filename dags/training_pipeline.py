from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta, timezone


default_args = {
    "owner" : "airflow",
    "retries" : 1,
    "retry_delay" : timedelta(minutes= 5) 
}

def validate_data():
    pass

def retrieve_features():
    pass

def train_model():
    pass

def evaluate_model():
    pass

def register_model():
    pass


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
        task_id = "register_model",
        python_callable = register_model
    )

    t1 >> t2 >> t3 >> t4 >> t5