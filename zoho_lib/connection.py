# connection.py

import time
import requests
from typing import List, Optional


class ZohoConnection:
    """
    Represents a single Zoho OAuth connection.
    Handles access token retrieval and refresh.
    """

    TOKEN_ENDPOINT = "/oauth/v2/token"

    def __init__(
        self,
        name: str,
        client_id: str,
        client_secret: str,
        scopes: List[str],
        soid: str,
        accounts_domain: str = "https://accounts.zoho.com"
    ):
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes
        self.soid = soid
        self.accounts_domain = accounts_domain

        self._access_token: Optional[str] = None
        self._expiry_ts: float = 0.0

    # -------------------------
    # Public API
    # -------------------------

    def get_access_token(self) -> str:
        """
        Return a valid access token.
        Refreshes token if expired or missing.
        """
        if self._token_expired():
            self._fetch_new_token()
        return self._access_token

    # -------------------------
    # Internal helpers
    # -------------------------

    def _token_expired(self) -> bool:
        """
        Check whether the current token is expired
        (with a small safety buffer).
        """
        # Refresh if within 60 seconds of expiry
        return not self._access_token or time.time() >= (self._expiry_ts - 60)

    def _fetch_new_token(self) -> None:
        """
        Fetch a new access token using client credentials grant.
        """
        scope_str = ",".join(self.scopes)

        url = f"{self.accounts_domain}{self.TOKEN_ENDPOINT}"

        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "scope": scope_str,
            "soid": self.soid,
        }

        response = requests.post(url, data=payload, timeout=30)
        response.raise_for_status()

        data = response.json()

        if "access_token" not in data:
            raise RuntimeError(
                f"Failed to obtain access token for connection '{self.name}': {data}"
            )

        self._access_token = data["access_token"]

        # Zoho typically returns expires_in (seconds)
        expires_in = int(data.get("expires_in", 3600))
        self._expiry_ts = time.time() + expires_in

    def get_org_id(self) -> str:
        """
        Extract and return the Org ID from the SOID.
        """
        return self.soid.split(".")[1]
