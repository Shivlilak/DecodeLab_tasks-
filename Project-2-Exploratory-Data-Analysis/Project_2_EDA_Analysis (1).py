"""
==================================================================================
 Project 2 - Exploratory Data Analysis (EDA)
 DecodeLabs Data Analytics Internship | Batch 2026
==================================================================================
 Goal (from the Project 2 brief):
    Analyze a dataset to understand patterns, trends, and distributions.

 This script:
    1. Loads the cleaned dataset produced in Project 1.
    2. Gives a dataset overview (shape, data types, missing values).
    3. Calculates basic statistics (count, mean, median, std, quartiles).
    4. Analyzes frequency distributions of categorical columns.
    5. Analyzes trends over time (monthly orders & revenue).
    6. Detects outliers using the IQR method.
    7. Calculates correlations between numeric variables.
    8. Compares categorical vs numerical variables (e.g. revenue by product).
    9. Saves charts as PNG files and prints a plain-English summary.

 Beginner notes are included as comments throughout.
==================================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ----------------------------------------------------------------------------
# 0. SETTINGS
# ----------------------------------------------------------------------------
INPUT_FILE = "cleaned_dataset.xlsx"     # <-- cleaned dataset from Project 1
CHART_FOLDER = "charts"                 # folder where PNG charts will be saved
pd.set_option("display.width", 120)
pd.set_option("display.max_columns", None)
sns.set_style("whitegrid")
os.makedirs(CHART_FOLDER, exist_ok=True)


def save_chart(fig, filename):
    """Helper: saves a matplotlib figure to the charts folder and closes it."""
    path = os.path.join(CHART_FOLDER, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  -> saved chart: {path}")


# ----------------------------------------------------------------------------
# 1. LOAD THE CLEANED DATASET
# ----------------------------------------------------------------------------
print("=" * 70)
print("STEP 1: Loading the cleaned dataset")
print("=" * 70)

df = pd.read_excel(INPUT_FILE)
df["Date"] = pd.to_datetime(df["Date"])   # make sure Date is a real datetime
N_COLS_ORIGINAL = df.shape[1]              # remember original column count (before any helper columns are added)

print(f"Loaded '{INPUT_FILE}' successfully.")
print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns\n")


# ----------------------------------------------------------------------------
# 2. DATASET OVERVIEW
# ----------------------------------------------------------------------------
print("=" * 70)
print("STEP 2: Dataset Overview")
print("=" * 70)

print("\nColumn data types:")
print(df.dtypes)

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values per column:")
print(df.isnull().sum())

print(f"\nFully duplicated rows: {df.duplicated().sum()}")
print(f"Unique OrderIDs: {df['OrderID'].nunique()}  |  Unique CustomerIDs: {df['CustomerID'].nunique()}")
print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}\n")


# ----------------------------------------------------------------------------
# 3. DESCRIPTIVE STATISTICS (Count, Mean, Median, etc.)
# ----------------------------------------------------------------------------
print("=" * 70)
print("STEP 3: Descriptive Statistics (Numeric Columns)")
print("=" * 70)

numeric_cols = ["Quantity", "UnitPrice", "ItemsInCart", "TotalPrice"]

# .describe() gives count, mean, std, min, 25%, 50% (median), 75%, max in one call
desc_stats = df[numeric_cols].describe().T
desc_stats["median"] = df[numeric_cols].median()   # explicit median column, as required by the brief
print(desc_stats.round(2))
print()

for col in numeric_cols:
    print(f"{col}: count={df[col].count()}, mean={df[col].mean():.2f}, median={df[col].median():.2f}")
print()


# ----------------------------------------------------------------------------
# 4. FREQUENCY DISTRIBUTION (Categorical Columns)
# ----------------------------------------------------------------------------
print("=" * 70)
print("STEP 4: Frequency Distribution (Categorical Columns)")
print("=" * 70)

categorical_cols = ["Product", "PaymentMethod", "OrderStatus", "ReferralSource", "CouponCode"]

for col in categorical_cols:
    print(f"\n--- {col} ---")
    counts = df[col].value_counts(dropna=False)
    pct = (counts / len(df) * 100).round(1)
    print(pd.DataFrame({"Count": counts, "Percent": pct}))

    fig, ax = plt.subplots(figsize=(7, 4))
    counts.plot(kind="bar", ax=ax, color="#4C72B0")
    ax.set_title(f"Order Count by {col}")
    ax.set_xlabel(col)
    ax.set_ylabel("Number of Orders")
    plt.xticks(rotation=30, ha="right")
    save_chart(fig, f"freq_{col}.png")

print()


# ----------------------------------------------------------------------------
# 5. DISTRIBUTION ANALYSIS (histograms for numeric columns)
# ----------------------------------------------------------------------------
print("=" * 70)
print("STEP 5: Distribution Analysis (Numeric Columns)")
print("=" * 70)

for col in numeric_cols:
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.histplot(df[col], kde=True, ax=ax, color="#55A868")
    ax.axvline(df[col].mean(), color="red", linestyle="--", label=f"Mean = {df[col].mean():.2f}")
    ax.axvline(df[col].median(), color="black", linestyle="-", label=f"Median = {df[col].median():.2f}")
    ax.set_title(f"Distribution of {col}")
    ax.set_xlabel(col)
    ax.set_ylabel("Frequency")
    ax.legend()
    save_chart(fig, f"distribution_{col}.png")

# Skewness tells us if the mean is being pulled away from the median
print("\nSkewness (0 = symmetric, >0 = right-skewed / long tail on the high side):")
print(df[numeric_cols].skew().round(2))
print()


# ----------------------------------------------------------------------------
# 6. TREND ANALYSIS (Orders & Revenue over time)
# ----------------------------------------------------------------------------
print("=" * 70)
print("STEP 6: Trend Analysis (Monthly Orders & Revenue)")
print("=" * 70)

df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)
monthly = df.groupby("YearMonth").agg(
    Orders=("OrderID", "count"),
    Revenue=("TotalPrice", "sum")
).reset_index()
monthly["AvgOrderValue"] = monthly["Revenue"] / monthly["Orders"]

print(monthly.to_string(index=False))

fig, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(monthly["YearMonth"], monthly["Orders"], marker="o", color="#4C72B0")
ax1.set_title("Monthly Order Count Trend")
ax1.set_xlabel("Month")
ax1.set_ylabel("Number of Orders")
plt.xticks(rotation=90)
save_chart(fig, "trend_monthly_orders.png")

fig, ax2 = plt.subplots(figsize=(12, 5))
ax2.plot(monthly["YearMonth"], monthly["Revenue"], marker="o", color="#C44E52")
ax2.set_title("Monthly Revenue Trend")
ax2.set_xlabel("Month")
ax2.set_ylabel("Revenue")
plt.xticks(rotation=90)
save_chart(fig, "trend_monthly_revenue.png")
print()


# ----------------------------------------------------------------------------
# 7. OUTLIER DETECTION (IQR Method)
# ----------------------------------------------------------------------------
print("=" * 70)
print("STEP 7: Outlier Detection (IQR Method)")
print("=" * 70)
print("Rule: a value is an outlier if it is below (Q1 - 1.5*IQR) or above (Q3 + 1.5*IQR)\n")

outlier_summary = []
for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    outlier_summary.append({
        "Column": col, "Q1": Q1, "Q3": Q3, "IQR": IQR,
        "LowerBound": lower_bound, "UpperBound": upper_bound,
        "OutlierCount": len(outliers)
    })
    print(f"{col}: Q1={Q1:.2f}, Q3={Q3:.2f}, IQR={IQR:.2f}, "
          f"bounds=({lower_bound:.2f}, {upper_bound:.2f}), outliers found = {len(outliers)}")

outlier_summary_df = pd.DataFrame(outlier_summary)

# Boxplots make outliers easy to see visually
fig, axes = plt.subplots(1, len(numeric_cols), figsize=(16, 5))
for ax, col in zip(axes, numeric_cols):
    sns.boxplot(y=df[col], ax=ax, color="#8172B2")
    ax.set_title(col)
fig.suptitle("Boxplots - Outlier Detection")
save_chart(fig, "outliers_boxplots.png")

# Show the actual TotalPrice outlier rows (the column with the most outliers)
Q1 = df["TotalPrice"].quantile(0.25)
Q3 = df["TotalPrice"].quantile(0.75)
IQR = Q3 - Q1
tp_outliers = df[(df["TotalPrice"] < Q1 - 1.5 * IQR) | (df["TotalPrice"] > Q3 + 1.5 * IQR)]
print(f"\nTotalPrice outlier records ({len(tp_outliers)} rows):")
print(tp_outliers[["OrderID", "Date", "Product", "Quantity", "UnitPrice", "TotalPrice", "OrderStatus"]]
      .sort_values("TotalPrice", ascending=False).to_string(index=False))
print()


# ----------------------------------------------------------------------------
# 8. CORRELATION ANALYSIS
# ----------------------------------------------------------------------------
print("=" * 70)
print("STEP 8: Correlation Analysis")
print("=" * 70)

corr_matrix = df[numeric_cols].corr()
print(corr_matrix.round(2))

fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
ax.set_title("Correlation Heatmap - Numeric Variables")
save_chart(fig, "correlation_heatmap.png")

fig, ax = plt.subplots(figsize=(6, 5))
ax.scatter(df["UnitPrice"], df["TotalPrice"], alpha=0.4, color="#4C72B0")
ax.set_title("UnitPrice vs TotalPrice")
ax.set_xlabel("UnitPrice")
ax.set_ylabel("TotalPrice")
save_chart(fig, "scatter_unitprice_totalprice.png")
print()


# ----------------------------------------------------------------------------
# 9. CATEGORICAL vs NUMERICAL COMPARISONS
# ----------------------------------------------------------------------------
print("=" * 70)
print("STEP 9: Categorical vs Numerical Comparisons")
print("=" * 70)

for col in ["Product", "OrderStatus", "PaymentMethod", "ReferralSource"]:
    summary = df.groupby(col)["TotalPrice"].agg(
        OrderCount="count", TotalRevenue="sum", AvgOrderValue="mean", MedianOrderValue="median"
    ).round(2).sort_values("TotalRevenue", ascending=False)
    print(f"\nTotalPrice by {col}:")
    print(summary)

    fig, ax = plt.subplots(figsize=(7, 4))
    summary["AvgOrderValue"].plot(kind="bar", ax=ax, color="#DD8452")
    ax.set_title(f"Average Order Value by {col}")
    ax.set_xlabel(col)
    ax.set_ylabel("Avg Order Value")
    plt.xticks(rotation=30, ha="right")
    save_chart(fig, f"avg_order_value_by_{col}.png")

print()


# ----------------------------------------------------------------------------
# 10. KEY OBSERVATIONS (printed summary)
# ----------------------------------------------------------------------------
print("=" * 70)
print("STEP 10: Key Observations")
print("=" * 70)

print(f"""
1. Dataset: {len(df)} orders, {N_COLS_ORIGINAL} columns, {df['Date'].min().date()} to {df['Date'].max().date()}.
   Only CouponCode has missing values ({df['CouponCode'].isnull().sum()} rows) - this simply means
   no coupon was used, not a data quality problem.

