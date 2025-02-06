"""
This DAG demonstrates a web scraping pipeline that:
1. Scrapes weather data from a website
2. Processes and transforms the data
3. Stores it in S3
4. Loads it into Snowflake
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['your-email@example.com'],
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create DAG
dag = DAG(
    'web_to_snowflake',
    default_args=default_args,
    description='Scrape web data and load to Snowflake',
    schedule_interval='@daily',
    catchup=False
)

def scrape_weather_data(**context): 
    """Scrape weather data from a website"""
    try:
        # For demo, we'll use simulated data
        data = {
            'temperature': 72,
            'humidity': 65,
            'date': context['ds'],
            'temperature_celsius': round((72 - 32) * 5/9, 2)
        }
        
        # Save to XCom for next task
        context['task_instance'].xcom_push(key='weather_data', value=data)
        print(f"Scraped data: {data}")
        return "Data scraped successfully"
    except Exception as e:
        print(f"Error scraping data: {str(e)}")
        raise

def process_data(**context):
    """Process and transform the scraped data"""
    try:
        # Get data from previous task
        data = context['task_instance'].xcom_pull(key='weather_data')
        
        # Convert to DataFrame
        df = pd.DataFrame([data])
        
        # Save as CSV
        csv_path = f"/tmp/weather_data_{context['ds_nodash']}.csv"
        df.to_csv(csv_path, index=False)
        
        # Upload to S3
        s3_hook = S3Hook(aws_conn_id='aws_default')
        s3_hook.load_file(
            filename=csv_path,
            key=f"weather/raw/{context['ds']}/data.csv",
            bucket_name='cfapublications',
            replace=True
        )
        
        print(f"Processed data saved to: {csv_path}")
        return csv_path
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        raise

# Test Snowflake connection
test_conn = SnowflakeOperator(
    task_id='test_snowflake_connection',
    snowflake_conn_id='snowflake_default',
    sql="SELECT CURRENT_TIMESTAMP;",
    dag=dag
)

# Create stage
create_stage = SnowflakeOperator(
    task_id='create_s3_stage',
    snowflake_conn_id='snowflake_default',
    sql="""
    CREATE STAGE IF NOT EXISTS my_s3_stage
    URL='s3://cfapublications/weather/raw/'
    CREDENTIALS=(AWS_KEY_ID='{{ conn.aws_default.login }}'
                AWS_SECRET_KEY='{{ conn.aws_default.password }}');
    """,
    dag=dag
)

# Create tasks
scrape_task = PythonOperator(
    task_id='scrape_weather_data',
    python_callable=scrape_weather_data,
    provide_context=True,
    dag=dag,
)

process_task = PythonOperator(
    task_id='process_data',
    python_callable=process_data,
    provide_context=True,
    dag=dag,
)

# Add a task to create table
create_table = SnowflakeOperator(
    task_id='create_snowflake_table',
    snowflake_conn_id='snowflake_default',
    sql="""
    CREATE TABLE IF NOT EXISTS weather_table (
        temperature FLOAT,
        humidity FLOAT,
        date DATE,
        temperature_celsius FLOAT
    );
    """,
    dag=dag
)

# Create file format
create_file_format = SnowflakeOperator(
    task_id='create_file_format',
    snowflake_conn_id='snowflake_default',
    sql="""
    CREATE OR REPLACE FILE FORMAT my_csv_format
        TYPE = 'CSV'
        FIELD_DELIMITER = ','
        SKIP_HEADER = 1
        NULL_IF = ('NULL', 'null')
        EMPTY_FIELD_AS_NULL = TRUE
        DATE_FORMAT = 'YYYY-MM-DD';
    """,
    dag=dag
)

# Snowflake Load task
load_to_snowflake = SnowflakeOperator(
    task_id='load_to_snowflake',
    snowflake_conn_id='snowflake_default',
    sql="""
    COPY INTO weather_table(temperature, humidity, date, temperature_celsius)
    FROM @my_s3_stage/{{ ds }}/
    FILE_FORMAT = my_csv_format
    ON_ERROR = 'CONTINUE';
    """,
    dag=dag
)

# Set task dependencies
test_conn >> create_stage >> create_file_format >> scrape_task >> process_task >> create_table >> load_to_snowflake