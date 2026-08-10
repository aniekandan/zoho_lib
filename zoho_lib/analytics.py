import json
import pandas as pd
from typing import Optional
from .invoke import invoke
from .connection_manager import ConnectionManager


class ZAnalytics:
    """
    High-level interface for Zoho Analytics APIs.
    Uses invoke() internally to handle auth + HTTP.
    """

    def __init__(self, conn_mgr: ConnectionManager, conn_name: str):
        self.conn_mgr = conn_mgr
        self.conn_name = conn_name
        self.conn = conn_mgr.get(conn_name)

    # -------------------------
    # Public Methods
    # -------------------------

    def get_table_data(
        self,
        workspace_id: str,
        view_id: str,
        selected_columns: list[str],
    ) -> pd.DataFrame:
        """
        Fetch table data from a Zoho Analytics view and return as DataFrame.
        """

        url = (
            f"https://analyticsapi.zoho.com/restapi/v2/"
            f"workspaces/{workspace_id}/views/{view_id}/data"
        )

        headers = {
            "ZANALYTICS-ORGID": self.conn.get_org_id()
        }

        config = {
            "responseFormat": "json",
            "selectedColumns": selected_columns,
        }

        params = {
            "CONFIG": json.dumps(config)
        }

        resp = invoke(
            connection_name=self.conn_name,
            method="GET",
            url=url,
            headers=headers,
            params=params
        )

        if not resp.get("success"):
            raise RuntimeError(f"Zoho Analytics API error: {resp}")

        # Analytics response shape:
        # { data: [ {...}, {...} ] }
        rows = resp.get("data", {}).get("data", [])

        return pd.DataFrame(rows)

