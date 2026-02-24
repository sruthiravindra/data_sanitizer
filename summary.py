import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def generate_business_summary(df):
    print("\n--- Generating Business Summary ---")


    # 1. Create a temporary 'Inventory_Value' Column
    df['Inventory_Value'] = df['Price'] * df['Stock_Count']

    # 2. Group by Category and sum numeric values
    summary = df.groupby(['Category']).agg({
        'SKU': 'count',
        'Stock_Count': 'sum',
        'Inventory_Value': 'sum'
    }).reset_index()

    summary.columns = ['Category', 'Product_Count', 'Total_Stock', 'Total_Value']

    # Draw charts WHILE Total_Value is still a number
    visualize_business_summary(summary)

    # NOW format for the console output
    readable_summary = summary.copy()
    readable_summary['Total_Value'] = readable_summary['Total_Value'].apply(lambda x: f"${x:,.2f}")
    print(readable_summary)

    return summary


def visualize_business_summary(summary):
    # Initialize the PDF file
    with PdfPages('data/Surgical_Inventory_Report.pdf') as pdf:
        # --- PAGE 1: Executive Summary Table ---
        fig_table, ax = plt.subplots(figsize=(10, 4))
        ax.axis('off')  # Hide the graph lines/axis
        readable_summary = summary.copy()
        readable_summary['Total_Value'] = readable_summary['Total_Value'].apply(lambda x: f"${x:,.2f}")

        # Create the table
        tbl = ax.table(
            cellText=readable_summary.values,
            colLabels=readable_summary.columns,
            cellLoc='center',
            loc='center'
        )

        # Style the table
        # Style the header specifically
        for (row, col), cell in tbl.get_celld().items():
            if row == 0:  # This is the header row
                cell.set_text_props(weight='bold', color='white')
                cell.set_facecolor('#4c72b0')  # A nice professional blue
            elif row%2 !=0:
                cell.set_text_props(color='black')
                cell.set_facecolor('skyblue')  # A nice professional blue
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(12)
        tbl.scale(1.2, 1.5)  # Scale for better padding

        plt.title("Executive Inventory Summary", y=1.1)
        pdf.savefig(fig_table, bbox_inches='tight')
        plt.close()

        # --- Page 2: Product Count ---
        fig1 = plt.figure(figsize=(10, 6))
        bars = plt.bar(summary['Category'], summary['Product_Count'], color='skyblue')
        # Logic to add text labels...
        plt.title("Product Count by Category")
        pdf.savefig(fig1)  # Save first
        plt.close()  # Close to free up RAM

        # --- Page 2: Total Value ---
        fig2 = plt.figure(figsize=(8, 8))
        plt.pie(summary['Total_Value'], labels=summary['Category'], autopct='%1.1f%%')
        plt.title("Inventory Value Distribution")
        pdf.savefig(fig2)
        plt.close()

        # --- Page 3: Stock Count ---
        fig3 = plt.figure(figsize=(10, 6))
        plt.bar(summary['Category'], summary['Total_Stock'], color='salmon')
        # Logic to add text labels...
        plt.title("Product Stock Count by Category")
        pdf.savefig(fig3)
        plt.close()

    print("✅ Professional PDF Report generated: Surgical_Inventory_Report.pdf")
#
# # Usage:
# df = pd.read_csv('data/cleaned_surgical_inventory.csv')
# generate_business_summary(df)
