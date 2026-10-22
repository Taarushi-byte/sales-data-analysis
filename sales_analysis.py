import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load the sample sales dataset
DATA_FILE = Path(__file__).with_name("sales_data.csv")
OUTPUT_DIR = Path(__file__).parent

df = pd.read_csv(DATA_FILE)

# Validate and prepare the data
required_columns = {
    "order_id", "order_date", "product",
    "category", "quantity", "unit_price"
}

missing_columns = required_columns - set(df.columns)
if missing_columns:
    raise ValueError(f"Missing columns: {sorted(missing_columns)}")

df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

df = df.dropna(subset=[
    "order_id", "order_date", "product",
    "category", "quantity", "unit_price"
])

df = df[(df["quantity"] >= 0) & (df["unit_price"] >= 0)]
df["revenue"] = df["quantity"] * df["unit_price"]

# Calculate summary metrics
total_revenue = df["revenue"].sum()
total_orders = df["order_id"].nunique()
total_units = df["quantity"].sum()
average_order_value = (
    total_revenue / total_orders if total_orders else 0
)

monthly_sales = (
    df.groupby(df["order_date"].dt.to_period("M"))["revenue"]
    .sum()
    .sort_index()
)

product_sales = (
    df.groupby("product")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

category_sales = (
    df.groupby("category")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("=" * 45)
print("SALES ANALYSIS REPORT")
print("=" * 45)
print(f"Total revenue: ₹{total_revenue:,.2f}")
print(f"Unique orders: {total_orders}")
print(f"Units sold: {total_units:,.0f}")
print(f"Average revenue per order: ₹{average_order_value:,.2f}")

print("\nRevenue by product:")
print(product_sales.to_string())

print("\nRevenue by category:")
print(category_sales.to_string())

print("\nMonthly revenue:")
print(monthly_sales.to_string())

# Export analysis results
df.to_csv(OUTPUT_DIR / "sales_analysis.csv", index=False)
product_sales.rename("revenue").to_csv(
    OUTPUT_DIR / "product_sales.csv"
)

monthly_sales.rename("revenue").to_csv(
    OUTPUT_DIR / "monthly_sales.csv"
)

# Chart 1: Monthly revenue
monthly_labels = monthly_sales.index.astype(str)

plt.figure(figsize=(10, 5))
plt.plot(monthly_labels, monthly_sales.values, marker="o")
plt.title("Monthly Sales Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "monthly_revenue.png", dpi=150)
plt.close()

# Chart 2: Product revenue
plt.figure(figsize=(9, 5))
product_sales.sort_values().plot(kind="barh")
plt.title("Revenue by Product")
plt.xlabel("Revenue (₹)")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "product_revenue.png", dpi=150)
plt.close()

# Chart 3: Category revenue
plt.figure(figsize=(7, 5))
category_sales.plot(kind="bar")
plt.title("Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "category_revenue.png", dpi=150)
plt.close()

print("\nAnalysis completed successfully.")
print("CSV reports and charts have been saved.")
print("Dataset contains fictional demonstration data.")
