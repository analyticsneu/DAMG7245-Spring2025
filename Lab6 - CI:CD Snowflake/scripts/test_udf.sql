-- Script to test the UDF after deployment

-- Use the development environment
USE DATABASE CICD_LAB_DEV;
USE SCHEMA DATA_SECURITY;
USE WAREHOUSE CICD_LAB_WH;

-- Test with individual values
SELECT mask_pii('john.doe@example.com', 'email', 'medium');
SELECT mask_pii('123-456-7890', 'phone', 'medium');
SELECT mask_pii('4111-1111-1111-1111', 'credit_card', 'medium');
SELECT mask_pii('123-45-6789', 'ssn', 'medium');

-- Test with different masking levels
SELECT 
    mask_pii('john.doe@example.com', 'email', 'low') AS LOW_MASK,
    mask_pii('john.doe@example.com', 'email', 'medium') AS MEDIUM_MASK,
    mask_pii('john.doe@example.com', 'email', 'high') AS HIGH_MASK;

-- Test with actual customer data
SELECT 
    CUSTOMER_ID,
    NAME,
    EMAIL,
    mask_pii(EMAIL, 'email', 'medium') AS MASKED_EMAIL,
    PHONE,
    mask_pii(PHONE, 'phone', 'medium') AS MASKED_PHONE,
    CREDIT_CARD,
    mask_pii(CREDIT_CARD, 'credit_card', 'medium') AS MASKED_CC,
    SSN,
    mask_pii(SSN, 'ssn', 'medium') AS MASKED_SSN
FROM CUSTOMER_DATA;

-- Create a view with masked data
CREATE OR REPLACE VIEW MASKED_CUSTOMER_DATA AS
SELECT 
    CUSTOMER_ID,
    NAME,
    mask_pii(EMAIL, 'email', 'medium') AS EMAIL,
    mask_pii(PHONE, 'phone', 'medium') AS PHONE,
    mask_pii(CREDIT_CARD, 'credit_card', 'medium') AS CREDIT_CARD,
    mask_pii(SSN, 'ssn', 'medium') AS SSN
FROM CUSTOMER_DATA;

-- Query the masked view
SELECT * FROM MASKED_CUSTOMER_DATA;
