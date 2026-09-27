-- ============================================================
-- Retail Sales Analytics — Database Schema
-- ============================================================
-- Database: retail_analytics
-- Table: sales_orders
-- Source: Sample Superstore Dataset (cleaned)
-- ============================================================

-- Create the database
CREATE DATABASE IF NOT EXISTS retail_analytics;
USE retail_analytics;

-- Drop existing table if it exists (for re-runs)
DROP TABLE IF EXISTS sales_orders;

-- Create the main sales orders table
CREATE TABLE sales_orders (
    row_id              INT PRIMARY KEY,
    order_id            VARCHAR(20) NOT NULL,
    order_date          DATE NOT NULL,
    ship_date           DATE NOT NULL,
    ship_mode           VARCHAR(30),
    customer_id         VARCHAR(20) NOT NULL,
    customer_name       VARCHAR(100),
    segment             VARCHAR(20),
    country             VARCHAR(50),
    city                VARCHAR(50),
    state               VARCHAR(50),
    postal_code         VARCHAR(10),
    region              VARCHAR(20),
    product_id          VARCHAR(20) NOT NULL,
    category            VARCHAR(30),
    sub_category        VARCHAR(30),
    product_name        VARCHAR(300),
    sales               DECIMAL(12, 4) NOT NULL,
    quantity            INT NOT NULL,
    discount            DECIMAL(4, 2) DEFAULT 0,
    profit              DECIMAL(12, 4),
    revenue             DECIMAL(12, 4),
    profit_margin       DECIMAL(10, 4),
    order_month         INT,
    order_year          INT,
    order_month_name    VARCHAR(20),
    order_quarter       INT,
    order_year_month    VARCHAR(10),
    shipping_days       INT,
    has_discount        TINYINT DEFAULT 0,
    is_profitable       TINYINT DEFAULT 0
);

-- Create indexes for frequently queried columns
CREATE INDEX idx_order_date ON sales_orders(order_date);
CREATE INDEX idx_customer_id ON sales_orders(customer_id);
CREATE INDEX idx_category ON sales_orders(category);
CREATE INDEX idx_region ON sales_orders(region);
CREATE INDEX idx_order_id ON sales_orders(order_id);
CREATE INDEX idx_product_id ON sales_orders(product_id);
CREATE INDEX idx_order_year_month ON sales_orders(order_year, order_month);