2. TotalPrice is right-skewed: mean (${df['TotalPrice'].mean():.2f}) > median (${df['TotalPrice'].median():.2f}).
   Use the median as the "typical order value" for reporting.

3. Quantity and ItemsInCart are close to uniformly distributed within their ranges
   (Quantity: 1-5, ItemsInCart: 1-10) - mean and median are close.

4. {len(tp_outliers)} orders ({len(tp_outliers)/len(df):.1%}) are TotalPrice outliers (IQR method) -
   all high-value orders combining above-average Quantity and UnitPrice. No outliers were
   found in Quantity, UnitPrice or ItemsInCart alone.

5. Monthly order volume fluctuates between ~27 and ~53 orders with no strong long-term trend.

6. Correlations: UnitPrice-TotalPrice (r={corr_matrix.loc['UnitPrice','TotalPrice']:.2f}) and
   Quantity-TotalPrice (r={corr_matrix.loc['Quantity','TotalPrice']:.2f}) are the strongest
   relationships, as expected since TotalPrice = Quantity x UnitPrice. UnitPrice and Quantity
   themselves are essentially uncorrelated (r={corr_matrix.loc['UnitPrice','Quantity']:.2f}).

7. Average order value is broadly similar (roughly $970-$1,130) across Product, PaymentMethod,
   OrderStatus and ReferralSource segments - order value is not strongly driven by any single
   categorical attribute in this dataset.
""")

print(f"All charts saved to the '{CHART_FOLDER}/' folder.")
print("EDA complete.")
