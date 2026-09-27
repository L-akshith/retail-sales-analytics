-- ============================================================
-- Retail Sales Analytics — SQL Analysis Queries
-- ============================================================
-- 23 business queries organized by analysis area.
-- Uses: GROUP BY, ORDER BY, WHERE, CASE, CTEs, Window
-- Functions, Aggregate Functions.
-- ============================================================

USE retail_analytics;

-- ════════════════════════════════════════════════════════════
-- SECTION A: SALES PERFORMANCE
-- ════════════════════════════════════════════════════════════

-- ──────────────────────────────────────────────────────────
-- Q1. What is total revenue?
-- ──────────────────────────────────────────────────────────
SELECT
    ROUND(SUM(revenue), 2) AS total_revenue
FROM sales_orders;


-- ──────────────────────────────────────────────────────────
-- Q2. What is total profit?
-- ──────────────────────────────────────────────────────────
SELECT
    ROUND(SUM(profit), 2) AS total_profit
FROM sales_orders;


-- ──────────────────────────────────────────────────────────
-- Q3. What is the total number of unique orders?
-- ──────────────────────────────────────────────────────────
SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM sales_orders;


-- ──────────────────────────────────────────────────────────
-- Q4. What is the average order value?
-- ──────────────────────────────────────────────────────────
SELECT
    ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS avg_order_value
FROM sales_orders;


-- ──────────────────────────────────────────────────────────
-- Q5. Monthly revenue — what is the revenue by month?
-- Uses: GROUP BY, ORDER BY, date functions
-- ──────────────────────────────────────────────────────────
SELECT
    order_year,
    order_month,
    order_month_name,
    ROUND(SUM(revenue), 2)     AS monthly_revenue,
    ROUND(SUM(profit), 2)      AS monthly_profit,
    COUNT(DISTINCT order_id)   AS total_orders
FROM sales_orders
GROUP BY order_year, order_month, order_month_name
ORDER BY order_year, order_month;


-- ──────────────────────────────────────────────────────────
-- Q6. Monthly profit — trend with running total
-- Uses: Window Function (SUM OVER)
-- ──────────────────────────────────────────────────────────
WITH monthly_data AS (
    SELECT
        order_year_month,
        ROUND(SUM(profit), 2) AS monthly_profit
    FROM sales_orders
    GROUP BY order_year_month
)
SELECT
    order_year_month,
    monthly_profit,
    ROUND(SUM(monthly_profit) OVER (
        ORDER BY order_year_month
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) AS cumulative_profit
FROM monthly_data
ORDER BY order_year_month;


-- ──────────────────────────────────────────────────────────
-- Q7. Year-over-year sales growth
-- Uses: CTE, Window Function (LAG)
-- ──────────────────────────────────────────────────────────
WITH yearly_revenue AS (
    SELECT
        order_year,
        ROUND(SUM(revenue), 2) AS annual_revenue
    FROM sales_orders
    GROUP BY order_year
)
SELECT
    order_year,
    annual_revenue,
    LAG(annual_revenue) OVER (ORDER BY order_year) AS prev_year_revenue,
    ROUND(
        (annual_revenue - LAG(annual_revenue) OVER (ORDER BY order_year))
        / LAG(annual_revenue) OVER (ORDER BY order_year) * 100, 1
    ) AS yoy_growth_pct
FROM yearly_revenue
ORDER BY order_year;


-- ════════════════════════════════════════════════════════════
-- SECTION B: PRODUCT ANALYSIS
-- ════════════════════════════════════════════════════════════

-- ──────────────────────────────────────────────────────────
-- Q8. Top 10 products by revenue
-- Uses: GROUP BY, ORDER BY, LIMIT
-- ──────────────────────────────────────────────────────────
SELECT
    product_name,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2)  AS total_profit,
    SUM(quantity)           AS total_qty
FROM sales_orders
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 10;


-- ──────────────────────────────────────────────────────────
-- Q9. Top 10 products by profit
-- ──────────────────────────────────────────────────────────
SELECT
    product_name,
    ROUND(SUM(profit), 2)  AS total_profit,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit) / NULLIF(SUM(revenue), 0) * 100, 1) AS margin_pct
FROM sales_orders
GROUP BY product_name
ORDER BY total_profit DESC
LIMIT 10;


-- ──────────────────────────────────────────────────────────
-- Q10. Products with high sales but low/negative profit
-- Uses: HAVING, CASE
-- ──────────────────────────────────────────────────────────
SELECT
    product_name,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2)  AS total_profit,
    ROUND(SUM(profit) / NULLIF(SUM(revenue), 0) * 100, 1) AS margin_pct,
    CASE
        WHEN SUM(profit) < 0 THEN 'LOSS-MAKING'
        WHEN SUM(profit) / NULLIF(SUM(revenue), 0) * 100 < 5 THEN 'LOW MARGIN'
        ELSE 'OK'
    END AS profit_status
