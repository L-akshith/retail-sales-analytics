"""
Exploratory Data Analysis (EDA) Script for Retail Sales Analytics
===================================================================
This script performs comprehensive EDA on the cleaned Superstore dataset.

Every visualization answers a specific business question.

Author: Laksh (Portfolio Project)
Dataset: Sample Superstore (cleaned)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import warnings

warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────
CLEANED_DATA_PATH = os.path.join('..', 'data', 'processed', 'cleaned_sales.csv')
CHARTS_DIR = os.path.join('..', 'reports', 'charts')

# Color palette — professional and accessible
COLORS = {
    'primary': '#2563EB',
    'secondary': '#7C3AED',
    'success': '#059669',
    'danger': '#DC2626',
    'warning': '#D97706',
    'info': '#0891B2',
    'palette': ['#2563EB', '#7C3AED', '#059669', '#DC2626', '#D97706',
                '#0891B2', '#4F46E5', '#DB2777', '#65A30D', '#EA580C']
}

# Set global style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette(COLORS['palette'])
plt.rcParams.update({
    'figure.figsize': (12, 6),
    'figure.dpi': 150,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.facecolor': 'white',
    'axes.facecolor': '#FAFAFA',
    'axes.edgecolor': '#CCCCCC',
    'grid.color': '#E5E5E5',
    'font.family': 'sans-serif',
})


def load_data():
    """Load the cleaned dataset."""
    df = pd.read_csv(CLEANED_DATA_PATH, parse_dates=['Order Date', 'Ship Date'])
    print(f"Loaded {len(df)} rows x {df.shape[1]} columns")
    return df


def ensure_charts_dir():
    """Create charts output directory if it doesn't exist."""
    os.makedirs(CHARTS_DIR, exist_ok=True)


def save_chart(fig, filename):
    """Save chart to the reports/charts directory."""
    filepath = os.path.join(CHARTS_DIR, filename)
    fig.savefig(filepath, bbox_inches='tight', dpi=150, facecolor='white')
    plt.close(fig)
    print(f"  Saved: {filepath}")


def format_currency(x, _):
    """Format large numbers as $XXK or $X.XM."""
    if abs(x) >= 1e6:
        return f'${x/1e6:.1f}M'
    elif abs(x) >= 1e3:
        return f'${x/1e3:.0f}K'
    return f'${x:.0f}'


