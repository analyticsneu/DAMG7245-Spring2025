import os
import json
import requests
from redis import Redis
from rq import Queue, Connection, Worker

# Airflow API configuration
AIRFLOW_HOST = "airflow-webserver"
AIRFLOW_PORT = 8080
AIRFLOW_USER = "airflow"
AIRFLOW_PASSWORD = "airflow"
AIRFLOW_URL = f"http://{AIRFLOW_HOST}:{AIRFLOW_PORT}"

def trigger_airflow_dag(task_data):
    """Trigger Airflow DAG with the task data."""
    endpoint = f"{AIRFLOW_URL}/api/v1/dags/pdf_extraction_dag/dagRuns"
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.post(
            endpoint,
            json={"conf": task_data},
            headers=headers,
            auth=(AIRFLOW_USER, AIRFLOW_PASSWORD)
        )
        response.raise_for_status()
        return True, response.json()
    except requests.exceptions.RequestException as e:
        return False, str(e)

def process_job(task_data):
    """Process the job by triggering Airflow DAG."""
    print(f"Processing task: {task_data}")
    success, result = trigger_airflow_dag(task_data)
    
    if success:
        print(f"Successfully triggered DAG for task {task_data.get('task_id')}")
        return {'success': True, 'result': result}
    else:
        print(f"Failed to trigger DAG: {result}")
        return {'success': False, 'error': result}

if __name__ == '__main__':
    # Connect to Redis service defined in docker-compose
    redis_conn = Redis(host='redis', port=6379)
    
    with Connection(redis_conn):
        worker = Worker(['pdf_tasks'])
        worker.work(with_scheduler=True)