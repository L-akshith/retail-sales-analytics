# 📊 Retail Sales & Customer Analytics Dashboard

> A portfolio-ready Data Analytics / Business Intelligence project demonstrating SQL, Python, EDA, data cleaning, business analysis, and Power BI dashboard design — modeled after consulting engagements like NeenOpal.

---

## 📋 Table of Contents

1. [Business Problem](#business-problem)
2. [Objective](#objective)
3. [Dataset](#dataset)
4. [Tech Stack](#tech-stack)
5. [Project Architecture](#project-architecture)
6. [Data Cleaning Methodology](#data-cleaning-methodology)
7. [SQL Analysis](#sql-analysis)
8. [Python EDA](#python-eda)
9. [Power BI Dashboard](#power-bi-dashboard)
10. [Key Insights](#key-insights)
11. [Business Recommendations](#business-recommendations)
12. [Skills Demonstrated](#skills-demonstrated)
13. [How to Reproduce](#how-to-reproduce)
14. [Future Improvements](#future-improvements)
15. [Resume Entry](#resume-entry)

---

## Business Problem

A retail company has grown its revenue over 4 years (2015–2018) but faces profitability challenges in specific product categories, geographic markets, and customer accounts. Management needs data-driven answers to:

- Where is the company making and losing money?
- Which products, categories, and regions need strategic attention?
- Is the current discounting strategy sustainable?
- Which customers are most valuable?
- What seasonal patterns should inform planning?

**This project delivers a comprehensive analytics solution** — from raw data to cleaned data to SQL analysis to Python EDA to Power BI dashboard design to actionable business recommendations.

---

## Objective

Build an end-to-end analytics workflow that demonstrates the ability to:

- Clean and prepare real-world transactional data
- Write analytical SQL queries to answer business questions
- Perform exploratory data analysis with Python
- Compute meaningful business metrics
- Design a professional Power BI dashboard
- Translate data into actionable business insights
- Communicate recommendations in consulting language

**Workflow:**

```
Raw Data → Data Cleaning → SQL Analysis → Python EDA → Business Metrics → Power BI Dashboard → Insights → Recommendations
```

---

## Dataset

**Source:** [Sample Superstore Dataset](https://github.com/leonism/sample-superstore) (publicly available on GitHub/Kaggle)

| Attribute | Value |
|-----------|-------|
| **Records** | 9,994 (after cleaning) |
| **Date Range** | January 2015 – December 2018 |
| **Unique Orders** | 5,009 |
| **Unique Customers** | 793 |
| **Unique Products** | 1,862 |
| **Categories** | 3 (Furniture, Office Supplies, Technology) |
| **Regions** | 4 (West, East, Central, South) |
| **States** | 49 US states |

**Key Fields:** Order ID, Order Date, Customer ID, Customer Name, Product Name, Category, Sub-Category, Region, State, City, Sales, Quantity, Discount, Profit

⚠️ All analysis results are derived from this dataset. No numbers were fabricated.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.11** | Data cleaning, EDA, business analysis |
| **Pandas / NumPy** | Data manipulation and computation |
| **Matplotlib / Seaborn** | Data visualization |
| **SQL (MySQL)** | Database schema, analytical queries |
| **Power BI** | Dashboard design and business reporting |
| **Git / GitHub** | Version control and portfolio presentation |

---

## Project Architecture

```
retail-sales-analytics/
│
├── data/
│   ├── raw/
│   │   └── superstore_raw.csv          # Original dataset
│   └── processed/
│       ├── cleaned_sales.csv           # Cleaned & enriched dataset
│       └── cleaning_report.txt         # Cleaning summary
│
├── sql/
│   ├── schema.sql                      # Database table definition
│   ├── data_loading.sql                # Data import scripts
│   └── analysis_queries.sql            # 23 business SQL queries
│
├── python/
│   ├── data_cleaning.py                # 10-step cleaning pipeline
│   ├── eda.py                          # 12 business visualizations
│   └── business_analysis.py            # KPIs + business metrics
│
├── powerbi/
│   └── dashboard_documentation.md      # Full dashboard spec
│
├── reports/
│   ├── business_insights.md            # 10 data-driven insights
│   ├── recommendations.md              # 7 actionable recommendations
│   ├── business_metrics.md             # Computed metrics tables
│   └── charts/                         # 12 EDA visualizations (PNG)
│
├── README.md                           # This file
└── requirements.txt                    # Python dependencies
```

---

## Data Cleaning Methodology

The cleaning pipeline (`python/data_cleaning.py`) follows 10 systematic steps:

| Step | Action | Result |
|------|--------|--------|
| 1 | Load raw data | 10,800 rows, 21 columns |
| 2 | Missing value analysis | Dropped 806 rows with missing critical fields |
| 3 | Duplicate detection | Removed 504 fully duplicate rows |
| 4 | Data type correction | Converted dates, ensured numeric types |
| 5 | Invalid value detection | Validated quantities, sales, discounts, date logic |
| 6 | Outlier investigation | Identified outliers; **retained** with business justification |
| 7 | Categorical standardization | Stripped whitespace, verified consistency |
| 8 | Calculated columns | Added 10 new business fields |
| 9 | Cleaning summary | Generated automated report |
| 10 | Export | Saved to `data/processed/cleaned_sales.csv` |

**Outlier Decision:** Outliers were **NOT** blindly removed. High sales values represent legitimate bulk orders; negative profits represent real business losses from discounting. Removing them would misrepresent business reality.

**Calculated Fields Added:**
- Revenue, Profit Margin (%), Order Month/Year/Quarter
- Order Year-Month, Shipping Days, Has Discount (flag), Is Profitable (flag)

---

## SQL Analysis

The SQL analysis (`sql/analysis_queries.sql`) contains **23 queries** organized into 5 sections:

### A. Sales Performance (Q1–Q7)
- Total revenue, profit, orders, average order value
- Monthly revenue and profit trends
- Year-over-year growth analysis (using `LAG` window function)

### B. Product Analysis (Q8–Q12)
- Top 10 products by revenue and profit
- Products with high revenue but low/negative margin (using `CASE`, `HAVING`)
- Category and sub-category profitability (using `RANK` window function)

### C. Customer Analysis (Q13–Q17)
- Top customers by revenue and profit
- Average revenue per customer
- Repeat customer segmentation (using CTEs)

### D. Regional Analysis (Q18–Q21)
- Revenue and profit by region with profitability tiers
- Top cities by revenue within each region (using `DENSE_RANK`)
- States with negative profit

### E. Discount Analysis (Q22–Q23)
- Profit by discount band (using `CASE` for banding)
- Category-level discount impact analysis (using `JOIN` on CTE)

**SQL Features Used:** `GROUP BY`, `ORDER BY`, `WHERE`, `HAVING`, `CASE`, `JOIN`, CTEs, Window Functions (`LAG`, `RANK`, `DENSE_RANK`, `SUM OVER`), Aggregate Functions

---

## Python EDA

The EDA script (`python/eda.py`) generates **12 business-focused visualizations**:

| # | Chart | Business Question |
|---|-------|-------------------|
| 1 | Monthly Revenue Trend | How has revenue changed over time? |
| 2 | Monthly Profit Trend | Are there months with negative profit? |
| 3 | Revenue & Profit by Category | Which categories are most profitable? |
| 4 | Sub-Category Performance | Which sub-categories are loss-making? |
| 5 | Regional Performance | Which regions outperform others? |
| 6 | Top 10 Products by Revenue | What are our best-selling products? |
| 7 | Top 10 Customers by Revenue | Who are our most valuable customers? |
| 8 | Discount vs Profit | Do higher discounts reduce profitability? |
| 9 | Seasonal Patterns | Are there seasonal sales trends? |
| 10 | Year-over-Year Growth | Is the business growing? |
| 11 | Customer Concentration (Pareto) | How concentrated is revenue? |
| 12 | Profit Margin Heatmap | Where are we losing margin by sub-category? |

Every visualization answers a specific business question — none exist solely for decoration.

---

## Power BI Dashboard

The Power BI dashboard specification (`powerbi/dashboard_documentation.md`) includes:

### KPI Cards
- Total Revenue • Total Profit • Total Orders • Total Customers • Avg Order Value • Profit Margin

### 3-Page Layout

| Page | Focus | Key Visuals |
|------|-------|-------------|
| Executive Overview | High-level KPIs + trends | KPI cards, revenue/profit trends, category/region split |
| Product Performance | Product/sub-category deep dive | Sub-category bars, top 10 products, discount scatter |
| Customer & Regional | Customer + geography analysis | Top customers table, concentration chart, state matrix |

### Slicers
- Date Range • Region • Category • Sub-Category • Customer

### DAX Measures
- Total Revenue, Total Profit, Total Orders, Total Customers, AOV, Profit Margin %, YoY Growth

*Note: The dashboard documentation provides the complete specification for building in Power BI Desktop. Actual .pbix file requires Power BI Desktop software.*

---

## Key Insights

10 insights derived from the data, each following: **Observation → Evidence → Business Implication**

| # | Insight | Key Finding |
|---|---------|-------------|
| 1 | Technology leads profitability | 17.4% margin — highest category |
| 2 | Furniture has a margin problem | Only 2.5% margin; Tables/Bookcases lose money |
| 3 | Discounts >20% destroy profit | ~$135K in losses from over-discounting |
| 4 | 10 states are unprofitable | Texas loses $25.7K despite $170K revenue |
| 5 | Revenue moderately concentrated | Top 20% of customers = 48% of revenue |
| 6 | Strong Q4 seasonality | Nov/Dec drive ~30% of annual revenue |
| 7 | Profit growth lags revenue | Margin compression despite revenue growth |
| 8 | Copiers are profit powerhouses | ~37% margin — best sub-category |
| 9 | West region outperforms | 14.9% margin vs Central's 7.9% |
| 10 | Top revenue customer is unprofitable | Sean Miller: $25K revenue, -$1.9K loss |

Full details with evidence: [`reports/business_insights.md`](reports/business_insights.md)

---

## Business Recommendations

7 data-backed recommendations:

1. **Implement a 20% discount ceiling** — Recover ~$135K in losses
2. **Strategic review of Tables & Bookcases** — Fix the Furniture margin problem
3. **Prioritize Technology & Copier lines** — Invest in highest-margin products
4. **State-level profitability audits** — Investigate TX, OH, PA, IL
5. **Customer-level profitability tracking** — Move beyond revenue-only management
6. **Optimize Q1 promotions** — Smooth seasonal revenue dips
7. **Benchmark Central region vs West** — Close the 7-point margin gap

Full details: [`reports/recommendations.md`](reports/recommendations.md)

---

## Skills Demonstrated

| Skill Area | Specific Application |
|------------|---------------------|
| **SQL** | Schema design, CTEs, window functions (LAG, RANK, DENSE_RANK), JOINs, CASE, HAVING |
| **Python** | Pandas, NumPy, Matplotlib, Seaborn, data pipelines |
| **Data Cleaning** | Missing values, duplicates, type conversion, outlier analysis with justification |
| **EDA** | 12 business-focused visualizations, trend analysis, correlation analysis |
| **Business Intelligence** | KPI computation, metrics framework, dashboard design |
| **Power BI** | DAX measures, multi-page dashboard, slicers, drill-down, formatting |
| **Business Analysis** | Consulting-style insights, Pareto analysis, margin analysis |
| **Communication** | Observation-Evidence-Implication framework, actionable recommendations |
| **Problem Solving** | Identifying unprofitable segments, discount strategy analysis, customer segmentation |

---

## How to Reproduce

### Prerequisites
- Python 3.8+
- MySQL 8.0+ (optional, for SQL queries)
- Power BI Desktop (optional, for dashboard)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/retail-sales-analytics.git
cd retail-sales-analytics

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Run data cleaning
cd python
python data_cleaning.py

# 4. Run EDA (generates charts)
python eda.py

# 5. Run business analysis
python business_analysis.py

# 6. (Optional) Load into MySQL
# Edit sql/data_loading.sql with your file path
mysql -u root -p < sql/schema.sql
mysql -u root -p < sql/data_loading.sql

# 7. (Optional) Open Power BI
# Import data/processed/cleaned_sales.csv into Power BI Desktop
# Follow powerbi/dashboard_documentation.md
```

---

## Future Improvements

1. **Customer Segmentation (RFM Analysis):** Implement Recency-Frequency-Monetary analysis for customer segmentation.
2. **Predictive Modeling:** Build a sales forecasting model using ARIMA or Prophet.
3. **Interactive Web Dashboard:** Create a Streamlit or Dash web app for interactive exploration.
4. **Automated Pipeline:** Schedule data cleaning and analysis with Airflow or cron jobs.
5. **A/B Testing Framework:** Design experiments for discount strategy optimization.
6. **Market Basket Analysis:** Identify product co-purchase patterns using association rules.

---

## Resume Entry

### ATS-Friendly Resume Bullets

- **Developed** a retail sales analytics solution using **Python (Pandas, NumPy, Matplotlib, Seaborn)** and **SQL**, analyzing 9,994 transactions to identify $135K+ in profit leakage from suboptimal discounting strategies across 5,009 orders.

- **Designed** 23 analytical **SQL queries** leveraging CTEs, window functions (LAG, RANK), and multi-level aggregations to uncover category-level, regional, and customer profitability insights for a retail dataset spanning 793 customers and 4 years of data.

- **Created** a 3-page **Power BI dashboard** with 6 KPI cards, interactive slicers, drill-down hierarchies, and DAX measures to visualize revenue trends, product performance, and regional profitability for executive decision-making.

- **Delivered** 10 data-driven business insights and 7 actionable recommendations in a consulting framework (Observation → Evidence → Implication), identifying 10 unprofitable U.S. states and 2 loss-making product sub-categories for strategic review.

---

## License

This project is for educational and portfolio purposes. The Sample Superstore dataset is publicly available and commonly used for analytics practice.

---

*Built as a portfolio project for Data Analyst / Business Intelligence consulting roles.*