# ─────────────────────────────────────────────────────────────
# VISUALIZATION 1: Monthly Revenue Trend
# Business Q: How has revenue changed over time?
# ─────────────────────────────────────────────────────────────
def plot_monthly_revenue_trend(df):
    """Monthly revenue trend line chart."""
    print("\n[1] Monthly Revenue Trend")

    monthly = df.groupby('Order Year-Month')['Revenue'].sum().reset_index()
    monthly['Order Year-Month'] = pd.to_datetime(monthly['Order Year-Month'])
    monthly = monthly.sort_values('Order Year-Month')

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(monthly['Order Year-Month'], monthly['Revenue'],
            color=COLORS['primary'], linewidth=2, marker='o', markersize=3)
    ax.fill_between(monthly['Order Year-Month'], monthly['Revenue'],
                    alpha=0.1, color=COLORS['primary'])

    ax.set_title('Monthly Revenue Trend (2015–2018)', fontweight='bold', fontsize=14)
    ax.set_xlabel('Month')
    ax.set_ylabel('Revenue ($)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    plt.xticks(rotation=45)
    plt.tight_layout()
    save_chart(fig, '01_monthly_revenue_trend.png')


# ─────────────────────────────────────────────────────────────
# VISUALIZATION 2: Monthly Profit Trend
# Business Q: How has profitability changed over time?
# ─────────────────────────────────────────────────────────────
def plot_monthly_profit_trend(df):
    """Monthly profit trend with positive/negative coloring."""
    print("[2] Monthly Profit Trend")

    monthly = df.groupby('Order Year-Month')['Profit'].sum().reset_index()
    monthly['Order Year-Month'] = pd.to_datetime(monthly['Order Year-Month'])
    monthly = monthly.sort_values('Order Year-Month')

    fig, ax = plt.subplots(figsize=(14, 5))
    colors = [COLORS['success'] if v >= 0 else COLORS['danger']
              for v in monthly['Profit']]
    ax.bar(monthly['Order Year-Month'], monthly['Profit'],
           color=colors, width=20, alpha=0.8)
    ax.axhline(y=0, color='black', linewidth=0.5)

    ax.set_title('Monthly Profit Trend (2015–2018)', fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Profit ($)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    plt.xticks(rotation=45)
    plt.tight_layout()
    save_chart(fig, '02_monthly_profit_trend.png')


# ─────────────────────────────────────────────────────────────
# VISUALIZATION 3: Revenue by Category
# Business Q: Which categories generate the most revenue?
# ─────────────────────────────────────────────────────────────
def plot_revenue_by_category(df):
    """Revenue and profit by category — horizontal bar chart."""
    print("[3] Revenue by Category")

    cat = df.groupby('Category').agg(
        Revenue=('Revenue', 'sum'),
        Profit=('Profit', 'sum')
    ).sort_values('Revenue', ascending=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Revenue
    axes[0].barh(cat.index, cat['Revenue'], color=COLORS['primary'], alpha=0.85)
    axes[0].set_title('Revenue by Category', fontweight='bold')
    axes[0].set_xlabel('Revenue ($)')
    axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    for i, v in enumerate(cat['Revenue']):
        axes[0].text(v + 5000, i, f'${v:,.0f}', va='center', fontsize=9)

    # Profit
    pcolors = [COLORS['success'] if v >= 0 else COLORS['danger'] for v in cat['Profit']]
    axes[1].barh(cat.index, cat['Profit'], color=pcolors, alpha=0.85)
    axes[1].set_title('Profit by Category', fontweight='bold')
    axes[1].set_xlabel('Profit ($)')
    axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    for i, v in enumerate(cat['Profit']):
        axes[1].text(v + 1000, i, f'${v:,.0f}', va='center', fontsize=9)

    plt.tight_layout()
    save_chart(fig, '03_revenue_profit_by_category.png')


# ─────────────────────────────────────────────────────────────
# VISUALIZATION 4: Revenue by Sub-Category
# Business Q: Which sub-categories perform best/worst?
# ─────────────────────────────────────────────────────────────
def plot_subcategory_performance(df):
    """Sub-category performance: revenue + profit margin."""
    print("[4] Sub-Category Performance")

    sub = df.groupby('Sub-Category').agg(
        Revenue=('Revenue', 'sum'),
        Profit=('Profit', 'sum')
    )
    sub['Margin'] = (sub['Profit'] / sub['Revenue'] * 100).round(1)
    sub = sub.sort_values('Revenue', ascending=True)

    fig, ax = plt.subplots(figsize=(12, 8))
    bar_colors = [COLORS['success'] if m >= 0 else COLORS['danger']
                  for m in sub['Margin']]
    bars = ax.barh(sub.index, sub['Revenue'], color=bar_colors, alpha=0.8)

    # Annotate with margin %
    for i, (rev, margin) in enumerate(zip(sub['Revenue'], sub['Margin'])):
        ax.text(rev + 5000, i, f'{margin:.1f}%', va='center', fontsize=9,
                color=COLORS['success'] if margin >= 0 else COLORS['danger'],
                fontweight='bold')

    ax.set_title('Revenue by Sub-Category (with Profit Margin %)',
                 fontweight='bold')
    ax.set_xlabel('Revenue ($)')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    plt.tight_layout()
    save_chart(fig, '04_subcategory_performance.png')


# ─────────────────────────────────────────────────────────────
# VISUALIZATION 5: Revenue by Region
# Business Q: Which regions outperform others?
# ─────────────────────────────────────────────────────────────
def plot_regional_performance(df):
    """Regional performance — revenue, profit, and margin."""
    print("[5] Regional Performance")

    reg = df.groupby('Region').agg(
        Revenue=('Revenue', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique')
    ).sort_values('Revenue', ascending=False)
    reg['Margin'] = (reg['Profit'] / reg['Revenue'] * 100).round(1)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Revenue
    axes[0].bar(reg.index, reg['Revenue'], color=COLORS['palette'][:len(reg)], alpha=0.85)
    axes[0].set_title('Revenue by Region', fontweight='bold')
    axes[0].set_ylabel('Revenue ($)')
    axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))

    # Profit
    pcolors = [COLORS['success'] if v >= 0 else COLORS['danger'] for v in reg['Profit']]
    axes[1].bar(reg.index, reg['Profit'], color=pcolors, alpha=0.85)
    axes[1].set_title('Profit by Region', fontweight='bold')
    axes[1].set_ylabel('Profit ($)')
    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))

    # Margin
    mcolors = [COLORS['success'] if v >= 0 else COLORS['danger'] for v in reg['Margin']]
    axes[2].bar(reg.index, reg['Margin'], color=mcolors, alpha=0.85)
    axes[2].set_title('Profit Margin by Region (%)', fontweight='bold')
    axes[2].set_ylabel('Margin (%)')
    axes[2].axhline(y=0, color='black', linewidth=0.5)

    plt.tight_layout()
    save_chart(fig, '05_regional_performance.png')


