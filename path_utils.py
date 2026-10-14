import os
import sys

def get_resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller bundle."""
    if hasattr(sys, "_MEIPASS"):
        # Running inside PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path)
    # Running in normal development environment
    return os.path.join(os.path.abspath("."), relative_path)

def get_writable_db_path(db_filename: str = "customers.db") -> str:
    """Ensure SQLite database is created in a user-writable folder (e.g., AppData)."""
    if sys.platform == "win32":
        app_data = os.environ.get("APPDATA", os.path.expanduser("~"))
        target_dir = os.path.join(app_data, "YourAppName")
    else:
        target_dir = os.path.expanduser("~/.yourappname")
        
    os.makedirs(target_dir, exist_ok=True)
    return os.path.join(target_dir, db_filename)