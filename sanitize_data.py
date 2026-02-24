import pandas as pd
from generate_validation_report import audit_inventory
import datetime
import os

def sanitize_data(file_path):
    # 1. Load data
    df = pd.read_csv(file_path)

    print("--- Start sanitizing data ---")

    # 2. Get audit report (optional, but good for logs)
    # report = audit_inventory(file_path)

    # 3. Clean Casing & Whitespace (Crucial for Surgical Labs!)
    # This fixes "Grasping " and "grasping" automatically
    df['Category'] = df['Category'].str.strip().str.title()
    df['Product_Name'] = df['Product_Name'].str.strip()

    # 4. Drop Duplicates
    df = df.drop_duplicates()

    # 5. Drop Null Values
    df = df.dropna(subset=['Price', 'Stock_Count'])

    # 6. Filter Outliers (Note the parentheses and the & symbol)
    # This keeps only the rows that meet ALL criteria
    df = df[(df['Price'] > 0) & (df['Price'] < 1000)]
    df = df[df['Stock_Count'] >= 0]

    # 7. Save the clean file
    clean_file = "data/cleaned_surgical_inventory.csv"
    df.to_csv(clean_file, index=False)

    print(f"Sanitization complete! Saved to {clean_file}")
    print(f"Rows remaining: {len(df)}")
    return df

def interactive_sanitize(file_path):
    df = pd.read_csv(file_path)

    # --- STEP 1: Normalization (Crucial!) ---
    # We do this FIRST so duplicates and grouping are accurate
    df['Category'] = df['Category'].str.strip().str.title()
    df['Product_Name'] = df['Product_Name'].str.strip()

    df['Audit_Flag'] = ""  # Temporary column for auditing

    # 1. Identity issues and append reasons
    # Duplicates
    df.loc[df.duplicated(keep='first'), 'Audit_Flag'] += "Duplicate Entry; "

    # Nulls
    df.loc[df.isnull().any(axis=1), 'Audit_Flag'] += "Missing Data; "

    # Outliers (Logic Checks)
    price_lower, price_upper = get_outlier_thresholds(df['Price'])
    df.loc[(df['Price'] <=price_lower) | (df['Price'] >= price_upper), 'Audit_Flag'] += "Price Mismatch; "
    df.loc[df['Stock_Count'] < 0, 'Audit_Flag'] += "Negative Stock; "

    # Filter to show only rows that have a flag
    dirty_data = df[df['Audit_Flag'] != ""]

    if dirty_data.empty:
        print("No issues found!")
        return df.drop(columns=['Audit_Flag'])

    print("\n--- Audit Review ---\n")

    # 2. Row-wise selection with reasons
    rows_to_drop = []
    for index, row in dirty_data.iterrows():
        print(f"\n[ROW {index}] SKU: {row['SKU']} | Product: {row['Product_Name']}")
        print(f" ISSUES: {row['Audit_Flag']}")

        choice = input("Action: (D)elete, (K)eep, (A)pprove All Remaining: ").lower()

        if choice == "d":
            rows_to_drop.append(index)
        elif choice == "a":
            # Convert the remaining indices to a list
            remaining_indices = dirty_data.index[dirty_data.index >= index].tolist()
            rows_to_drop.extend(remaining_indices)
            break
        else:
            print("Keeping row...")

    # 3. Finalize Cleanup
    print(df.head(5))
    df_clean = df.drop(index=rows_to_drop).drop(columns=['Audit_Flag'])

    # 4. Save the clean file
    clean_file = "data/cleaned_surgical_inventory.csv"
    df_clean.to_csv(clean_file, index=False)

    print(f"Sanitization complete! Saved to {clean_file}")
    print(f"Rows remaining: {len(df_clean)}")


    log_deleted_rows(df, rows_to_drop)
    return df_clean

def log_deleted_rows(df, dropped_indices, filename="data/sanitization_log.csv"):
    if not dropped_indices:
        print("No rows were deleted. Log not created.")
        return

    # 1. Extract the rows that are about to be deleted
    deleted_data = df.loc[dropped_indices].copy()

    # 2. Add a timestamp for the audit trail
    deleted_data['Deletion_Timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 3. Save to a log file (append mode if you want to keep history)
    # If the file exists, don't write the header again
    file_exists = os.path.isfile(filename)
    deleted_data.to_csv(filename, mode="a", index=False, header=not file_exists)

    print(f" Audit trail updated: {filename}")

def get_outlier_thresholds(column):
    Q1 = column.quantile(0.25)  # the 25th percentile
    Q3 = column.quantile(0.75)  # the 75th percentile
    IQR = Q3 - Q1

    # Standard statistical formula for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Business Logic: Price can't be less than zero
    if lower_bound < 0:
        lower_bound = 0

    return lower_bound, upper_bound

# sanitize_data('data/messy_surgical_inventory.csv')