# ─────────────────────────────────────────────────────────────
# VISUALIZATION 6: Top 10 Products by Revenue
# Business Q: Which products are the top sellers?
# ─────────────────────────────────────────────────────────────
def plot_top_products(df):
    """Top 10 products by revenue."""
    print("[6] Top 10 Products by Revenue")

    top = (df.groupby('Product Name')['Revenue'].sum()
           .nlargest(10)
           .sort_values(ascending=True))

    fig, ax = plt.subplots(figsize=(12, 6))
    # Shorten long product names
    labels = [name[:45] + '...' if len(name) > 45 else name for name in top.index]
    ax.barh(labels, top.values, color=COLORS['primary'], alpha=0.85)

    ax.set_title('Top 10 Products by Revenue', fontweight='bold')
    ax.set_xlabel('Revenue ($)')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    for i, v in enumerate(top.values):
        ax.text(v + 500, i, f'${v:,.0f}', va='center', fontsize=9)

    plt.tight_layout()
    save_chart(fig, '06_top10_products_revenue.png')


# ─────────────────────────────────────────────────────────────
# VISUALIZATION 7: Top 10 Customers by Revenue
# Business Q: Who are the most valuable customers?
# ─────────────────────────────────────────────────────────────
def plot_top_customers(df):
    """Top 10 customers by revenue."""
    print("[7] Top 10 Customers by Revenue")

    top = (df.groupby('Customer Name')['Revenue'].sum()
           .nlargest(10)
           .sort_values(ascending=True))

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.barh(top.index, top.values, color=COLORS['secondary'], alpha=0.85)

    ax.set_title('Top 10 Customers by Revenue', fontweight='bold')
    ax.set_xlabel('Revenue ($)')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    for i, v in enumerate(top.values):
        ax.text(v + 500, i, f'${v:,.0f}', va='center', fontsize=9)

    plt.tight_layout()
    save_chart(fig, '07_top10_customers_revenue.png')


# ─────────────────────────────────────────────────────────────
# VISUALIZATION 8: Discount vs Profit Relationship
# Business Q: Are higher discounts associated with lower profit?
# ─────────────────────────────────────────────────────────────
def plot_discount_vs_profit(df):
    """Discount vs Profit scatter + aggregated bar chart."""
    print("[8] Discount vs Profit Relationship")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Scatter plot
    axes[0].scatter(df['Discount'], df['Profit'], alpha=0.15,
                    color=COLORS['primary'], s=10)
    axes[0].axhline(y=0, color=COLORS['danger'], linewidth=1, linestyle='--')
    axes[0].set_title('Discount vs Profit (Order Level)', fontweight='bold')
    axes[0].set_xlabel('Discount')
    axes[0].set_ylabel('Profit ($)')

    # Aggregated by discount band
    df_temp = df.copy()
    df_temp['Discount Band'] = pd.cut(df_temp['Discount'],
                                       bins=[-0.01, 0, 0.1, 0.2, 0.3, 0.5, 1.0],
                                       labels=['0%', '1-10%', '11-20%',
                                                '21-30%', '31-50%', '51-100%'])
    disc_profit = df_temp.groupby('Discount Band', observed=False)['Profit'].mean()
    bar_colors = [COLORS['success'] if v >= 0 else COLORS['danger']
                  for v in disc_profit.values]
    axes[1].bar(disc_profit.index, disc_profit.values, color=bar_colors, alpha=0.85)
    axes[1].axhline(y=0, color='black', linewidth=0.5)
    axes[1].set_title('Average Profit by Discount Band', fontweight='bold')
    axes[1].set_xlabel('Discount Band')
    axes[1].set_ylabel('Average Profit ($)')

    plt.tight_layout()
    save_chart(fig, '08_discount_vs_profit.png')


# ─────────────────────────────────────────────────────────────
# VISUALIZATION 9: Seasonal Patterns
# Business Q: Are there seasonal sales patterns?
# ─────────────────────────────────────────────────────────────
def plot_seasonal_patterns(df):
    """Revenue by month (averaged across years) to detect seasonality."""
    print("[9] Seasonal Sales Patterns")

    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    seasonal = (df.groupby(['Order Year', 'Order Month'])['Revenue'].sum()
                .reset_index()
                .groupby('Order Month')['Revenue'].mean()
                .reindex(range(1, 13)))

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(range(1, 13), seasonal.values, color=COLORS['palette'][:12], alpha=0.85)
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(month_names)
    ax.set_title('Average Monthly Revenue (Seasonal Pattern)', fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Average Revenue ($)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))

    plt.tight_layout()
    save_chart(fig, '09_seasonal_patterns.png')


