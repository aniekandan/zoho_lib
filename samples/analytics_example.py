# analytics_example.py
# This script demonstrates how to fetch table data from Zoho Analytics workspaces
# using the zoho_lib library.

import sys
import os
import pandas as pd

# Add the parent directory of this script to the Python system path.
# This ensures that zoho_lib can be imported cleanly, regardless of whether 
# you run this script from the project root or from inside the samples/ directory.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from zoho_lib import conn_mgr, ZAnalytics

# Initialize the Analytics service adapter using the connection named 'my_analytics_conn'
# from your external connections.json configuration file.
analytics_service = ZAnalytics(conn_mgr, "my_analytics_conn")

def fetch_table_data_demo():
    print("--- Fetching Table Data from Zoho Analytics View ---")
    
    workspace_id = "1234567890123456789"
    view_id = "9876543210987654321"
    
    # Define columns to extract
    columns_to_fetch = [
        "Region",
        "Sales",
        "Quantity",
        "Profit"
    ]
    
    # Fetch data (returns a Pandas DataFrame)
    df = analytics_service.get_table_data(
        workspace_id=workspace_id,
        view_id=view_id,
        selected_columns=columns_to_fetch
    )
    
    print(f"Loaded {len(df)} rows successfully.")
    print("\nFirst 5 rows of retrieved data:")
    print(df.head())
    
    # Perform cleanups or calculations with Pandas
    if not df.empty:
        print("\nBasic Stats on Numerical Columns:")
        # Convert values to numeric if necessary
        df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
        print(df["Sales"].describe())

if __name__ == "__main__":
    fetch_table_data_demo()
