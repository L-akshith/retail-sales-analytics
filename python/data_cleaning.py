"""
Data Cleaning Script for Retail Sales Analytics
=================================================
This script performs comprehensive data cleaning on the Sample Superstore dataset.

Steps performed:
1. Load raw data
2. Missing value analysis
3. Duplicate detection and removal
4. Data type correction and date conversion
5. Invalid value detection
6. Outlier investigation (with business justification for decisions)
7. Standardization of categorical fields
8. Creation of calculated columns
9. Export cleaned dataset

Author: Laksh (Portfolio Project)
Dataset: Sample Superstore (Kaggle / GitHub)
"""

import pandas as pd
import numpy as np
import os
import sys
import warnings

warnings.filterwarnings('ignore')


# ─────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────
RAW_DATA_PATH = os.path.join('..', 'data', 'raw', 'superstore_raw.csv')
PROCESSED_DATA_PATH = os.path.join('..', 'data', 'processed', 'cleaned_sales.csv')
CLEANING_REPORT_PATH = os.path.join('..', 'data', 'processed', 'cleaning_report.txt')


def load_raw_data(filepath):
    """Load the raw Superstore CSV dataset."""
    print("=" * 70)
    print("STEP 1: LOADING RAW DATA")
    print("=" * 70)

    df = pd.read_csv(filepath, encoding='latin-1')
    print(f"  Loaded {len(df)} rows and {df.shape[1]} columns.")
    print(f"  Columns: {list(df.columns)}")
    print(f"  Memory usage: {df.memory_usage(deep=True).sum() / 1024:.1f} KB")
    return df


def analyze_missing_values(df):
    """Analyze and report missing values across all columns."""
    print("\n" + "=" * 70)
    print("STEP 2: MISSING VALUE ANALYSIS")
    print("=" * 70)

    missing = df.isnull().sum()
    missing_pct = (df.isnull().sum() / len(df)) * 100

    missing_report = pd.DataFrame({
        'Missing Count': missing,
        'Missing %': missing_pct.round(2)
    })

    print(missing_report.to_string())

    total_missing = missing.sum()
    if total_missing == 0:
        print("\n  ✓ No missing values found in the dataset.")
    else:
        print(f"\n  ⚠ Total missing values: {total_missing}")

    # Drop rows where critical business columns are all NaN
    # These are empty/padding rows from the CSV and not real transactions
    critical_cols = ['Order ID', 'Customer ID', 'Sales', 'Profit']
    existing_critical = [c for c in critical_cols if c in df.columns]
    before = len(df)
    df = df.dropna(subset=existing_critical, how='any').reset_index(drop=True)
    dropped = before - len(df)
    if dropped > 0:
        print(f"  Dropped {dropped} rows with missing critical fields "
              f"(Order ID, Customer ID, Sales, Profit).")
        print(f"  Rows remaining: {len(df)}")

    # Re-check after dropping
    remaining_missing = df.isnull().sum().sum()
    if remaining_missing > 0:
        print(f"  Remaining missing values after cleanup: {remaining_missing}")
    else:
        print("  ✓ No missing values remain after cleanup.")

    return df


def detect_and_remove_duplicates(df):
    """Detect and remove duplicate rows."""
    print("\n" + "=" * 70)
    print("STEP 3: DUPLICATE DETECTION AND REMOVAL")
    print("=" * 70)

    # Check for fully duplicate rows
    full_duplicates = df.duplicated().sum()
    print(f"  Fully duplicate rows: {full_duplicates}")

    if full_duplicates > 0:
        print(f"  Removing {full_duplicates} fully duplicate rows.")
        df = df.drop_duplicates().reset_index(drop=True)
        print(f"  Rows after removal: {len(df)}")
    else:
        print("  ✓ No fully duplicate rows found.")

    # Check for duplicate Row IDs (should be unique per row)
    if 'Row ID' in df.columns:
        dup_row_ids = df['Row ID'].duplicated().sum()
        print(f"  Duplicate Row IDs: {dup_row_ids}")
        if dup_row_ids > 0:
            df = df.drop_duplicates(subset=['Row ID'], keep='first').reset_index(drop=True)
            print(f"  Removed duplicate Row IDs. Rows remaining: {len(df)}")

    return df


def correct_data_types(df):
    """Correct data types and convert dates."""
    print("\n" + "=" * 70)
    print("STEP 4: DATA TYPE CORRECTION & DATE CONVERSION")
    print("=" * 70)

    # Convert date columns
    date_columns = ['Order Date', 'Ship Date']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format='mixed', dayfirst=False)
            print(f"  Converted '{col}' to datetime. Range: {df[col].min()} to {df[col].max()}")

    # Ensure numeric columns are correct types
    numeric_cols = ['Sales', 'Quantity', 'Discount', 'Profit']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            print(f"  '{col}' dtype: {df[col].dtype}")

    # Postal Code should be string (leading zeros matter)
    if 'Postal Code' in df.columns:
        df['Postal Code'] = df['Postal Code'].fillna(0).astype(int).astype(str)
        print(f"  Converted 'Postal Code' to string.")

    print("\n  Data types after correction:")
    print(df.dtypes.to_string())

    return df


