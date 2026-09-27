"""
Business Analysis Script for Retail Sales Analytics
=====================================================
This script computes business metrics, answers consulting-level questions,
and generates the data behind the business insights and recommendations.

All numbers are computed from the actual dataset — nothing is fabricated.

Author: Laksh (Portfolio Project)
Dataset: Sample Superstore (cleaned)
"""

import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────
CLEANED_DATA_PATH = os.path.join('..', 'data', 'processed', 'cleaned_sales.csv')
REPORT_DIR = os.path.join('..', 'reports')


def load_data():
    """Load the cleaned dataset."""
    df = pd.read_csv(CLEANED_DATA_PATH, parse_dates=['Order Date', 'Ship Date'])
    print(f"Loaded {len(df)} rows x {df.shape[1]} columns")
    return df


def compute_kpi_summary(df):
    """Compute high-level KPIs for the dashboard."""
    print("\n" + "=" * 70)
    print("  KEY PERFORMANCE INDICATORS (KPIs)")
    print("=" * 70)

    total_revenue = df['Revenue'].sum()
    total_profit = df['Profit'].sum()
    total_orders = df['Order ID'].nunique()
    total_customers = df['Customer ID'].nunique()
    avg_order_value = total_revenue / total_orders
    profit_margin = (total_profit / total_revenue) * 100

    kpis = {
        'Total Revenue': f'${total_revenue:,.2f}',
        'Total Profit': f'${total_profit:,.2f}',
        'Total Orders': f'{total_orders:,}',
        'Total Customers': f'{total_customers:,}',
        'Unique Products': f'{df["Product ID"].nunique():,}',
        'Average Order Value': f'${avg_order_value:,.2f}',
        'Overall Profit Margin': f'{profit_margin:.1f}%',
    }

    for k, v in kpis.items():
        print(f"  {k:30s} {v}")

    return kpis


