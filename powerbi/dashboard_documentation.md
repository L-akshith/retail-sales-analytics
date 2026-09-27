# Power BI Dashboard Documentation

## Retail Sales & Customer Analytics Dashboard

### Overview

This document provides the complete design specification for the Power BI dashboard. Follow these instructions to recreate the dashboard using the cleaned dataset (`data/processed/cleaned_sales.csv`).

---

## Data Source

**File:** `data/processed/cleaned_sales.csv`

**Import Steps:**
1. Open Power BI Desktop → Get Data → Text/CSV
2. Select `cleaned_sales.csv`
3. In the Power Query Editor:
   - Verify `Order Date` and `Ship Date` are detected as Date type
   - Verify `Sales`, `Profit`, `Revenue`, `Discount` are Decimal Number
   - Verify `Quantity` is Whole Number
   - Close & Apply

**Key Columns:**
| Column | Type | Description |
|--------|------|-------------|
| Order ID | Text | Unique order identifier |
| Order Date | Date | Transaction date |
| Customer ID | Text | Unique customer identifier |
| Customer Name | Text | Full name |
| Category | Text | Product category (3 values) |
| Sub-Category | Text | Product sub-category (17 values) |
| Region | Text | Sales region (4 values) |
| State | Text | US State |
| Revenue | Decimal | Sales amount |
| Profit | Decimal | Profit amount |
| Quantity | Integer | Units sold |
| Discount | Decimal | Discount rate (0–0.8) |
| Profit Margin | Decimal | Calculated profit margin % |
| Order Year | Integer | Year of the order |
| Order Month | Integer | Month of the order |
| Order Year-Month | Text | Year-Month string for time series |

---

## DAX Measures to Create

Create these measures in Power BI:

```dax
-- KPI Measures
Total Revenue = SUM('sales_orders'[Revenue])

Total Profit = SUM('sales_orders'[Profit])

Total Orders = DISTINCTCOUNT('sales_orders'[Order ID])

Total Customers = DISTINCTCOUNT('sales_orders'[Customer ID])

Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)

Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0) * 100

-- Year-over-Year Growth
Revenue YoY Growth =
VAR CurrentYear = [Total Revenue]
VAR PreviousYear = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR('sales_orders'[Order Date]))
RETURN DIVIDE(CurrentYear - PreviousYear, PreviousYear, 0) * 100

-- Discount Impact
Avg Discount = AVERAGE('sales_orders'[Discount]) * 100
```

---

## Dashboard Layout

### Page 1: Executive Overview

**Layout: 3 rows**

#### Row 1 — KPI Cards (6 cards, evenly spaced across top)

