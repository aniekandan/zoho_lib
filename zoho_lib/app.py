# app.py

from .connection_manager import ConnectionManager

# Private singleton instance
_conn_mgr = None


def get_connection_manager() -> ConnectionManager:
    """
    Returns a singleton ConnectionManager.
    Safe to call multiple times (Jupyter, Flask, CLI).
    """
    global _conn_mgr

    if _conn_mgr is None:
        _conn_mgr = ConnectionManager()

    return _conn_mgr


# Convenience export (Deluge-like feel)
conn_mgr = get_connection_manager()
