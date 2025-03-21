-- Cleanup Script

-- Use with caution - this will remove all lab resources
USE ROLE CICD_LAB_ROLE;

-- Drop databases
DROP DATABASE IF EXISTS CICD_LAB_DEV;
DROP DATABASE IF EXISTS CICD_LAB_PROD;

-- Drop warehouse
DROP WAREHOUSE IF EXISTS CICD_LAB_WH;

-- Switch to ACCOUNTADMIN to drop role
USE ROLE ACCOUNTADMIN;
DROP ROLE IF EXISTS CICD_LAB_ROLE;