def detect_invalid_values(df):
    """Detect and flag invalid or suspicious values."""
    print("\n" + "=" * 70)
    print("STEP 5: INVALID VALUE DETECTION")
    print("=" * 70)

    issues = []

    # Check for negative quantities
    if 'Quantity' in df.columns:
        neg_qty = (df['Quantity'] <= 0).sum()
        if neg_qty > 0:
            issues.append(f"  ⚠ {neg_qty} rows with non-positive Quantity")
            # These likely represent returns — flag but keep
            print(f"  ⚠ {neg_qty} rows with Quantity ≤ 0 (potential returns — retained)")
        else:
            print(f"  ✓ All Quantity values are positive.")

    # Check for negative sales
    if 'Sales' in df.columns:
        neg_sales = (df['Sales'] < 0).sum()
        if neg_sales > 0:
            issues.append(f"  ⚠ {neg_sales} rows with negative Sales")
            print(f"  ⚠ {neg_sales} rows with negative Sales (returns/refunds — retained)")
        else:
            print(f"  ✓ All Sales values are non-negative.")

    # Check discount range (should be 0 to 1 or 0 to 100)
    if 'Discount' in df.columns:
        max_discount = df['Discount'].max()
        min_discount = df['Discount'].min()
        print(f"  Discount range: {min_discount} to {max_discount}")
        if max_discount > 1:
            print("  Note: Discounts appear to be in percentage form (0-100).")
        else:
            print("  ✓ Discounts are in decimal form (0-1).")

        invalid_discount = ((df['Discount'] < 0) | (df['Discount'] > 1)).sum()
        if invalid_discount > 0 and max_discount <= 1:
            print(f"  ⚠ {invalid_discount} rows with discount outside 0-1 range.")

    # Check date logic: Ship Date should be >= Order Date
    if 'Order Date' in df.columns and 'Ship Date' in df.columns:
        date_issues = (df['Ship Date'] < df['Order Date']).sum()
        if date_issues > 0:
            print(f"  ⚠ {date_issues} rows where Ship Date is before Order Date!")
            issues.append(f"  {date_issues} rows with Ship Date < Order Date")
        else:
            print(f"  ✓ All Ship Dates are on or after Order Dates.")

    if not issues:
        print("\n  ✓ No critical data integrity issues detected.")

    return df


def investigate_outliers(df):
    """
    Investigate outliers using IQR method.
    Business justification: We do NOT blindly remove outliers.
    Large sales/profit values can represent bulk B2B orders.
    Negative profits are legitimate (discounted or loss-leader products).
    """
    print("\n" + "=" * 70)
    print("STEP 6: OUTLIER INVESTIGATION")
    print("=" * 70)

    numeric_cols = ['Sales', 'Quantity', 'Discount', 'Profit']
    for col in numeric_cols:
        if col not in df.columns:
            continue

        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = ((df[col] < lower) | (df[col] > upper)).sum()
        pct = (outliers / len(df)) * 100

        print(f"\n  {col}:")
        print(f"    Q1={Q1:.2f}, Q3={Q3:.2f}, IQR={IQR:.2f}")
        print(f"    Lower bound: {lower:.2f}, Upper bound: {upper:.2f}")
        print(f"    Outliers: {outliers} ({pct:.1f}%)")

    print("\n  DECISION: Outliers are RETAINED.")
    print("  RATIONALE:")
    print("    - High Sales values are legitimate bulk/corporate orders.")
    print("    - Negative Profit values are real business losses from discounts.")
    print("    - Removing them would misrepresent business reality.")
    print("    - For a consulting engagement, understanding extreme values is crucial.")

    return df


def standardize_categorical_fields(df):
    """Standardize categorical fields for consistency."""
    print("\n" + "=" * 70)
    print("STEP 7: STANDARDIZE CATEGORICAL FIELDS")
    print("=" * 70)

    categorical_cols = ['Ship Mode', 'Segment', 'Country', 'City', 'State',
                        'Region', 'Category', 'Sub-Category']

    for col in categorical_cols:
        if col not in df.columns:
            continue

        # Strip whitespace
        df[col] = df[col].astype(str).str.strip()

        # Title case for consistency (except short codes)
        unique_count = df[col].nunique()
        print(f"  {col}: {unique_count} unique values")

        # Show value counts for key fields
        if unique_count <= 10:
            vals = [v for v in df[col].unique() if pd.notna(v)]
            print(f"    Values: {sorted(vals)}")

    return df


