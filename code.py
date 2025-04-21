import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("retail_store_sales.csv")
#Basic Exploration
df.head(5)
df.isnull().sum()
df.info()
df.describe()

# -------------------- GENERAL CLEANING -------------------- #

# Display original columns
print("Columns in the dataset:")
print(df.columns.tolist(), "\n")

# Convert date column if exists
if 'Transaction Date' in df.columns:
    df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], errors='coerce')

# Handle missing values with logic
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].fillna("Unknown")
    elif np.issubdtype(df[col].dtype, np.number):
        df[col] = df[col].fillna(df[col].median())

# Recalculate missing 'Total Spent' if 'Price' and 'Quantity' exist
if {'Price', 'Quantity'}.issubset(df.columns):
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    df['Total Spent'] = pd.to_numeric(df.get('Total Spent', df['Price'] * df['Quantity']), errors='coerce')
    df['Total Spent'] = df['Price'] * df['Quantity']

# Drop invalid or zero values
for col in ['Price', 'Quantity', 'Total Spent']:
    if col in df.columns:
        df = df[df[col] > 0]


#check for null
df.isnull().sum()
df.info()

# -------------------- STATISTICAL EDA -------------------- #

print("\n === STATISTICAL EDA ===\n")

# Total Revenue
if 'Total Spent' in df.columns:
    print(f"Total Revenue: ₹{df['Total Spent'].sum():,.2f}")
    print(f"Average Transaction Value: ₹{df['Total Spent'].mean():.2f}")

# Most Purchased Item
if {'Item', 'Quantity'}.issubset(df.columns):
    item_qty = df.groupby('Item')['Quantity'].sum()
    top_item = item_qty.idxmax()
    print(f"Most Purchased Item: {top_item} ({item_qty.max()} units)")

# Top Revenue Generating Item
if {'Item', 'Total Spent'}.issubset(df.columns):
    item_rev = df.groupby('Item')['Total Spent'].sum()
    top_rev_item = item_rev.idxmax()
    print(f"Top Revenue Item: {top_rev_item} (₹{item_rev.max():,.2f})")

# Top 5 Categories by Revenue
if {'Category', 'Total Spent'}.issubset(df.columns):
    print("\nTop Categories by Revenue:")
    print(df.groupby('Category')['Total Spent'].sum().sort_values(ascending=False).head(5))

# Payment Method distribution
if 'Payment Method' in df.columns:
    print("\nPayment Method Usage:")
    print(df['Payment Method'].value_counts())

# Discount impact
if {'Discount Applied', 'Total Spent'}.issubset(df.columns):
    print("\n Avg Spend (with Discount): ₹", df[df['Discount Applied'] == True]['Total Spent'].mean())
    print("Avg Spend (without Discount): ₹", df[df['Discount Applied'] == False]['Total Spent'].mean())

# Yearly sales trend
if 'Transaction Date' in df.columns:
    df['Year'] = df['Transaction Date'].dt.year
    print("\n Sales by Year:")
    print(df.groupby('Year')['Total Spent'].sum())

# Customer insights
if {'Customer ID', 'Total Spent'}.issubset(df.columns):
    print("\n Top 5 Customers by Spend:")
    print(df.groupby('Customer ID')['Total Spent'].sum().sort_values(ascending=False).head(5))

# Store/Location performance
if {'Location', 'Total Spent'}.issubset(df.columns):
    print("\nTop Locations by Revenue:")
    print(df.groupby('Location')['Total Spent'].sum().sort_values(ascending=False).head(5))
