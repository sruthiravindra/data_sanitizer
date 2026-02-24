import pandas as pd
import numpy as np
import random

def generate_messy_surgical_data(rows=20):
    data={
        'SKU': [f"SURG-{1000+i}" for i in range(rows)],
        'Product_Name':([
            "Scalpel Holder", "Hemostatic Forceps", "Retractor", "Needle Driver",
            "Metzenbaum Scissors", "Adson Tissue Forceps", "Speculum", "Bone Saw"
        ]*(rows // 8 + 1))[:rows],
        'Category': (["Cutting", "Grasping", "Retracting", "Suturing", "Cutting", "Grasping", "Diagnostic",
                     "Orthopedic"] * (rows // 8 + 1))[:rows],
        'Price':[round(random.uniform(15.0, 500.2),2) for _ in range(rows)],
        'Stock_Count':[random.randint(0,100) for _ in range(rows)],
        'Last_Restock_Date': pd.date_range(start='2023-01-01', periods=rows, freq='D').strftime('%Y-%m-%d')
    }

    df = pd.DataFrame(data).iloc[:rows]

    # --- INJECTING "MESSY" DATA ---

    # 1. Typos and Casing issues
    df.at[2, 'Category'] = "cutting"  # Lowercase
    df.at[5, 'Category'] = "Grasping "  # Trailing space
    df.at[10, 'Product_Name'] = "Scalp3l Holdr"  # Typos

    # 2. Missing values (NaNs)
    df.at[3, 'Price'] = np.nan
    df.at[7, 'Stock_Count'] = np.nan

    # 3. Outliers and illogical values
    df.at[0, 'Price'] = 99999.99  # Extreme outlier
    df.at[12, 'Stock_Count'] = -5  # Impossible value

    # 4. Format inconsistencies
    df.at[15, 'Last_Restock_Date'] = "05/12/2023"  # Wrong date format

    # 5. Duplicates
    df = pd.concat([df, df.iloc[[1]]], ignore_index=True)

    return df

# # Generate and save
# messy_df = generate_messy_surgical_data(25)
# messy_df.to_csv('messy_surgical_inventory.csv', index=False)
# print("Dataset 'messy_surgical_inventory.csv' generated successfully!")