def create_calculated_columns(df):
    """Create business-relevant calculated columns."""
    print("\n" + "=" * 70)
    print("STEP 8: CREATE CALCULATED COLUMNS")
    print("=" * 70)

    # Revenue (same as Sales in this dataset, but explicit)
    df['Revenue'] = df['Sales']
    print("  ✓ Created 'Revenue' (= Sales)")

    # Profit Margin (%)
    df['Profit Margin'] = np.where(
        df['Sales'] != 0,
        (df['Profit'] / df['Sales']) * 100,
        0
    )
    print("  ✓ Created 'Profit Margin' (%)")

    # Order Month and Year
    df['Order Month'] = df['Order Date'].dt.month
    df['Order Year'] = df['Order Date'].dt.year
    df['Order Month Name'] = df['Order Date'].dt.strftime('%B')
    df['Order Quarter'] = df['Order Date'].dt.quarter
    df['Order Year-Month'] = df['Order Date'].dt.to_period('M').astype(str)
    print("  ✓ Created 'Order Month', 'Order Year', 'Order Month Name', "
          "'Order Quarter', 'Order Year-Month'")

    # Shipping Duration (days)
    df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
    print("  ✓ Created 'Shipping Days'")

    # Discount Flag
    df['Has Discount'] = (df['Discount'] > 0).astype(int)
    print("  ✓ Created 'Has Discount' (binary flag)")

    # Profit Flag
    df['Is Profitable'] = (df['Profit'] > 0).astype(int)
    print("  ✓ Created 'Is Profitable' (binary flag)")

    print(f"\n  Final column count: {df.shape[1]}")
    print(f"  New columns added: Revenue, Profit Margin, Order Month, Order Year,")
    print(f"    Order Month Name, Order Quarter, Order Year-Month, Shipping Days,")
    print(f"    Has Discount, Is Profitable")

    return df


def generate_cleaning_summary(df, report_path):
    """Generate a summary report of the cleaned dataset."""
    print("\n" + "=" * 70)
    print("STEP 9: CLEANING SUMMARY")
    print("=" * 70)

    summary_lines = [
        "RETAIL SALES DATA CLEANING REPORT",
        "=" * 50,
        f"Date: Generated by data_cleaning.py",
        f"Source: Sample Superstore Dataset (GitHub/Kaggle)",
        "",
        f"Total rows: {len(df)}",
        f"Total columns: {df.shape[1]}",
        f"Date range: {df['Order Date'].min().strftime('%Y-%m-%d')} to "
        f"{df['Order Date'].max().strftime('%Y-%m-%d')}",
        f"Unique orders: {df['Order ID'].nunique()}",
        f"Unique customers: {df['Customer ID'].nunique()}",
        f"Unique products: {df['Product ID'].nunique()}",
        "",
        "NUMERIC SUMMARY:",
        "-" * 50,
    ]

    # Add numeric summary
    numeric_summary = df[['Sales', 'Quantity', 'Discount', 'Profit',
                          'Profit Margin']].describe().round(2)
    summary_lines.append(numeric_summary.to_string())
    summary_lines.append("")
    summary_lines.append("CATEGORY DISTRIBUTION:")
    summary_lines.append("-" * 50)
    summary_lines.append(df['Category'].value_counts().to_string())
    summary_lines.append("")
    summary_lines.append("REGION DISTRIBUTION:")
    summary_lines.append("-" * 50)
    summary_lines.append(df['Region'].value_counts().to_string())

    report_text = "\n".join(summary_lines)
    print(report_text)

    # Save report
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    print(f"\n  ✓ Cleaning report saved to: {report_path}")


def save_cleaned_data(df, filepath):
    """Save the cleaned dataset to CSV."""
    print("\n" + "=" * 70)
    print("STEP 10: SAVE CLEANED DATASET")
    print("=" * 70)

    df.to_csv(filepath, index=False, encoding='utf-8')
    file_size = os.path.getsize(filepath) / 1024
    print(f"  ✓ Cleaned dataset saved to: {filepath}")
    print(f"  File size: {file_size:.1f} KB")
    print(f"  Rows: {len(df)}, Columns: {df.shape[1]}")


def main():
    """Main data cleaning pipeline."""
    print("\n" + "█" * 70)
    print("  RETAIL SALES & CUSTOMER ANALYTICS — DATA CLEANING PIPELINE")
    print("█" * 70 + "\n")

    # Step 1: Load
    df = load_raw_data(RAW_DATA_PATH)

    # Step 2: Missing values
    df = analyze_missing_values(df)

    # Step 3: Duplicates
    df = detect_and_remove_duplicates(df)

    # Step 4: Data types
    df = correct_data_types(df)

    # Step 5: Invalid values
    df = detect_invalid_values(df)

    # Step 6: Outliers
    df = investigate_outliers(df)

    # Step 7: Standardize
    df = standardize_categorical_fields(df)

    # Step 8: Calculated columns
    df = create_calculated_columns(df)

    # Step 9: Summary
    generate_cleaning_summary(df, CLEANING_REPORT_PATH)

    # Step 10: Save
    save_cleaned_data(df, PROCESSED_DATA_PATH)

    print("\n" + "█" * 70)
    print("  DATA CLEANING COMPLETE!")
    print("█" * 70 + "\n")

    return df


if __name__ == '__main__':
    main()