FROM sales_orders
GROUP BY product_name
HAVING total_revenue > (SELECT AVG(revenue) * 10 FROM sales_orders)
   AND margin_pct < 5
ORDER BY total_revenue DESC
LIMIT 15;


-- ──────────────────────────────────────────────────────────
-- Q11. Category-wise revenue and profit
-- Uses: GROUP BY, aggregate functions
-- ──────────────────────────────────────────────────────────
SELECT
    category,
    ROUND(SUM(revenue), 2)  AS total_revenue,
    ROUND(SUM(profit), 2)   AS total_profit,
    COUNT(DISTINCT order_id) AS order_count,
    ROUND(SUM(profit) / NULLIF(SUM(revenue), 0) * 100, 1) AS margin_pct,
    ROUND(AVG(discount) * 100, 1) AS avg_discount_pct
FROM sales_orders
GROUP BY category
ORDER BY total_revenue DESC;


-- ──────────────────────────────────────────────────────────
-- Q12. Sub-category-wise profitability (ranked)
-- Uses: Window Function (RANK)
-- ──────────────────────────────────────────────────────────
SELECT
    sub_category,
    category,
    ROUND(SUM(revenue), 2)  AS total_revenue,
    ROUND(SUM(profit), 2)   AS total_profit,
    ROUND(SUM(profit) / NULLIF(SUM(revenue), 0) * 100, 1) AS margin_pct,
    RANK() OVER (ORDER BY SUM(profit) DESC) AS profit_rank
FROM sales_orders
GROUP BY sub_category, category
ORDER BY profit_rank;


-- ════════════════════════════════════════════════════════════
-- SECTION C: CUSTOMER ANALYSIS
-- ════════════════════════════════════════════════════════════

-- ──────────────────────────────────────────────────────────
-- Q13. Top 10 customers by revenue
-- ──────────────────────────────────────────────────────────
SELECT
    customer_id,
    customer_name,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2)  AS total_profit,
    COUNT(DISTINCT order_id) AS num_orders,
    ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS avg_order_value
FROM sales_orders
GROUP BY customer_id, customer_name
ORDER BY total_revenue DESC
LIMIT 10;


-- ──────────────────────────────────────────────────────────
-- Q14. Top 10 customers by profit
-- ──────────────────────────────────────────────────────────
SELECT
    customer_id,
    customer_name,
    ROUND(SUM(profit), 2)  AS total_profit,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit) / NULLIF(SUM(revenue), 0) * 100, 1) AS margin_pct
FROM sales_orders
GROUP BY customer_id, customer_name
ORDER BY total_profit DESC
LIMIT 10;


-- ──────────────────────────────────────────────────────────
-- Q15. Number of unique customers
-- ──────────────────────────────────────────────────────────
SELECT
    COUNT(DISTINCT customer_id) AS unique_customers
FROM sales_orders;


-- ──────────────────────────────────────────────────────────
-- Q16. Average revenue per customer
-- ──────────────────────────────────────────────────────────
SELECT
    ROUND(SUM(revenue) / COUNT(DISTINCT customer_id), 2) AS avg_revenue_per_customer
FROM sales_orders;


-- ──────────────────────────────────────────────────────────
-- Q17. Repeat customer analysis
-- Uses: CTE, CASE, aggregate functions
-- ──────────────────────────────────────────────────────────
WITH customer_orders AS (
    SELECT
        customer_id,
        customer_name,
        COUNT(DISTINCT order_id) AS num_orders,
        ROUND(SUM(revenue), 2)  AS total_revenue,
        ROUND(SUM(profit), 2)   AS total_profit
    FROM sales_orders
    GROUP BY customer_id, customer_name
)
SELECT
    CASE
        WHEN num_orders = 1 THEN 'One-Time'
        WHEN num_orders BETWEEN 2 AND 5 THEN 'Regular (2-5 orders)'
        WHEN num_orders BETWEEN 6 AND 10 THEN 'Frequent (6-10 orders)'
        ELSE 'Loyal (11+ orders)'
    END AS customer_segment,
    COUNT(*)                      AS customer_count,
    ROUND(AVG(total_revenue), 2)  AS avg_revenue,
    ROUND(AVG(total_profit), 2)   AS avg_profit,
    ROUND(AVG(num_orders), 1)     AS avg_orders
FROM customer_orders
GROUP BY customer_segment
ORDER BY avg_revenue DESC;


-- ════════════════════════════════════════════════════════════
-- SECTION D: REGIONAL ANALYSIS
-- ════════════════════════════════════════════════════════════

-- ──────────────────────────────────────────────────────────
-- Q18. Revenue by region
-- ──────────────────────────────────────────────────────────
SELECT
    region,
    ROUND(SUM(revenue), 2)  AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS avg_order_value
FROM sales_orders
GROUP BY region
ORDER BY total_revenue DESC;


