# Apache Airflow Lab

This lab demonstrates how to use Apache Airflow to orchestrate a data pipeline that includes:
- Web scraping
- Data transformation
- AWS S3 integration
- Snowflake data loading

## Requirements

- Docker Desktop
- AWS Account with S3 access
- Snowflake Account

## Setup Instructions

[Installation Guide](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)

[Docker - Compose File](https://airflow.apache.org/docs/apache-airflow/2.10.4/docker-compose.yaml)



` MODIFY the docker-compose file as per your requirements`

1. Start the Airflow containers:
```bash
docker compose up -d
```

2. Access Airflow UI:
   - URL: http://localhost:8080
   - Username: airflow
   - Password: airflow

3. Configure Connections in Airflow UI:

**`Admin-> Connections`**

### AWS Connection
   - Conn Id: aws_default
   - Conn Type: Amazon Web Services
   - Login: YOUR_AWS_ACCESS_KEY
   - Password: YOUR_AWS_SECRET_KEY

Can specify region as well

### Snowflake Connection
   - Conn Id: snowflake_default
   - Conn Type: Snowflake
   - Host: your-account.snowflakecomputing.com
   - Login: your-username
   - Password: your-password
   - Schema: your-schema
   - Extra: 
     ```json
     {
       "account": "your-account",
       "database": "your-database",
       "warehouse": "your-warehouse",
       "role": "your-role"
     }
     ```
you can add these extra as a JSON or enter in the input fields in UI.

## Running the Pipeline

1. Go to Airflow UI > DAGs
2. Find 'web_to_snowflake' DAG
3. Enable the DAG
4. Trigger DAG manually or wait for scheduled run

## Pipeline Steps

1. Test Snowflake connection
2. Create S3 stage in Snowflake
3. Create file format for CSV
4. Scrape weather data
5. Process and transform data
6. Create Snowflake table
7. Load data into Snowflake

## Directory Structure
```
Airflow/
├── dags/                      # DAG files
│   └── web_to_snowflake.py   # Sample DAG
├── logs/                      # Airflow logs
├── plugins/                   # Custom plugins
├── .env                      # Environment variables
├── docker-compose.yaml       # Docker configuration
└── README.md                 # Documentation
```

## Stopping the Environment
```bash
# Stop containers but keep data
docker compose down

# Stop containers and delete volumes
docker compose down -v
```

## References
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Snowflake Data Loading](https://docs.snowflake.com/en/user-guide/data-load-overview)
- [AWS S3 Integration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)