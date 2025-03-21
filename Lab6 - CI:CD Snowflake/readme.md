# CI/CD with Snowflake: Data Masking UDF Lab

This repository contains the code for a CI/CD pipeline with Snowflake, demonstrating how to build, test, and deploy a data masking User-Defined Function (UDF) using GitHub Actions.

## Overview

The Data Masking UDF provides functionality to mask Personally Identifiable Information (PII) such as:
- Email addresses
- Phone numbers
- Credit card numbers
- Social Security Numbers (SSNs)

The UDF supports different masking levels (high, medium, low) and is implemented using Snowpark Python.

## Project Structure

```
snowflake-cicd-lab/
├── .github/
│   └── workflows/
│       └── snowpark-ci-cd.yml     # GitHub Actions workflow
├── config/
│   ├── dev.yml                    # Development environment config
│   └── prod.yml                   # Production environment config
├── src/
│   └── data_masker/               # Snowpark UDF project
│       ├── requirements.txt       # Dependencies
│       ├── snowflake.yml          # Snowflake project definition
│       └── data_masker/
│           ├── __init__.py
│           └── function.py        # UDF implementation
├── scripts/
│   ├── setup_snowflake.sql        # Initial setup script
│   ├── load_sample_data.sql       # Load sample data with PII
│   ├── test_udf.sql               # SQL tests for the UDF
│   └── cleanup.sql                # Cleanup script
├── tests/
│   └── test_data_masker.py        # Python unit tests
├── deploy_snowpark_app.py         # Manual deployment script
└── README.md                      # This file
```

## Prerequisites

- Snowflake account with ACCOUNTADMIN privileges
- GitHub account
- Python 3.10 or later
- Snowflake CLI (snow) installed

## Step-by-Step Setup and Execution

### 1. Clone the Repository

```bash
git clone https://github.com/[your-username]/snowflake-cicd-lab.git
cd snowflake-cicd-lab
```

### 2. Set Up Snowflake Environment

1. Log in to your Snowflake account using ACCOUNTADMIN role
2. Run the setup script to create necessary Snowflake objects:

```bash
snowsql -f scripts/setup_snowflake.sql
```

Or execute the script through the Snowflake web UI.

3. Load the sample data:

```bash
snowsql -f scripts/load_sample_data.sql
```

### 3. Configure Your Local Environment

1. Install required Python packages:

```bash
pip install -r src/data_masker/requirements.txt
pip install pytest snowflake-cli-labs pyyaml
```

2. Set Snowflake connection environment variables:

```bash
export SNOWFLAKE_ACCOUNT="your-account-identifier"
export SNOWFLAKE_USER="your-username"
export SNOWFLAKE_PASSWORD="your-password"
export SNOWFLAKE_ROLE="CICD_LAB_ROLE"
export SNOWFLAKE_WAREHOUSE="CICD_LAB_WH"
```

### 4. Run Unit Tests Locally

```bash
pytest tests/test_data_masker.py -v
```

### 5. Deploy Manually to Development Environment

```bash
python deploy_snowpark_app.py --env dev
```

### 6. Test the UDF in Snowflake

Execute the test script in Snowflake:

```bash
snowsql -f scripts/test_udf.sql
```

Or through the Snowflake web UI.

### 7. Configure GitHub Actions for CI/CD

1. Fork this repository if you haven't already
2. In your GitHub repository, go to Settings > Secrets and Variables > Actions
3. Add the following repository secrets:
   - `SNOWFLAKE_ACCOUNT`: Your Snowflake account identifier
   - `SNOWFLAKE_USER`: Your Snowflake username
   - `SNOWFLAKE_PASSWORD`: Your Snowflake password
   - `SNOWFLAKE_ROLE`: CICD_LAB_ROLE
   - `SNOWFLAKE_WAREHOUSE`: CICD_LAB_WH

### 8. Experience the CI/CD Pipeline

The CI/CD pipeline is triggered automatically when you push to the repository:
- Pushing to the `dev` branch deploys to the development environment
- Pushing to the `main` branch deploys to the production environment

1. Create a new branch and make a change to the UDF:

```bash
git checkout -b feature/update-udf
# Make changes to src/data_masker/data_masker/function.py
git add src/data_masker/data_masker/function.py
git commit -m "Update UDF functionality"
git push -u origin feature/update-udf
```

2. Create a pull request to merge into the `dev` branch
3. After the PR is merged, the GitHub Actions workflow will deploy to DEV
4. When ready for production, create a PR from `dev` to `main`
5. After the PR is merged, the GitHub Actions workflow will deploy to PROD

### 9. Clean Up When Finished

```bash
snowsql -f scripts/cleanup.sql
```

## UDF Usage Examples

After deployment, you can use the UDF in Snowflake as follows:

```sql
-- Mask an email address
SELECT mask_pii('john.doe@example.com', 'email', 'medium');
-- Result: j******@e******.com

-- Mask a phone number
SELECT mask_pii('123-456-7890', 'phone', 'medium');
-- Result: XXX-XXX-7890

-- Mask a credit card number
SELECT mask_pii('4111-1111-1111-1111', 'credit_card', 'medium');
-- Result: 4XXX-XXXX-XXXX-1111

-- Mask a Social Security Number
SELECT mask_pii('123-45-6789', 'ssn', 'medium');
-- Result: XXX-XX-6789

-- Create a masked view of customer data
CREATE OR REPLACE VIEW MASKED_CUSTOMER_DATA AS
SELECT 
    CUSTOMER_ID,
    NAME,
    mask_pii(EMAIL, 'email', 'medium') AS EMAIL,
    mask_pii(PHONE, 'phone', 'medium') AS PHONE,
    mask_pii(CREDIT_CARD, 'credit_card', 'medium') AS CREDIT_CARD,
    mask_pii(SSN, 'ssn', 'medium') AS SSN
FROM CUSTOMER_DATA;
```

## Troubleshooting

- **Authentication Issues**: Verify your Snowflake credentials are correctly set
- **Permission Errors**: Ensure the CICD_LAB_ROLE has all required privileges
- **Deployment Failures**: Check the GitHub Actions logs for detailed errors
- **Testing Errors**: Confirm your Python environment has all dependencies installed

## Resources

- [Snowflake Documentation](https://docs.snowflake.com/)
- [Snowpark Python Developer Guide](https://docs.snowflake.com/en/developer-guide/snowpark/python/index.html)
- [Snowflake CLI Documentation](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index.html)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
