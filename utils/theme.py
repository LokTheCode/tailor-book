"""Application-wide theme.

All styling lives in one file: assets/styles/theme.qss.
Call apply_theme(app) once in main.py; every window picks it up.

To style a widget, give it one of the object names documented at the
top of theme.qss (Card, PageTitle, Primary, ...) instead of calling
setStyleSheet() on it.
"""

from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import QApplication

import re
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


# Settings > Appearance. Each accent replaces the five blue/purple
# colours used in theme.qss: (start, end, solid, hover end, pressed)
ACCENTS = {
    "Blue":   ("#3B82F6", "#8B5CF6", "#2563EB", "#7C3AED", "#1D4ED8"),
    "Purple": ("#8B5CF6", "#EC4899", "#7C3AED", "#DB2777", "#6D28D9"),
    "Green":  ("#10B981", "#14B8A6", "#059669", "#0D9488", "#047857"),
    "Orange": ("#F59E0B", "#EF4444", "#D97706", "#DC2626", "#B45309"),
    "Pink":   ("#EC4899", "#F43F5E", "#DB2777", "#E11D48", "#BE185D"),
}

FONT_SCALES = {"Small": 0.9, "Normal": 1.0, "Large": 1.15}


def _appearance():
    """Accent name and text scale from Settings (defaults if unavailable)."""
    try:
        from services import settings_service
        accent = settings_service.get("accent_color")
        size = settings_service.get("font_size")
    except Exception:
        accent, size = "Blue", "Normal"
    return (accent if accent in ACCENTS else "Blue"), FONT_SCALES.get(size, 1.0)


def _customise(qss: str, accent: str, scale: float) -> str:
    """Swap accent colours and scale every font-size in the stylesheet."""
    if accent != "Blue":
        source = ACCENTS["Blue"]
        target = ACCENTS[accent]
        # Two passes so colours that appear in both lists don't clash
        for index, colour in enumerate(source):
            qss = re.sub(colour, f"@@ACCENT{index}@@", qss, flags=re.IGNORECASE)
        for index, colour in enumerate(target):
            qss = qss.replace(f"@@ACCENT{index}@@", colour)

    if scale != 1.0:
        qss = re.sub(
            r"font-size:\s*(\d+)px",
            lambda m: f"font-size: {max(8, round(int(m.group(1)) * scale))}px",
            qss,
        )
    return qss


def apply_theme(app: QApplication) -> None:
    """Apply the shared font, palette and stylesheet to the whole app.

    Safe to call again after Settings > Appearance changes.
    """
    accent, scale = _appearance()

    app.setFont(QFont("Segoe UI", round(10 * scale)))
    palette = _palette()
    palette.setColor(QPalette.Highlight, QColor(ACCENTS[accent][2]))
    app.setPalette(palette)

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

    app.setStyleSheet(_customise("\n".join(stylesheet), accent, scale))


def repolish(widget) -> None:
    """Re-apply the stylesheet after changing an object name or property."""
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.update()
