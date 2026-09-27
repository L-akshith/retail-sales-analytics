-- ============================================================
-- Retail Sales Analytics — Data Loading Script
-- ============================================================
-- Load the cleaned CSV into the sales_orders table.
-- Adjust the file path to match your local environment.
-- ============================================================

USE retail_analytics;

-- ────────────────────────────────────────────────────────────
-- Option 1: MySQL LOAD DATA (fastest for large files)
-- ────────────────────────────────────────────────────────────
-- Note: Adjust the file path below to your local path
-- Ensure MySQL has FILE privileges and secure_file_priv is configured

LOAD DATA INFILE '/path/to/data/processed/cleaned_sales.csv'
INTO TABLE sales_orders
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    row_id, order_id, @order_date, @ship_date, ship_mode,
    customer_id, customer_name, segment, country, city,
    state, postal_code, region, product_id, category,
    sub_category, product_name, sales, quantity, discount,
    profit, revenue, profit_margin, order_month, order_year,
    order_month_name, order_quarter, order_year_month,
    shipping_days, has_discount, is_profitable
)
SET
    order_date = STR_TO_DATE(@order_date, '%Y-%m-%d'),
    ship_date = STR_TO_DATE(@ship_date, '%Y-%m-%d');

-- ────────────────────────────────────────────────────────────
-- Option 2: Verify loaded data
-- ────────────────────────────────────────────────────────────
SELECT COUNT(*) AS total_rows FROM sales_orders;
SELECT * FROM sales_orders LIMIT 5;

-- ────────────────────────────────────────────────────────────
-- Option 3: Alternative — Python-based loading
-- ────────────────────────────────────────────────────────────
-- If MySQL LOAD DATA doesn't work, use Python + SQLAlchemy:
--
--   import pandas as pd
--   from sqlalchemy import create_engine
--
--   engine = create_engine('mysql+pymysql://user:pass@localhost/retail_analytics')
--   df = pd.read_csv('data/processed/cleaned_sales.csv')
--   df.to_sql('sales_orders', engine, if_exists='replace', index=False)
