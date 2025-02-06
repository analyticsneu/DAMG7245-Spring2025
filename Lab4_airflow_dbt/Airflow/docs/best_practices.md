# Airflow Best Practices Guide

## Task Design Best Practices

### 1. Keep Tasks Atomic
Tasks should do one thing and do it well. This makes your pipeline:
- Easier to debug
- More maintainable
- Reusable
```python
# BAD: One task doing multiple things
def process_and_save():
    data = extract_data()
    transformed = transform(data)
    save_to_db(transformed)

# GOOD: Separate tasks for each operation
def extract_data():
    return raw_data

def transform_data(raw_data):
    return transformed_data

def save_data(transformed_data):
    save_to_db(transformed_data)
```

### 2. Proper Error Handling
```python
def task_with_error_handling(**context):
    try:
        # Your main logic
        result = process_data()
        
        # Validate results
        if not is_valid(result):
            raise ValueError("Invalid data found")
            
        return result
        
    except ValueError as e:
        # Handle expected errors
        print(f"Validation error: {str(e)}")
        # Maybe send notification
        raise
        
    except Exception as e:
        # Handle unexpected errors
        print(f"Unexpected error: {str(e)}")
        # Log or send alert
        raise
```

### 3. Use Retries Effectively
```python
task = PythonOperator(
    task_id='api_call',
    python_callable=call_api,
    retries=3,                                    # Number of retries
    retry_delay=timedelta(minutes=5),             # Wait time between retries
    retry_exponential_backoff=True,               # Increase wait time
    max_retry_delay=timedelta(minutes=30)         # Maximum wait time
)
```

## XCom Usage

### 1. Basic XCom Pattern
```python
# Task 1: Push data to XCom
def push_data(**context):
    value = calculate_something()
    context['task_instance'].xcom_push(
        key='my_data',
        value=value
    )

# Task 2: Pull data from XCom
def pull_data(**context):
    value = context['task_instance'].xcom_pull(
        task_ids='task1',
        key='my_data'
    )
    # Use the value
```

### 2. XCom Best Practices
- Use for small amounts of data only
- Use clear, descriptive key names
- Don't store sensitive information
```python
# GOOD: Small amount of data
context['task_instance'].xcom_push(
    key='order_summary',
    value={'total': 100, 'items': 5}
)

# BAD: Large dataset
context['task_instance'].xcom_push(
    key='full_data',
    value=large_dataset  # Don't do this
)
```

For large data: Use files, dump data into a file and refer that file in other tasks


## Environment Variables

### 1. Setting Up .env File
```bash
# .env file
AIRFLOW_UID=50000
AIRFLOW_GID=0

# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key

# Snowflake Credentials
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
```

### 2. Using Environment Variables in DAGs
```python
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Use environment variables
aws_key = os.getenv('AWS_ACCESS_KEY_ID')
snowflake_user = os.getenv('SNOWFLAKE_USER')

# In your tasks
def use_credentials(**context):
    aws_key = os.getenv('AWS_ACCESS_KEY_ID')
    # Use the credentials
```

## Directory Structure

```
Airflow/
├── dags/                      # DAG files
│   ├── 01_basic_concepts.py  # Basic examples
│   └── my_pipeline.py        # Your DAGs
│
├── plugins/                   # Custom components
│   └── custom_operators/     # Your operators
│
├── logs/                     # Airflow logs
│
├── docs/                     # Documentation
│   └── best_practices.md     # This guide
│
├── .env                      # Environment variables
├── docker-compose.yaml       # Docker configuration
└── README.md                # Project documentation
```

### Key Directories Explained:

1. **dags/**
   - All your DAG files go here
   - Python files only
   - Automatically loaded by Airflow

2. **plugins/**
   - Custom operators
   - Custom hooks
   - Shared utilities

3. **logs/**
   - Generated automatically
   - Contains execution logs
   - Useful for debugging

4. **docs/**
   - Project documentation
   - Best practices
   - Setup guides

### Important Files:

1. **.env**
   - Environment variables
   - Sensitive credentials
   - Never commit to git

2. **docker-compose.yaml**
   - Container configuration
   - Service definitions
   - Volume mappings

3. **README.md**
   - Project overview
   - Setup instructions
   - Prerequisites