# invoke.py

import requests
from typing import Dict, Any, Optional
from .app import conn_mgr


def invoke(
    connection_name: str,
    method: str,
    url: str,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    files: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
) -> Dict[str, Any]:
    """
    Generic HTTP request using a named Zoho connection.

    Args:
        connection_name: str, name of connection in conn_mgr
        method: HTTP method ("GET", "POST", "PATCH", etc.)
        url: full API endpoint
        params: URL query parameters
        data: request payload (dict, will be converted to JSON)
        headers: additional headers
        files: files dict for multipart upload
        timeout: request timeout in seconds

    Returns:
        dict: normalized JSON response
    """
    try:
        conn = conn_mgr.get(connection_name)
    except KeyError:
        return {"success": False, "error": f"Connection '{connection_name}' not found"}

    # Default headers with Authorization
    request_headers = headers.copy() if headers else {}
    request_headers["Authorization"] = f"Zoho-oauthtoken {conn.get_access_token()}"
    if data and not files:
        request_headers["Content-Type"] = "application/json"

    try:
        resp = requests.request(
            method=method.upper(),
            url=url,
            headers=request_headers,
            params=params,
            json=data,
            files=files,
            timeout=timeout,
        )

        # Raise for HTTP error codes
        resp.raise_for_status()

        # Parse JSON if possible
        try:
            return {"success": True, "data": resp.json()}
        except ValueError:
            return {"success": True, "data": resp.text}

    except requests.RequestException as e:
        return {"success": False, "error": str(e)}
