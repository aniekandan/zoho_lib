[Portfolio Home](https://aniekandan.github.io/PythonPortfolioDocs/)
# Zoho Helper Python Library (zoho_lib`)

An abstract, elegant, and robust Python-based library for programmatic data exchanges (ETL, synchronization) with **Zoho Creator** and **Zoho Analytics**. It removes OAuth boilerplate, standardizes REST API transport, and seamlessly exports records directly as clean **Pandas DataFrames**.

---

## 1. Directory Structure

The core library, package configurations, and ready-to-run samples are neatly separated. The connection configuration file (`connections.json`) resides at a fixed, predictable location directly **inside** the `zoho_lib` package directory:

```
my_project/
│
├── zoho_lib/                 # Core Python Package (reusable & isolated)
│   ├── __init__.py           # Package entry point and exports
│   ├── app.py                # Singleton manager entry point
│   ├── connections.json      # Fixed internal configuration (KEEP SECURE!)
│   ├── connection.py         # Individual Zoho connection & OAuth handler
│   ├── connection_manager.py # Registry & Programmatic Connection API
│   ├── invoke.py             # Standardized HTTP transport & auth injector
│   ├── creator.py            # Zoho Creator API service adapter
│   └── analytics.py          # Zoho Analytics API service adapter
│
├── samples/                  # Sibling examples folder (run scripts from here)
│   ├── connections_example.py# Zoho connection management CRUD operations
│   ├── creator_example.py    # Zoho Creator integration (GET, POST, PATCH)
│   └── analytics_example.py  # Zoho Analytics table data integration (GET)
│
└── requirements.txt          # Package dependencies
```

---

## 2. Installation & Prerequisites

Ensure you have Python 3.8+ installed along with `requests` and `pandas`:

```bash
pip install -r requirements.txt
```

---

## 3. Configuration & Connection API (`connections.json`)

### Predictable File Resolution
The configuration file `connections.json` has a fixed, reliable path inside the `zoho_lib` directory. Since the library resolves this path relative to its own module, you can run scripts from any location in your workspace without worrying about relative file paths or file-not-found errors!

### Programmatic Connection Management (Code-First)
The library exposes a complete set of Python APIs to query, add, update, and remove connections in `connections.json` directly from your code. Any modifications made are automatically saved to the configuration file (controlled by the optional `save=True` argument).

```python
from zoho_lib import conn_mgr

# 1. List all currently registered connection names
print(conn_mgr.list_connections())
# Output: ['my_creator_conn', 'my_analytics_conn']

# 2. Add a new Zoho Creator connection programmatically
conn_mgr.add_connection(
    name="division_b_creator",
    client_id="1000.ANOTHERCLIENTID9876",
    client_secret="anothersecret6543210example",
    scopes=["ZohoCreator.report.READ"],
    soid="ZohoCreator.987654321",
    accounts_domain="https://accounts.zoho.eu"  # Custom datacenter support
)

# 3. Update an existing connection's client_secret or scopes
conn_mgr.update_connection(
    name="my_creator_conn",
    client_secret="newly_rotated_secret_123456"
)

# 4. Remove a connection programmatically
conn_mgr.delete_connection("division_b_creator")
```

### Static Configuration Template
If you prefer editing the JSON configuration file directly, open `zoho_lib/connections.json` and customize your connection mappings using the template below:

```json
{
  "my_creator_conn": {
    "client_id": "YOUR_ZOHO_CLIENT_ID_HERE",
    "client_secret": "YOUR_ZOHO_CLIENT_SECRET_HERE",
    "soid": "ZohoCreator.YOUR_ORG_ID_HERE",
    "accounts_domain": "https://accounts.zoho.com",
    "scopes": [
      "ZohoCreator.form.CREATE",
      "ZohoCreator.report.READ",
      "ZohoCreator.report.UPDATE",
      "ZohoCreator.report.DELETE"
    ]
  },
  "my_analytics_conn": {
    "client_id": "YOUR_ZOHO_CLIENT_ID_HERE",
    "client_secret": "YOUR_ZOHO_CLIENT_SECRET_HERE",
    "soid": "ZohoAnalytics.YOUR_ORG_ID_HERE",
    "accounts_domain": "https://accounts.zoho.com",
    "scopes": [
      "ZohoAnalytics.data.read",
      "ZohoAnalytics.data.create"
    ]
  }
}
```

---

## 4. Getting Started

Import the convenience manager and service adapters directly from the library to execute operations:

```python
import pandas as pd
from zoho_lib import conn_mgr, ZCreator, ZAnalytics

# 1. Initialize the services using the connection names declared in connections.json
creator = ZCreator(conn_mgr, "my_creator_conn")
analytics = ZAnalytics(conn_mgr, "my_analytics_conn")

# 2. Fetch Creator reports as clean Pandas DataFrames
df_creator = creator.get_records(
    owner="example_user",
    app="crm-app",
    report="All_Contacts"
)
print(df_creator.head())

# 3. Fetch Analytics tables as clean Pandas DataFrames
df_analytics = analytics.get_table_data(
    workspace_id="1234567890123456789",
    view_id="9876543210987654321",
    selected_columns=["Region", "Sales", "Quantity"]
)
print(df_analytics.head())
```

---

## 5. Ready-to-Run Samples

Fully functional scripts reside in the **external** sibling `samples/` directory:

* **`samples/connections_example.py`**: Demonstrates connection management (CRUD) such as programmatically listing, adding, updating, and deleting connections in `connections.json` using the connection manager.
* **`samples/creator_example.py`**: Handles Zoho Creator list views, inserts a new contact, and edits existing record parameters.
* **`samples/analytics_example.py`**: Fetches multidimensional workspace views as a Pandas DataFrame and summarizes records.

### How to Run:
You can execute these samples from any location. All files are pre-loaded with sys-path append guards:
```bash
# From project root:
python samples/connections_example.py
python samples/creator_example.py
python samples/analytics_example.py

# Or from inside the samples/ folder:
cd samples
python connections_example.py
python creator_example.py
```
