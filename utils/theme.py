"""Application-wide theme.

All styling lives in one file: assets/styles/theme.qss.
Call apply_theme(app) once in main.py; every window picks it up.

To style a widget, give it one of the object names documented at the
top of theme.qss (Card, PageTitle, Primary, ...) instead of calling
setStyleSheet() on it.
"""

from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import QApplication

import sys
from pathlib import Path

from config import DEBUG

THEME_FILE = "assets/styles/theme.qss"

# Outlines every widget in a bright colour; enable with DEBUG=True in config.py
DEBUG_FILE = "assets/styles/debug.qss"


def _asset_path(relative: str) -> Path:
    """Works both from source and inside a PyInstaller bundle."""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
    return base / relative

# Same colours as the palette notes at the top of theme.qss
BACKGROUND = "#111827"
SURFACE = "#1F2937"
BORDER = "#374151"
TEXT = "#F9FAFB"
MUTED = "#9CA3AF"
PRIMARY = "#2563EB"
SUCCESS = "#10B981"
WARNING = "#F59E0B"
DANGER = "#DC2626"


def _palette() -> QPalette:
    """Dark palette so native parts (dialogs, popups) match the QSS."""
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(BACKGROUND))
    palette.setColor(QPalette.WindowText, QColor(TEXT))
    palette.setColor(QPalette.Base, QColor(BACKGROUND))
    palette.setColor(QPalette.AlternateBase, QColor(SURFACE))
    palette.setColor(QPalette.Text, QColor(TEXT))
    palette.setColor(QPalette.Button, QColor(SURFACE))
    palette.setColor(QPalette.ButtonText, QColor(TEXT))
    palette.setColor(QPalette.Highlight, QColor(PRIMARY))
    palette.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))
    palette.setColor(QPalette.ToolTipBase, QColor(SURFACE))
    palette.setColor(QPalette.ToolTipText, QColor(TEXT))
    palette.setColor(QPalette.PlaceholderText, QColor("#6B7280"))
    return palette


def apply_theme(app: QApplication) -> None:
    """Apply the shared font, palette and stylesheet to the whole app."""
    app.setFont(QFont("Segoe UI", 10))
    app.setPalette(_palette())

    files = [THEME_FILE]
    if DEBUG:
        files.append(DEBUG_FILE)

    stylesheet = []
    for relative in files:
        path = _asset_path(relative)
        try:
            stylesheet.append(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            print(f"Warning: stylesheet not found at {path}")

    app.setStyleSheet("\n".join(stylesheet))


def repolish(widget) -> None:
    """Re-apply the stylesheet after changing an object name or property."""
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.update()