-- ──────────────────────────────────────────────────────────
-- Q19. Profit by region with margin
-- ──────────────────────────────────────────────────────────
SELECT
    region,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2)  AS total_profit,
    ROUND(SUM(profit) / NULLIF(SUM(revenue), 0) * 100, 1) AS margin_pct,
    CASE
        WHEN SUM(profit) / NULLIF(SUM(revenue), 0) * 100 > 12 THEN 'Strong'
        WHEN SUM(profit) / NULLIF(SUM(revenue), 0) * 100 > 5  THEN 'Moderate'
        ELSE 'Weak'
    END AS profitability_tier
FROM sales_orders
GROUP BY region
ORDER BY margin_pct DESC;


-- ──────────────────────────────────────────────────────────
-- Q20. State/City with highest revenue
-- Uses: DENSE_RANK window function
-- ──────────────────────────────────────────────────────────
WITH state_revenue AS (
    SELECT
        state,
        city,
        region,
        ROUND(SUM(revenue), 2)  AS total_revenue,
        ROUND(SUM(profit), 2)   AS total_profit,
        DENSE_RANK() OVER (
            PARTITION BY region
            ORDER BY SUM(revenue) DESC
        ) AS state_rank_in_region
    FROM sales_orders
    GROUP BY state, city, region
)
SELECT
    region,
    state,
    city,
    total_revenue,
    total_profit,
    state_rank_in_region
FROM state_revenue
WHERE state_rank_in_region <= 3
ORDER BY region, state_rank_in_region;


-- ──────────────────────────────────────────────────────────
-- Q21. Regions/States with negative profit
-- Uses: HAVING
-- ──────────────────────────────────────────────────────────
SELECT
    region,
    state,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2)  AS total_profit,
    ROUND(SUM(profit) / NULLIF(SUM(revenue), 0) * 100, 1) AS margin_pct,
    COUNT(DISTINCT order_id) AS order_count
FROM sales_orders
GROUP BY region, state
HAVING SUM(profit) < 0
ORDER BY total_profit ASC;


-- ════════════════════════════════════════════════════════════
-- SECTION E: DISCOUNT ANALYSIS
-- ════════════════════════════════════════════════════════════

-- ──────────────────────────────────────────────────────────
-- Q22. Relationship between discount and profit
-- Uses: CASE for discount banding, GROUP BY
-- ──────────────────────────────────────────────────────────
SELECT
    CASE
        WHEN discount = 0      THEN '0% (No Discount)'
        WHEN discount <= 0.10  THEN '1-10%'
        WHEN discount <= 0.20  THEN '11-20%'
        WHEN discount <= 0.30  THEN '21-30%'
        WHEN discount <= 0.50  THEN '31-50%'
        ELSE '51%+'
    END AS discount_band,
    COUNT(*)                     AS order_lines,
    ROUND(AVG(revenue), 2)       AS avg_revenue,
    ROUND(AVG(profit), 2)        AS avg_profit,
    ROUND(SUM(profit), 2)        AS total_profit,
    ROUND(SUM(profit) / NULLIF(SUM(revenue), 0) * 100, 1) AS margin_pct,
    SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) AS loss_making_orders
FROM sales_orders
GROUP BY discount_band
ORDER BY
    CASE discount_band
        WHEN '0% (No Discount)' THEN 1
        WHEN '1-10%'            THEN 2
        WHEN '11-20%'           THEN 3
        WHEN '21-30%'           THEN 4
        WHEN '31-50%'           THEN 5
        ELSE 6
    END;


-- ──────────────────────────────────────────────────────────
-- Q23. Categories/Sub-categories where discounts hurt profitability
-- Uses: CASE, GROUP BY, HAVING
-- ──────────────────────────────────────────────────────────
WITH discount_impact AS (
    SELECT
        category,
        sub_category,
        CASE WHEN discount > 0 THEN 'Discounted' ELSE 'Full Price' END AS pricing,
        ROUND(AVG(profit), 2)     AS avg_profit,
        ROUND(SUM(profit), 2)     AS total_profit,
        ROUND(AVG(profit_margin), 1) AS avg_margin,
        COUNT(*)                   AS order_count
    FROM sales_orders
    GROUP BY category, sub_category, pricing
)
SELECT
    d.category,
    d.sub_category,
    d.avg_profit   AS discounted_avg_profit,
    d.avg_margin   AS discounted_avg_margin,
    f.avg_profit   AS full_price_avg_profit,
    f.avg_margin   AS full_price_avg_margin,
    ROUND(d.avg_profit - f.avg_profit, 2) AS profit_impact,
    CASE
        WHEN d.avg_profit < 0 THEN 'LOSING MONEY on discounts'
        WHEN d.avg_profit < f.avg_profit * 0.5 THEN 'Significant margin erosion'
        ELSE 'Acceptable impact'
    END AS assessment
FROM discount_impact d
JOIN discount_impact f
    ON d.category = f.category
    AND d.sub_category = f.sub_category
    AND d.pricing = 'Discounted'
    AND f.pricing = 'Full Price'
ORDER BY profit_impact ASC;
