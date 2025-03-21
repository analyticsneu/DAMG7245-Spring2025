# CI/CD with Snowflake and Snowpark - Lab Implementation Plan

## Overview

This document outlines the implementation plan for a comprehensive lab on CI/CD with Snowflake and Snowpark. The lab will guide students through creating and automating the deployment of Snowpark Python applications using GitHub Actions.

## Learning Objectives

By the end of this lab, students will be able to:

1. Understand CI/CD principles as they apply to Snowflake development
2. Create and test Snowpark Python applications locally
3. Configure environment-specific settings with YAML
4. Build GitHub Actions workflows for automated testing and deployment
5. Implement best practices for Snowflake CI/CD

## Lab Components

### 1. Project Structure

```
snowflake-cicd-lab/
├── .github/
│   └── workflows/
│       └── snowpark-ci-cd.yml     # GitHub Actions workflow
├── config/
│   ├── dev.yml                    # Development environment config
│   └── prod.yml                   # Production environment config
├── src/
│   ├── temperature_converter/     # Snowpark UDF project
│   │   ├── requirements.txt       # Dependencies
│   │   ├── snowflake.yml          # Snowflake project definition
│   │   └── temperature_converter/
│   │       ├── __init__.py
│   │       └── function.py        # UDF implementation
│   └── sales_processor/           # Snowpark stored procedure
│       ├── requirements.txt       # Dependencies
│       ├── snowflake.yml          # Snowflake project definition
│       └── sales_processor/
│           ├── __init__.py
│           └── procedure.py       # Stored procedure implementation
├── scripts/
│   ├── setup_snowflake.sql        # Initial setup script
│   └── load_sample_data.sql       # Load sample data
├── tests/
│   ├── test_temperature_udf.py    # UDF tests
│   └── test_sales_processor.py    # Stored procedure tests
└── README.md                      # Lab instructions
```

### 2. Key Code Examples

#### Snowflake Project Definition (snowflake.yml)

```yaml
# src/temperature_converter/snowflake.yml
definition_version: 1
snowpark:
  project_name: "cicd_lab"
  stage_name: "analytics.deployment"
  src: "temperature_converter/"
  functions:
    - name: "temperature_converter_udf"
      database: "CICD_LAB_DB"
      schema: "analytics"
      handler: "function.main"
      runtime: "3.10"
      signature:
        - name: "temp_f"
          type: "float"
      returns: float
```

#### Python UDF Implementation

```python
# src/temperature_converter/temperature_converter/function.py
from scipy.constants import convert_temperature

def main(temp_f: float) -> float:
    """
    Convert temperature from Fahrenheit to Celsius
    """
    return convert_temperature(float(temp_f), 'F', 'C')
```

#### GitHub Actions Workflow

```yaml
# .github/workflows/snowpark-ci-cd.yml
name: Snowpark CI/CD Pipeline

on:
  push:
    branches: [main, dev]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest
          pip install -r src/temperature_converter/requirements.txt
          pip install -r src/sales_processor/requirements.txt
      - name: Run tests
        run: pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    env:
      SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
      SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }}
      SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
      SNOWFLAKE_ROLE: ${{ secrets.SNOWFLAKE_ROLE }}
      SNOWFLAKE_WAREHOUSE: ${{ secrets.SNOWFLAKE_WAREHOUSE }}
      SNOWFLAKE_DATABASE: ${{ secrets.SNOWFLAKE_DATABASE }}
    
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install snowflake-cli-labs
          pip install pyyaml
      - name: Set environment variables
        run: |
          if [[ "${{ github.ref }}" == "refs/heads/main" ]]; then
            echo "ENVIRONMENT=prod" >> $GITHUB_ENV
          else
            echo "ENVIRONMENT=dev" >> $GITHUB_ENV
          fi
      - name: Deploy Snowpark applications
        run: python deploy_snowpark_apps.py $GITHUB_WORKSPACE
```

