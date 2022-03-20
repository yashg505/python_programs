from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

from spotify_etl import run_spotify_etl

default_args = {
    'owner' : 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 3, 14),
    'email': 'airflow@example.com',
    'email_on_failure':False,
    'email_on_retry':False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)  
}

dag = DAG(
    dag_id='spotify_dag',
    default_args=default_args,
    description='our first dag',
    schedule_interval=timedelta(days=1),
)

def just_a_function():
    print("this is airflow")

run_etl = PythonOperator(
    task_id = 'whole_spotify_etl',
    python_callable=run_spotify_etl,
    dag = dag,
)

run_etl