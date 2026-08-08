# connection_manager.py

import json
import os
from typing import Dict, List

from .connection import ZohoConnection

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "connections.json")


class ConnectionManager:
    """
    Registry and programmatic CRUD manager for named ZohoConnection objects.
    """

    def __init__(self, config_path: str = DEFAULT_CONFIG_PATH):
        self.config_path = config_path
        self._connections: Dict[str, ZohoConnection] = {}
        # Load connections from file (creates an empty file or initializes gracefully if missing)
        self.load_from_file(self.config_path)

    def load_from_file(self, path: str = None) -> None:
        """
        Load connection definitions from a JSON file.
        If the file doesn't exist or is empty, initializes an empty connections dictionary.
        """
        if path is None:
            path = self.config_path

        if not os.path.isfile(path):
            self._connections = {}
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                raw_configs = json.load(f)
        except Exception:
            self._connections = {}
            return

        if not isinstance(raw_configs, dict):
            raise ValueError("Connection config file must contain a JSON object")

        self._connections = {}
        for name, cfg in raw_configs.items():
            self._connections[name] = self._create_connection(name, cfg)

    def save_to_file(self, path: str = None) -> None:
        """
        Persists the current configuration registry back to the JSON file.
        """
        if path is None:
            path = self.config_path

        raw_configs = {}
        for name, conn in self._connections.items():
            raw_configs[name] = {
                "client_id": conn.client_id,
                "client_secret": conn.client_secret,
                "soid": conn.soid,
                "accounts_domain": conn.accounts_domain,
                "scopes": conn.scopes
            }

        parent_dir = os.path.dirname(os.path.abspath(path))
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(raw_configs, f, indent=2)

    def _create_connection(self, name: str, cfg: dict) -> ZohoConnection:
        """
        Create a ZohoConnection from raw config.
        """
        required_keys = {"client_id", "client_secret", "scopes", "soid"}

        missing = required_keys - cfg.keys()
        if missing:
            raise ValueError(f"Connection '{name}' missing keys: {missing}")

        return ZohoConnection(
            name=name,
            client_id=cfg["client_id"],
            client_secret=cfg["client_secret"],
            scopes=cfg["scopes"],
            soid=cfg["soid"],
            accounts_domain=cfg.get("accounts_domain", "https://accounts.zoho.com")
        )

    # -------------------------------------------------------------
    # Programmatic Connection CRUD API
    # -------------------------------------------------------------

    def add_connection(
        self,
        name: str,
        client_id: str,
        client_secret: str,
        scopes: List[str],
        soid: str,
        accounts_domain: str = "https://accounts.zoho.com",
        save: bool = True
    ) -> None:
        """
        Programmatically add a new named ZohoConnection to the registry and persist it.
        """
        conn = ZohoConnection(
            name=name,
            client_id=client_id,
            client_secret=client_secret,
            scopes=scopes,
            soid=soid,
            accounts_domain=accounts_domain
        )
        self._connections[name] = conn
        if save:
            self.save_to_file()

    def update_connection(self, name: str, save: bool = True, **kwargs) -> None:
        """
        Programmatically update properties of an existing connection and save.
        """
        if name not in self._connections:
            raise KeyError(f"Unknown connection '{name}'")

        conn = self._connections[name]
        
        if "client_id" in kwargs:
            conn.client_id = kwargs["client_id"]
        if "client_secret" in kwargs:
            conn.client_secret = kwargs["client_secret"]
        if "scopes" in kwargs:
            conn.scopes = kwargs["scopes"]
        if "soid" in kwargs:
            conn.soid = kwargs["soid"]
        if "accounts_domain" in kwargs:
            conn.accounts_domain = kwargs["accounts_domain"]

        if save:
            self.save_to_file()

    def delete_connection(self, name: str, save: bool = True) -> None:
        """
        Programmatically delete a connection from the registry and save.
        """
        if name not in self._connections:
            raise KeyError(f"Unknown connection '{name}'")

        del self._connections[name]
        if save:
            self.save_to_file()

    def get(self, name: str) -> ZohoConnection:
        """
        Retrieve a connection by name.
        """
        if name not in self._connections:
            raise KeyError(f"Unknown connection '{name}'")

        return self._connections[name]

    def list_connections(self) -> List[str]:
        """
        List available connection names.
        """
        return list(self._connections.keys())
