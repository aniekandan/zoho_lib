# connections_example.py
# This script demonstrates how to programmatically manage (CRUD) Zoho API connections
# in your connections.json configuration using the connection manager.

import sys
import os

# Add the parent directory of this script to the Python system path.
# This ensures that zoho_lib can be imported cleanly, regardless of whether 
# you run this script from the project root or from inside the samples/ directory.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from zoho_lib import conn_mgr

def demonstrate_connection_crud():
    print("=== 1. Listing Current Connections ===")
    initial_connections = conn_mgr.list_connections()
    print(f"Current connections: {initial_connections}")

    print("\n=== 2. Adding a New Connection Programmatically ===")
    test_connection_name = "sandbox_creator_connection"
    
    # We add a connection with dummy credentials for demo purposes
    conn_mgr.add_connection(
        name=test_connection_name,
        client_id="1000.SANDBOXCLIENTID1234567890",
        client_secret="sandboxsecret9876543210example",
        scopes=[
            "ZohoCreator.form.CREATE",
            "ZohoCreator.report.READ"
        ],
        soid="ZohoCreator.999999999",
        accounts_domain="https://accounts.zoho.eu", # Supporting custom domains
        save=True # This saves the changes to connections.json instantly
    )
    print(f"Added connection '{test_connection_name}'.")
    print(f"Updated connections: {conn_mgr.list_connections()}")

    print("\n=== 3. Retrieving and Inspecting the New Connection ===")
    connection_details = conn_mgr.get(test_connection_name)
    print(f"Connection Object Name: {connection_details.name}")
    print(f"Client ID: {connection_details.client_id}")
    print(f"Client Secret: {connection_details.client_secret}")
    print(f"Scopes: {connection_details.scopes}")
    print(f"SOID: {connection_details.soid}")
    print(f"Accounts Domain: {connection_details.accounts_domain}")

    print("\n=== 4. Updating the Connection programmatically ===")
    conn_mgr.update_connection(
        name=test_connection_name,
        client_secret="new_rotated_sandbox_secret_abc123",
        save=True
    )
    updated_connection = conn_mgr.get(test_connection_name)
    print(f"Updated Client Secret: {updated_connection.client_secret}")

    print("\n=== 5. Deleting the Connection programmatically ===")
    conn_mgr.delete_connection(test_connection_name, save=True)
    print(f"Deleted connection '{test_connection_name}'.")
    print(f"Final connections list: {conn_mgr.list_connections()}")

if __name__ == "__main__":
    demonstrate_connection_crud()
