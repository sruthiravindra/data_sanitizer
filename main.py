import os
import pandas as pd

from create_sample_data import generate_messy_surgical_data
from generate_validation_report import audit_inventory
from sanitize_data import sanitize_data, interactive_sanitize
from summary import generate_business_summary

#
# BUSINESS_RULES = {
#     'max_price': 5000,
#     'min_price': 0.50,
#     'max_stock': 1000
# }

def run_pipeline():
    # Define file names
    raw_file = 'data/messy_surgical_inventory.csv'
    report_pdf = 'data/Surgical_Inventory_Report.pdf'

    print("Starting OneMetricLabs Data Sanitizer...")

    # STEP 1: Generate Data (Only if it doesn't exist)
    if not os.path.exists(raw_file):
        print(f"Generating raw dataset: {raw_file}")
        df_raw = generate_messy_surgical_data(rows=50)
        df_raw.to_csv(raw_file, index=False)

    # STEP 2: Audit (The "Before" Picture)
    print("\nAuditing raw data for issues...")
    audit_results = audit_inventory(raw_file)

    # STEP 3: Sanitize (The Cleaning Process)
    print("\nSanitizing data...")
    # df_clean = sanitize_data(raw_file)
    df_clean = interactive_sanitize(raw_file)

    # STEP 4: Analyze & Report
    print("\nGenerating business insights and PDF report...")
    summary = generate_business_summary(df_clean)

    print("\n" + "="*40)
    print(f"SUCCESS! Final report saved as: {report_pdf}")
    print("="*40)



if __name__ == "__main__":
    run_pipeline()