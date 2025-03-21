-- Sample Data Creation Script

-- Use the development database
USE DATABASE CICD_LAB_DEV;
USE SCHEMA DATA_SECURITY;
USE WAREHOUSE CICD_LAB_WH;

-- Create a table with PII data for testing
CREATE OR REPLACE TABLE CUSTOMER_DATA (
    CUSTOMER_ID INT,
    NAME VARCHAR(100),
    EMAIL VARCHAR(100),
    PHONE VARCHAR(20),
    CREDIT_CARD VARCHAR(19),
    SSN VARCHAR(11)
);

-- Insert dummy data
INSERT INTO CUSTOMER_DATA VALUES
(1, 'John Doe', 'john.doe@example.com', '123-456-7890', '4111-1111-1111-1111', '123-45-6789'),
(2, 'Jane Smith', 'jane.smith@company.org', '456-789-0123', '5555-5555-5555-4444', '456-78-9012'),
(3, 'Bob Johnson', 'bob.johnson@mail.net', '789-012-3456', '3782-8224-6310-005', '789-01-2345'),
(4, 'Alice Brown', 'alice.brown@gmail.com', '555-123-4567', '6011-0009-9013-9424', '321-54-9876'),
(5, 'Charlie Wilson', 'charlie.wilson@yahoo.com', '888-555-1212', '3566-0020-2036-0505', '987-65-4321'),
(6, 'Diana Miller', 'diana.miller@hotmail.com', '212-555-1234', '6011-6011-6011-6611', '111-22-3333'),
(7, 'Evan Davis', 'evan.davis@outlook.com', '415-555-6789', '5105-1051-0510-5100', '444-55-6666'),
(8, 'Fiona White', 'fiona.white@aol.com', '303-555-9876', '4012-8888-8888-1881', '777-88-9999'),
(9, 'George Clark', 'george.clark@icloud.com', '650-555-5432', '3530-1113-3036-0020', '222-33-4444'),
(10, 'Helen Walker', 'helen.walker@protonmail.com', '702-555-1111', '6304-1000-0000-0007', '555-66-7777');

-- Copy to production for consistency
USE DATABASE CICD_LAB_PROD;
USE SCHEMA DATA_SECURITY;

CREATE OR REPLACE TABLE CUSTOMER_DATA AS 
SELECT * FROM CICD_LAB_DEV.DATA_SECURITY.CUSTOMER_DATA;
