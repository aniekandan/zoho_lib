# creator.py

from typing import Optional, Dict, Any
import pandas as pd
from .invoke import invoke
from .connection_manager import ConnectionManager


class ZCreator:
    """
    High-level interface for Zoho Creator APIs.
    Uses invoke() internally to handle auth + HTTP.
    """

    def __init__(self, conn_mgr: ConnectionManager, conn_name: str):
        self.conn_mgr = conn_mgr
        self.conn_name = conn_name

    # -------------------------
    # Public Methods
    # -------------------------

    def get_records(
        self,
        owner: str,
        app: str,
        report: str,
        criteria: Optional[str] = None,
        max_records: int = 200,
    ) -> pd.DataFrame:
        """
        Fetch records from a Creator report and return as DataFrame.
        """

        url = f"https://creator.zoho.com/api/v2.1/{owner}/{app}/report/{report}"

        params = {"max_records": max_records}
        if criteria:
            params["criteria"] = criteria

        resp = invoke(self.conn_name, "GET", url, params=params)

        if not resp.get("success"):
            raise RuntimeError(f"Zoho Creator API error: {resp}")

        # Creator response shape:
        # { code: 3000, data: [ {...}, {...} ] }
        records = resp.get("data", [])

        return pd.DataFrame(records)

    def create_record(
        self, owner: str, app: str, form: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a new record in a Creator form.
        """
        url = f"https://creator.zoho.com/api/v2.1/{owner}/{app}/form/{form}"
        payload = {"data": data}
        return invoke(self.conn_name, "POST", url, data=payload)

    def update_record(
        self, owner: str, app: str, report: str, record_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing record in a report/form.
        """
        url = f"https://creator.zoho.com/api/v2.1/{owner}/{app}/report/{report}/{record_id}"
        payload = {"data": data}
        return invoke(self.conn_name, "PATCH", url, data=payload)
