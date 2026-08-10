# people.py

import json
from typing import List, Dict, Any, Optional, Union
from .invoke import invoke
from .connection_manager import ConnectionManager


class ZPeople:
    """
    High-level interface for Zoho People APIs.
    Uses invoke() internally to handle auth + HTTP.
    """

    def __init__(self, conn_mgr: ConnectionManager, conn_name: str):
        self.conn_mgr = conn_mgr
        self.conn_name = conn_name

    # -------------------------
    # Public Methods
    # -------------------------

    def bulk_import_attendance(
        self,
        data: List[Dict[str, Any]],
        date_format: str = "yyyy-MM-dd HH:mm:ss"
    ) -> Dict[str, Any]:
        """
        Bulk import check-in and check-out details of employees.
        
        Args:
            data: List of dicts containing attendance entries.
                  Example: [{"empId":"1","checkIn":"2014-11-07 09:01:00"}]
            date_format: format of the date strings in the data.
        """
        url = "https://people.zoho.com/people/api/attendance/bulkImport"
        
        # The documentation shows data as a query parameter containing a JSON string.
        params = {
            "data": json.dumps(data),
            "dateFormat": date_format
        }
        
        return invoke(
            connection_name=self.conn_name,
            method="POST",
            url=url,
            params=params
        )

    def update_form_record(
        self,
        form_link_name: str,
        record_id: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a specific record in a Zoho People form.
        
        Args:
            form_link_name: The link name of the form/module.
            record_id: The Zoho People record ID.
            input_data: A dictionary of fields and values to update.
        """
        url = f"https://people.zoho.com/api/forms/json/{form_link_name}/updateRecord"
        
        params = {
            "recordId": record_id,
            "inputData": json.dumps(input_data)
        }
        
        return invoke(
            connection_name=self.conn_name,
            method="POST",
            url=url,
            params=params
        )

    def get_holidays(self, from_date: str, to_date: str) -> List[str]:
        """
        Fetch holiday dates from Zoho People within a given range.
        
        Args:
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            
        Returns:
            List of date strings that are holidays (e.g. ['2024-01-01', ...])
        """
        url = "https://people.zoho.com/people/api/leave/v2/holidays/get"
        params = {
            "fromDate": from_date,
            "toDate": to_date
        }
        
        response = invoke(
            connection_name=self.conn_name,
            method="GET",
            url=url,
            params=params
        )
        
        if not response.get("success"):
            return []
            
        data = response.get("data", {})
        
        # Parse the nested response: {"response": {"result": [{"date": "..."}]}}
        resp_obj = data.get("response", {})
        result_list = resp_obj.get("result", [])
        
        if not isinstance(result_list, list):
             return []
             
        holidays = []
        for item in result_list:
            if isinstance(item, dict) and "date" in item:
                holidays.append(item["date"])
                
        return holidays

    def get_employee_by_biometric_id(self, biometric_id: str) -> Optional[str]:
        """
        Lookup the core Zoho Employee ID for a given Biometric ID.
        
        Args:
            biometric_id: The ID coming from the ZKTeco hardware.
            
        Returns:
            The Zoho EmployeeID string if found, else None.
        """
        url = "https://people.zoho.com/people/api/forms/P_Employee/getRecords"
        
        response = invoke(
            connection_name=self.conn_name,
            method="GET",
            url=url
        )
        
        if not response.get("success"):
            return None
            
        data = response.get("data", {})
        resp_obj = data.get("response", {})
        result_list = resp_obj.get("result", [])
        
        if not isinstance(result_list, list):
             return None
             
        for item in result_list:
             if isinstance(item, dict):
                 for key, val_list in item.items():
                     if isinstance(val_list, list):
                         for record in val_list:
                             if isinstance(record, dict):
                                 if str(record.get("Biometric_ID")) == str(biometric_id):
                                     return record.get("EmployeeID")
                                     
        return None