def analyze_sales_performance(df):
    """Sales performance analysis — monthly, yearly, growth."""
    print("\n" + "=" * 70)
    print("  SALES PERFORMANCE ANALYSIS")
    print("=" * 70)

    # Monthly revenue
    monthly = df.groupby('Order Year-Month').agg(
        Revenue=('Revenue', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique')
    ).reset_index()
    monthly = monthly.sort_values('Order Year-Month')

    print("\n  Monthly Revenue (last 12 months of data):")
    for _, row in monthly.tail(12).iterrows():
        print(f"    {row['Order Year-Month']}: "
              f"Revenue=${row['Revenue']:,.0f}  "
              f"Profit=${row['Profit']:,.0f}  "
              f"Orders={row['Orders']}")

    # Yearly summary
    yearly = df.groupby('Order Year').agg(
        Revenue=('Revenue', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique'),
        Customers=('Customer ID', 'nunique')
    ).reset_index()

    print("\n  Yearly Summary:")
    for _, row in yearly.iterrows():
        print(f"    {int(row['Order Year'])}: "
              f"Revenue=${row['Revenue']:,.0f}  "
              f"Profit=${row['Profit']:,.0f}  "
              f"Orders={row['Orders']:,.0f}  "
              f"Customers={row['Customers']:,.0f}")

    # Year-over-year growth
    print("\n  Year-over-Year Revenue Growth:")
    yearly_sorted = yearly.sort_values('Order Year')
    for i in range(1, len(yearly_sorted)):
        prev = yearly_sorted.iloc[i - 1]['Revenue']
        curr = yearly_sorted.iloc[i]['Revenue']
        growth = ((curr - prev) / prev) * 100
        print(f"    {int(yearly_sorted.iloc[i-1]['Order Year'])} → "
              f"{int(yearly_sorted.iloc[i]['Order Year'])}: {growth:+.1f}%")

    return monthly, yearly


def analyze_product_performance(df):
    """Product and category performance analysis."""
    print("\n" + "=" * 70)
    print("  PRODUCT & CATEGORY ANALYSIS")
    print("=" * 70)

    # Category performance
    cat = df.groupby('Category').agg(
        Revenue=('Revenue', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique'),
        Quantity=('Quantity', 'sum')
    ).sort_values('Revenue', ascending=False)
    cat['Margin'] = (cat['Profit'] / cat['Revenue'] * 100).round(1)

    print("\n  Category Performance:")
    for idx, row in cat.iterrows():
        print(f"    {idx:20s} Revenue=${row['Revenue']:>12,.0f}  "
              f"Profit=${row['Profit']:>10,.0f}  "
              f"Margin={row['Margin']:>5.1f}%  "
              f"Orders={row['Orders']:>5,.0f}")

    # Sub-category performance
    sub = df.groupby('Sub-Category').agg(
        Revenue=('Revenue', 'sum'),
        Profit=('Profit', 'sum')
    ).sort_values('Profit', ascending=False)
    sub['Margin'] = (sub['Profit'] / sub['Revenue'] * 100).round(1)

    print("\n  Sub-Category Performance (sorted by profit):")
    for idx, row in sub.iterrows():
        status = "✓" if row['Profit'] > 0 else "✗"
        print(f"    {status} {idx:20s} Revenue=${row['Revenue']:>10,.0f}  "
              f"Profit=${row['Profit']:>10,.0f}  "
              f"Margin={row['Margin']:>6.1f}%")

    # Top 10 products by revenue
    top_rev = (df.groupby('Product Name')['Revenue'].sum()
               .nlargest(10).reset_index())
    print("\n  Top 10 Products by Revenue:")
    for i, row in top_rev.iterrows():
        name = row['Product Name'][:50]
        print(f"    {i+1:2d}. {name:52s} ${row['Revenue']:>10,.2f}")

    # Top 10 products by profit
    top_profit = (df.groupby('Product Name')['Profit'].sum()
                  .nlargest(10).reset_index())
    print("\n  Top 10 Products by Profit:")
    for i, row in top_profit.iterrows():
        name = row['Product Name'][:50]
        print(f"    {i+1:2d}. {name:52s} ${row['Profit']:>10,.2f}")

    # Products with high revenue but low/negative profit
    product_perf = df.groupby('Product Name').agg(
        Revenue=('Revenue', 'sum'),
        Profit=('Profit', 'sum')
    )
    product_perf['Margin'] = (product_perf['Profit'] / product_perf['Revenue'] * 100)
    high_rev_low_profit = (product_perf[product_perf['Revenue'] > product_perf['Revenue'].quantile(0.75)]
                           .query('Margin < 5')
                           .sort_values('Revenue', ascending=False)
                           .head(10))

    print("\n  Products with High Revenue but Low Margin (<5%):")
    for idx, row in high_rev_low_profit.iterrows():
        name = idx[:50]
        print(f"    {name:52s} Rev=${row['Revenue']:>10,.0f}  "
              f"Margin={row['Margin']:>6.1f}%")

    return cat, sub


def analyze_customer_behavior(df):
    """Customer analysis — value, concentration, repeat behavior."""
    print("\n" + "=" * 70)
    print("  CUSTOMER ANALYSIS")
    print("=" * 70)

    customer = df.groupby(['Customer ID', 'Customer Name']).agg(
        Revenue=('Revenue', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique'),
        Quantity=('Quantity', 'sum')
    ).reset_index()
    customer['AOV'] = customer['Revenue'] / customer['Orders']
    customer['Margin'] = (customer['Profit'] / customer['Revenue'] * 100).round(1)

    total_customers = len(customer)
    total_revenue = customer['Revenue'].sum()
    avg_rev_per_customer = total_revenue / total_customers

    print(f"\n  Total Unique Customers: {total_customers}")
    print(f"  Average Revenue per Customer: ${avg_rev_per_customer:,.2f}")

    # Top 10 customers by revenue
    top_cust = customer.nlargest(10, 'Revenue')
    print("\n  Top 10 Customers by Revenue:")
    for _, row in top_cust.iterrows():
        print(f"    {row['Customer Name']:30s} Rev=${row['Revenue']:>10,.0f}  "
              f"Profit=${row['Profit']:>8,.0f}  "
              f"Orders={row['Orders']:>3}  "
              f"Margin={row['Margin']:>5.1f}%")

    # Revenue concentration
    top_20_pct = int(total_customers * 0.2)
    top_20_rev = customer.nlargest(top_20_pct, 'Revenue')['Revenue'].sum()
    concentration = (top_20_rev / total_revenue) * 100
    print(f"\n  Revenue Concentration:")
    print(f"    Top 20% of customers ({top_20_pct}) generate "
          f"{concentration:.1f}% of total revenue.")

    # Repeat vs one-time customers
    repeat = customer[customer['Orders'] > 1]
    one_time = customer[customer['Orders'] == 1]
    print(f"\n  Customer Repeat Behavior:")
    print(f"    Repeat customers: {len(repeat)} ({len(repeat)/total_customers*100:.1f}%)")
    print(f"    One-time customers: {len(one_time)} ({len(one_time)/total_customers*100:.1f}%)")
    print(f"    Avg orders per repeat customer: {repeat['Orders'].mean():.1f}")
    print(f"    Avg revenue: Repeat=${repeat['Revenue'].mean():,.0f} vs "
          f"One-time=${one_time['Revenue'].mean():,.0f}")

    return customer


def analyze_regional_performance(df):
    """Regional analysis — revenue, profit, top states."""
    print("\n" + "=" * 70)
    print("  REGIONAL ANALYSIS")
    print("=" * 70)

    # By region
    region = df.groupby('Region').agg(
        Revenue=('Revenue', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique'),
        Customers=('Customer ID', 'nunique')
    ).sort_values('Revenue', ascending=False)
    region['Margin'] = (region['Profit'] / region['Revenue'] * 100).round(1)

    print("\n  Performance by Region:")
    for idx, row in region.iterrows():
        print(f"    {idx:10s} Revenue=${row['Revenue']:>12,.0f}  "
              f"Profit=${row['Profit']:>10,.0f}  "
              f"Margin={row['Margin']:>5.1f}%  "
              f"Orders={row['Orders']:>5,.0f}")

    # Top 10 states by revenue
    state = df.groupby('State').agg(
        Revenue=('Revenue', 'sum'),
        Profit=('Profit', 'sum')
    ).sort_values('Revenue', ascending=False)
    state['Margin'] = (state['Profit'] / state['Revenue'] * 100).round(1)

    print("\n  Top 10 States by Revenue:")
    for idx, row in state.head(10).iterrows():
        status = "✓" if row['Profit'] > 0 else "✗"
        print(f"    {status} {idx:25s} Revenue=${row['Revenue']:>10,.0f}  "
              f"Profit=${row['Profit']:>10,.0f}  Margin={row['Margin']:>5.1f}%")

    # States with negative profit
    negative_states = state[state['Profit'] < 0].sort_values('Profit')
    if len(negative_states) > 0:
        print(f"\n  States with Negative Profit ({len(negative_states)}):")
        for idx, row in negative_states.iterrows():
            print(f"    ✗ {idx:25s} Revenue=${row['Revenue']:>10,.0f}  "
                  f"Loss=${row['Profit']:>10,.0f}")

    # Top 10 cities by revenue
    city = df.groupby('City').agg(
        Revenue=('Revenue', 'sum'),
        Profit=('Profit', 'sum')
    ).sort_values('Revenue', ascending=False)

    print("\n  Top 10 Cities by Revenue:")
    for idx, row in city.head(10).iterrows():
        print(f"    {idx:25s} Revenue=${row['Revenue']:>10,.0f}  "
              f"Profit=${row['Profit']:>10,.0f}")

    return region


def analyze_discount_impact(df):
    """Analyze the relationship between discounts and profitability."""
    print("\n" + "=" * 70)
    print("  DISCOUNT ANALYSIS")
    print("=" * 70)

    # Overall discount impact
    discounted = df[df['Has Discount'] == 1]
    non_discounted = df[df['Has Discount'] == 0]

    print(f"\n  Discounted Orders: {len(discounted)} ({len(discounted)/len(df)*100:.1f}%)")
    print(f"  Non-Discounted:    {len(non_discounted)} ({len(non_discounted)/len(df)*100:.1f}%)")

    print(f"\n  Average Profit Comparison:")
    print(f"    Discounted:     ${discounted['Profit'].mean():>8,.2f}")
    print(f"    Non-discounted: ${non_discounted['Profit'].mean():>8,.2f}")

    print(f"\n  Profit Margin Comparison:")
    disc_margin = discounted['Profit'].sum() / discounted['Revenue'].sum() * 100
    nodisc_margin = non_discounted['Profit'].sum() / non_discounted['Revenue'].sum() * 100
    print(f"    Discounted:     {disc_margin:.1f}%")
    print(f"    Non-discounted: {nodisc_margin:.1f}%")

    # By discount band
    df_temp = df.copy()
    df_temp['Discount Band'] = pd.cut(df_temp['Discount'],
                                       bins=[-0.01, 0, 0.1, 0.2, 0.3, 0.5, 1.0],
                                       labels=['0%', '1-10%', '11-20%',
                                                '21-30%', '31-50%', '51-100%'])

    disc_analysis = df_temp.groupby('Discount Band', observed=False).agg(
        Count=('Revenue', 'count'),
        Avg_Revenue=('Revenue', 'mean'),
        Avg_Profit=('Profit', 'mean'),
        Total_Profit=('Profit', 'sum')
    ).round(2)

    print("\n  Profitability by Discount Band:")
    for idx, row in disc_analysis.iterrows():
        status = "✓" if row['Avg_Profit'] > 0 else "✗"
        print(f"    {status} {str(idx):10s} Count={row['Count']:>5.0f}  "
              f"Avg Profit=${row['Avg_Profit']:>8,.2f}  "
              f"Total Profit=${row['Total_Profit']:>12,.0f}")

    # Category-level discount sensitivity
    print("\n  Discount Impact by Category:")
    for cat in df['Category'].unique():
        cat_data = df[df['Category'] == cat]
        disc_data = cat_data[cat_data['Has Discount'] == 1]
        nodisc_data = cat_data[cat_data['Has Discount'] == 0]
        if len(disc_data) > 0 and len(nodisc_data) > 0:
            disc_avg = disc_data['Profit'].mean()
            nodisc_avg = nodisc_data['Profit'].mean()
            print(f"    {cat:20s} Discounted Avg Profit=${disc_avg:>8,.2f}  "
                  f"Non-discounted=${nodisc_avg:>8,.2f}  "
                  f"Delta=${disc_avg - nodisc_avg:>8,.2f}")


def generate_business_metrics_report(df, kpis, monthly, yearly, cat, sub,
                                     customer, region):
    """Generate a consolidated business metrics report."""
    print("\n" + "=" * 70)
    print("  GENERATING BUSINESS METRICS REPORT")
    print("=" * 70)

    lines = [
        "# Business Metrics Report",
        "",
        "## Key Performance Indicators",
        "",
        "| Metric | Value |",
        "|--------|-------|",
    ]
    for k, v in kpis.items():
        lines.append(f"| {k} | {v} |")

    lines.extend([
        "",
        "## Category Performance",
        "",
        "| Category | Revenue | Profit | Margin |",
        "|----------|---------|--------|--------|",
    ])
    for idx, row in cat.iterrows():
        margin = (row['Profit'] / row['Revenue'] * 100)
        lines.append(f"| {idx} | ${row['Revenue']:,.0f} | ${row['Profit']:,.0f} "
                     f"| {margin:.1f}% |")

    lines.extend([
        "",
        "## Sub-Category Performance",
        "",
        "| Sub-Category | Revenue | Profit | Margin |",
        "|--------------|---------|--------|--------|",
    ])
    for idx, row in sub.iterrows():
        lines.append(f"| {idx} | ${row['Revenue']:,.0f} | ${row['Profit']:,.0f} "
                     f"| {row['Margin']:.1f}% |")

    lines.extend([
        "",
        "## Regional Performance",
        "",
        "| Region | Revenue | Profit | Margin |",
        "|--------|---------|--------|--------|",
    ])
    for idx, row in region.iterrows():
        lines.append(f"| {idx} | ${row['Revenue']:,.0f} | ${row['Profit']:,.0f} "
                     f"| {row['Margin']:.1f}% |")

    report_path = os.path.join(REPORT_DIR, 'business_metrics.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"  ✓ Business metrics report saved to: {report_path}")


def main():
    """Run all business analyses."""
    print("\n" + "=" * 70)
    print("  RETAIL SALES & CUSTOMER ANALYTICS — BUSINESS ANALYSIS")
    print("=" * 70)

    df = load_data()

    kpis = compute_kpi_summary(df)
    monthly, yearly = analyze_sales_performance(df)
    cat, sub = analyze_product_performance(df)
    customer = analyze_customer_behavior(df)
    region = analyze_regional_performance(df)
    analyze_discount_impact(df)

    generate_business_metrics_report(df, kpis, monthly, yearly, cat, sub,
                                     customer, region)

    print("\n" + "=" * 70)
    print("  BUSINESS ANALYSIS COMPLETE!")
    print("=" * 70)


if __name__ == '__main__':
    main()