# ─────────────────────────────────────────────────────────────
# VISUALIZATION 10: Year-over-Year Growth
# Business Q: How has the business grown year over year?
# ─────────────────────────────────────────────────────────────
def plot_yoy_growth(df):
    """Year-over-year revenue and profit comparison."""
    print("[10] Year-over-Year Growth")

    yearly = df.groupby('Order Year').agg(
        Revenue=('Revenue', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique')
    ).reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    x = yearly['Order Year'].astype(int)
    width = 0.35

    # Revenue + Profit
    axes[0].bar(x - width / 2, yearly['Revenue'], width, label='Revenue',
                color=COLORS['primary'], alpha=0.85)
    axes[0].bar(x + width / 2, yearly['Profit'], width, label='Profit',
                color=COLORS['success'], alpha=0.85)
    axes[0].set_title('Revenue & Profit by Year', fontweight='bold')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Amount ($)')
    axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    axes[0].legend()
    axes[0].set_xticks(x)

    # Orders
    axes[1].bar(x, yearly['Orders'], color=COLORS['info'], alpha=0.85)
    axes[1].set_title('Total Orders by Year', fontweight='bold')
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('Number of Orders')
    axes[1].set_xticks(x)

    plt.tight_layout()
    save_chart(fig, '10_yoy_growth.png')


# ─────────────────────────────────────────────────────────────
# VISUALIZATION 11: Customer Revenue Concentration
# Business Q: How concentrated is revenue among top customers?
# ─────────────────────────────────────────────────────────────
def plot_customer_concentration(df):
    """Revenue concentration — Pareto analysis of customers."""
    print("[11] Customer Revenue Concentration")

    customer_rev = (df.groupby('Customer Name')['Revenue'].sum()
                    .sort_values(ascending=False))
    cum_pct = customer_rev.cumsum() / customer_rev.sum() * 100
    customer_pct = np.arange(1, len(customer_rev) + 1) / len(customer_rev) * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(customer_pct, cum_pct, color=COLORS['primary'], linewidth=2)
    ax.fill_between(customer_pct, cum_pct, alpha=0.1, color=COLORS['primary'])

    # Mark 80% revenue line
    ax.axhline(y=80, color=COLORS['danger'], linewidth=1, linestyle='--',
               label='80% Revenue')
    # Find what % of customers produce 80% of revenue
    pct_at_80 = customer_pct[np.argmax(cum_pct >= 80)]
    ax.axvline(x=pct_at_80, color=COLORS['warning'], linewidth=1, linestyle='--',
               label=f'{pct_at_80:.0f}% of Customers')

    ax.set_title('Customer Revenue Concentration (Pareto)', fontweight='bold')
    ax.set_xlabel('% of Customers')
    ax.set_ylabel('% of Revenue (Cumulative)')
    ax.legend()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 105)

    plt.tight_layout()
    save_chart(fig, '11_customer_concentration.png')


# ─────────────────────────────────────────────────────────────
# VISUALIZATION 12: Profit Margin by Sub-Category (Heatmap style)
# Business Q: Which sub-categories lose money?
# ─────────────────────────────────────────────────────────────
def plot_category_subcategory_heatmap(df):
    """Profit margin heatmap by category and sub-category."""
    print("[12] Category × Sub-Category Profit Margin")

    pivot = df.pivot_table(
        values='Profit Margin',
        index='Sub-Category',
        columns='Category',
        aggfunc='mean'
    ).round(1)

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn', center=0,
                linewidths=0.5, ax=ax, cbar_kws={'label': 'Avg Profit Margin (%)'})
    ax.set_title('Average Profit Margin (%) by Sub-Category and Category',
                 fontweight='bold')
    plt.tight_layout()
    save_chart(fig, '12_profit_margin_heatmap.png')


def main():
    """Run all EDA visualizations."""
    print("=" * 70)
    print("  RETAIL SALES & CUSTOMER ANALYTICS — EXPLORATORY DATA ANALYSIS")
    print("=" * 70)

    df = load_data()
    ensure_charts_dir()

    print("\nGenerating visualizations...\n")

    plot_monthly_revenue_trend(df)
    plot_monthly_profit_trend(df)
    plot_revenue_by_category(df)
    plot_subcategory_performance(df)
    plot_regional_performance(df)
    plot_top_products(df)
    plot_top_customers(df)
    plot_discount_vs_profit(df)
    plot_seasonal_patterns(df)
    plot_yoy_growth(df)
    plot_customer_concentration(df)
    plot_category_subcategory_heatmap(df)

    print("\n" + "=" * 70)
    print(f"  EDA COMPLETE — {12} visualizations saved to {CHARTS_DIR}")
    print("=" * 70)


if __name__ == '__main__':
    main()
