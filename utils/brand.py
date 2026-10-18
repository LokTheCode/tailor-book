"""Product branding helpers: icon, logo, and the customer's shop name."""

import sys
from pathlib import Path

from config import APP_NAME

BRAND_DIR = "assets/brand"
ICON_PNG = f"{BRAND_DIR}/tailorbook_icon.png"
ICON_ICO = f"{BRAND_DIR}/tailorbook.ico"

DEFAULT_SHOP_NAME = "My Tailor Shop"


def asset(relative: str) -> str:
    """Absolute path to a bundled file.

    Works when run from source and inside the installed (PyInstaller)
    app, where files live next to the .exe rather than in the current
    folder.
    """
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
    return str(base / relative)


def app_icon():
    from PySide6.QtGui import QIcon
    return QIcon(asset(ICON_ICO if sys.platform == "win32" else ICON_PNG))


def logo_pixmap(size: int):
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QPixmap
    pixmap = QPixmap(asset(ICON_PNG))
    return pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)


def shop_name() -> str:
    """The customer's own shop name from Settings > Shop Details."""
    try:
        from services import settings_service
        return settings_service.get("shop_name").strip() or DEFAULT_SHOP_NAME
    except Exception:
        return DEFAULT_SHOP_NAME


def window_title() -> str:
    return f"{shop_name()} - {APP_NAME}"