| Card | Measure | Format | Color |
|------|---------|--------|-------|
| Total Revenue | Total Revenue | $#,##0 | Blue (#2563EB) |
| Total Profit | Total Profit | $#,##0 | Green (#059669) |
| Total Orders | Total Orders | #,##0 | Purple (#7C3AED) |
| Total Customers | Total Customers | #,##0 | Teal (#0891B2) |
| Avg Order Value | Average Order Value | $#,##0.00 | Orange (#D97706) |
| Profit Margin | Profit Margin % | 0.0% | Green (#059669) |

#### Row 2 — Trend Charts (2 visuals, side by side)

**Left: Monthly Revenue Trend**
- Visual type: **Line Chart**
- X-axis: `Order Date` (monthly granularity)
- Y-axis: `Total Revenue`
- Color: Blue (#2563EB)
- Add a trend line

**Right: Monthly Profit Trend**
- Visual type: **Area Chart**
- X-axis: `Order Date` (monthly granularity)
- Y-axis: `Total Profit`
- Color: Green (#059669)
- Conditional formatting: Red for negative months

#### Row 3 — Category & Region (2 visuals, side by side)

**Left: Revenue by Category**
- Visual type: **Donut Chart**
- Values: `Total Revenue`
- Legend: `Category`
- Colors: Technology (#2563EB), Furniture (#7C3AED), Office Supplies (#059669)

**Right: Revenue by Region**
- Visual type: **Clustered Bar Chart**
- Y-axis: `Region`
- X-axis: `Total Revenue`, `Total Profit`
- Sort: By revenue descending

---

### Page 2: Product Performance

#### Top Section — Sub-Category Analysis

**Visual: Clustered Bar Chart**
- Y-axis: `Sub-Category`
- X-axis: `Total Revenue`, `Total Profit`
- Sort: By revenue descending
- Conditional formatting: Red bars for negative profit sub-categories

#### Middle — Top 10 Products

**Left: Top 10 Products by Revenue**
- Visual type: **Horizontal Bar Chart**
- Y-axis: `Product Name` (Top N filter = 10)
- X-axis: `Total Revenue`
- Color: Blue gradient

**Right: Top 10 Products by Profit**
- Visual type: **Horizontal Bar Chart**
- Y-axis: `Product Name` (Top N filter = 10)
- X-axis: `Total Profit`
- Color: Green gradient

#### Bottom — Discount vs Profit

**Visual: Scatter Chart**
- X-axis: `Discount` (average)
- Y-axis: `Total Profit`
- Detail: `Sub-Category`
- Size: `Total Revenue`
- Add a reference line at Profit = 0

---

### Page 3: Customer & Regional Deep Dive

#### Left Column — Customer Analysis

**Top: Top 10 Customers Table**
- Visual type: **Table**
- Columns: Customer Name, Total Revenue, Total Profit, Profit Margin %, Total Orders
- Sort: By revenue descending
- Conditional formatting: Data bars for revenue, red highlight for negative profit

**Bottom: Customer Concentration**
- Visual type: **Pie Chart** or text card showing:
  - "Top 20% of customers generate 48% of revenue"

#### Right Column — Regional Analysis

**Top: Revenue & Profit by Region**
- Visual type: **Matrix**
- Rows: Region → State (drill-down)
- Values: Total Revenue, Total Profit, Profit Margin %
- Conditional formatting: Red for negative margins

**Bottom: States with Negative Profit**
- Visual type: **Table**
- Filter: States where Profit < 0
- Columns: State, Revenue, Profit, Margin %
- Highlight: Red background

---

## Slicers

Add the following slicers (place on left sidebar or top of each page):

| Slicer | Field | Type |
|--------|-------|------|
| Date Range | Order Date | Date range slider |
| Region | Region | Dropdown |
| Category | Category | Dropdown |
| Sub-Category | Sub-Category | Dropdown |
| Customer | Customer Name | Search-enabled dropdown |

**Slicer Sync:** Sync Date, Region, and Category slicers across all pages.

---

## Drill-Down Configuration

1. **Region → State → City:** On the regional bar/matrix, enable drill-down hierarchy.
2. **Category → Sub-Category → Product:** On category visuals, enable drill-down.
3. **Year → Quarter → Month:** On time-series charts, enable date hierarchy drill-down.

---

## Formatting Guidelines

- **Theme:** Use a dark or professional theme (e.g., Power BI "Storm" or custom)
- **Font:** Segoe UI, 10pt for data, 14pt for titles
- **Background:** White or light gray (#F5F5F5)
- **Card styling:** Rounded corners, subtle shadow, colored accent bar at top
- **Number formatting:** Currency with commas ($#,##0), percentages with one decimal
- **Interactions:** Set visual interactions to "Filter" mode (not "Highlight") for slicers

---

## Bookmarks (Optional)

Create bookmarks for:
1. **Executive Summary:** Default view with all KPIs
2. **Problem Areas:** Pre-filtered to show loss-making states and sub-categories
3. **Growth Trends:** Year-over-year comparison view

---

## Color Reference

| Purpose | Hex Code |
|---------|----------|
| Primary (Revenue) | #2563EB |
| Secondary (Profit) | #059669 |
| Accent | #7C3AED |
| Warning | #D97706 |
| Danger (Loss) | #DC2626 |
| Info | #0891B2 |
| Background | #F5F5F5 |
| Text | #1F2937 |

---

*This documentation provides the complete specification to recreate the Power BI dashboard. Screenshots should be added after the dashboard is built in Power BI Desktop.*
