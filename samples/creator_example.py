# creator_example.py
# This script demonstrates how to fetch, create, and update records in Zoho Creator
# using the zoho_lib library.

import sys
import os
import pandas as pd

# Add the parent directory of this script to the Python system path.
# This ensures that zoho_lib can be imported cleanly, regardless of whether 
# you run this script from the project root or from inside the samples/ directory.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from zoho_lib import conn_mgr, ZCreator

# Initialize the Creator service adapter using the connection named 'my_creator_conn'
# from your external connections.json configuration file.
creator_service = ZCreator(conn_mgr, "my_creator_conn")

def fetch_records_demo():
    print("--- Fetching Records from Zoho Creator Report ---")
    
    # Fetch records from a Creator report (returns a Pandas DataFrame)
    df = creator_service.get_records(
        owner="example_user",
        app="crm-app",
        report="All_Contacts",
        max_records=200
    )
    
    print(f"Loaded {len(df)} records successfully.")
    print(df.head())
    return df

def create_record_demo():
    print("\n--- Creating a New Record in Zoho Creator Form ---")
    
    new_record_payload = {
        "Name": "John Doe",
        "Email": "john.doe@example.com",
        "Company": "ACME Corp"
    }
    
    response = creator_service.create_record(
        owner="example_user",
        app="crm-app",
        form="Contact_Form",
        data=new_record_payload
    )
    
    print("Response from Creator:")
    print(response)

def update_record_demo(record_id):
    print(f"\n--- Updating Record {record_id} ---")
    
    update_payload = {
        "Status": "Active"
    }
    
    response = creator_service.update_record(
        owner="example_user",
        app="crm-app",
        report="All_Contacts",
        record_id=record_id,
        data=update_payload
    )
    
    print("Response from Creator:")
    print(response)

if __name__ == "__main__":
    # 1. Fetch records
    df = fetch_records_demo()
    
    # 2. Add record (uncomment to test)
    # create_record_demo()
    
    # 3. Update record (uncomment to test with a valid ID)
    # if not df.empty:
    #     first_id = df.iloc[0].get("ID")
    #     if first_id:
    #         update_record_demo(first_id)
