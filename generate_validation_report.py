import pandas as pd

def audit_inventory(file_path):
    # load the data
    df = pd.read_csv(file_path)

    print(f"---Starting Audit for {file_path} ---")

    # 1. Find Duplicates
    duplicates = df[df.duplicated()]

    # 2. Find Missing Values (Nulls)
    # .any(axis=1) finds rows where at least one column is NaN
    missing_data =df[df.isnull().any(axis=1)]


    # 3. Find Logical Outliers (Prices > $1000 or Stock < 0)
    # This is like an 'if' statement for the whole table
    price_outliers = df[df['Price'] > 1000]
    negative_stock = df[df['Stock_Count'] < 0]

    # 4. Find Inconsistent Casing in Categories
    # We find unique values to see if 'Cutting' and 'cutting' both exist
    category_counts = df['Category'].value_counts()


    # --- REPORTING ---

    print(f"Total Rows Scanned: {len(df)}")
    print(f"⚠️ Duplicates Found: {len(duplicates)}")
    print(f"⚠️ Rows with Missing Values: {len(missing_data)}")
    print(f"⚠️ Price Outliers: {len(price_outliers)}")
    print(f"⚠️ Negative Stock Issues: {len(negative_stock)}")

    print("\nInconsistent Categories Detected:")
    print(category_counts)

    return {
        "duplicates": duplicates,
        "missing": missing_data,
        "outliers": price_outliers,
        "negative_stocks": negative_stock,
        "category_counts": category_counts

    }


# Run the audit
# report = audit_inventory('messy_surgical_inventory.csv')