#### Deployment Script

```python
# deploy_snowpark_apps.py
import sys
import os
import yaml

def deploy_snowpark_app(directory_path):
    print(f"Deploying Snowpark app in {directory_path}")
    # Read the project configuration
    with open(f"{directory_path}/snowflake.yml", "r") as file:
        config = yaml.safe_load(file)
    
    # Get environment-specific settings
    env = os.environ.get("ENVIRONMENT", "dev")
    env_config_path = f"{os.path.dirname(os.path.dirname(directory_path))}/config/{env}.yml"
    
    with open(env_config_path, "r") as file:
        env_config = yaml.safe_load(file)
    
    # Build and deploy using Snow CLI
    os.chdir(directory_path)
    os.system(f"snow snowpark build")
    os.system(f"snow snowpark deploy --replace")

if __name__ == "__main__":
    root_dir = sys.argv[1]
    
    # Find all Snowpark projects
    for root, dirs, files in os.walk(root_dir):
        if "snowflake.yml" in files:
            deploy_snowpark_app(root)
```

### 3. Implementation Steps

1. **Environment Setup**
   - Create GitHub repository with CI/CD workflow
   - Set up GitHub Codespace configuration
   - Configure Snowflake connection

2. **Snowflake Object Creation**
   - Databases, schemas, stages, warehouses
   - User roles and permissions

3. **Snowpark Application Development**
   - Temperature converter UDF
   - Sales processor stored procedure
   - Local testing

4. **YAML Configuration**
   - Environment-specific settings
   - Parameterization techniques

5. **GitHub Actions Workflow Setup**
   - Testing automation
   - Deployment automation
   - Branch-based environment targeting

6. **Deployment Testing**
   - Manual deployment with SnowCLI
   - Automated deployment with GitHub Actions
   - Verification and troubleshooting

## Key Concepts and Technical Details

### 1. Snowflake CLI Integration

The Snowflake CLI is a critical tool for Snowpark deployment:

```bash
# Build Snowpark application
snow snowpark build

# Deploy Snowpark application
snow snowpark deploy

# Execute a function or procedure
snow snowpark execute function "temperature_converter_udf(32.0)"
```

### 2. Snowpark Python Project Structure

- **Handler**: Entry point for the UDF or stored procedure
- **Runtime version**: Python version (e.g., 3.8, 3.10)
- **Packages**: Required Python packages
- **Signature**: Input parameter definitions
- **Returns**: Return type definition

### 3. YAML Configuration for Environment Parameterization

```yaml
# config/dev.yml
environment: "dev"
database_name: "CICD_LAB_DEV"
schema_name: "analytics"
data_retention_days: 1
warehouse_size: "xsmall"

# config/prod.yml
environment: "prod"
database_name: "CICD_LAB_PROD"
schema_name: "analytics"
data_retention_days: 90
warehouse_size: "medium"
```

### 4. GitHub Actions Pipeline Flow

1. **Trigger**: Code push or manual workflow dispatch
2. **Test**: Run pytest on all Snowpark applications
3. **Build**: Package Snowpark applications
4. **Deploy**: Deploy to environment based on branch
   - `dev` branch → development environment
   - `main` branch → production environment

### 5. Secret Management in GitHub

Required secrets for Snowflake connection:
- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_ROLE`
- `SNOWFLAKE_WAREHOUSE`
- `SNOWFLAKE_DATABASE`

### 6. Testing Best Practices

- Unit tests for UDFs
- Integration tests for stored procedures
- Test environment isolation
- Automated testing in CI pipeline

## Lab Workflow

1. **Introduction to CI/CD concepts and tools**
2. **Setup of Snowflake environment**
3. **Development of Snowpark applications**
4. **Testing applications locally**
5. **Manual deployment with SnowCLI**
6. **Setup of GitHub Actions workflow**
7. **Automated deployment via CI/CD**
8. **Extension exercises**
