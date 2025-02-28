from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def fetch_data():
    """Fetch data from backend API"""
    try:
        response = requests.get('http://backend:8000/data')
        data = response.json()
        print(f"Fetched {len(data)} records")
        return data
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return None

def process_data(**context):
    """Process the fetched data"""
    ti = context['task_instance']
    data = ti.xcom_pull(task_ids='fetch_data_task')
    
    if data:
        print(f"Processing {len(data)} records")
        # Add your processing logic here
        print("Data processing completed")
    else:
        print("No data to process")

with DAG(
    'example_data_pipeline',
    default_args=default_args,
    description='An example DAG that fetches and processes data',
    schedule_interval=timedelta(days=1),
) as dag:

    fetch_task = PythonOperator(
        task_id='fetch_data_task',
        python_callable=fetch_data,
    )

    process_task = PythonOperator(
        task_id='process_data_task',
        python_callable=process_data,
    )

    fetch_task >> process_task