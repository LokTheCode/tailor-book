"""Application-wide theme.

All styling lives in one file: assets/styles/theme.qss. It uses colour
roles like @bg and @text; this module fills them in from the theme the
user picked in Settings > Appearance, plus their accent colour and text
size. Call apply_theme(app) once in main.py (and again after a change).

To style a widget, give it one of the object names documented at the
top of theme.qss (Card, PageTitle, Primary, ...) instead of calling
setStyleSheet() on it. For icons on normal buttons use
theme_color("text") instead of a fixed colour, so they show on light
themes too.
"""

import colorsys
import re
import sys
from pathlib import Path

from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import QApplication

from config import DEBUG

THEME_FILE = "assets/styles/theme.qss"

# Outlines every widget in a bright colour; enable with DEBUG=True in config.py
DEBUG_FILE = "assets/styles/debug.qss"


def _asset_path(relative: str) -> Path:
    """Works both from source and inside a PyInstaller bundle."""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
    return base / relative


# ==========================================================
# THEMES
# ==========================================================
# Every theme fills the same colour roles used in theme.qss.
# "accent" is the theme's own accent (see ACCENTS) unless the user
# picks another one.

THEMES = {
    "Midnight": {
        "description": "Dark slate with blue (default)",
        "dark": True,
        "accent": "Blue",
        "bg": "#111827", "surface": "#1F2937", "border": "#374151", "border_strong": "#4B5563",
        "hover": "#273549", "disabled_bg": "#0F172A",
        "text": "#F9FAFB", "text_soft": "#E5E7EB", "text_label": "#D1D5DB", "text_info": "#CBD5E1",
        "muted": "#9CA3AF", "faint": "#6B7280",
        "row_alt": "#1A2332", "row_line": "#2B3647", "row_hover": "#243247",
        "row_selected": "#1E3A5F", "selected_text": "#FFFFFF",
        "sidebar_bg": "#0F172A", "sidebar_hover": "#1F2937", "sidebar_text": "#D1D5DB",
        "sidebar_strong": "#FFFFFF", "topbar_bg": "#111827",
        "success_text": "#10B981", "warning_text": "#F59E0B", "danger_text": "#EF4444",
    },
    "Classic Light": {
        "description": "Clean white and light grey",
        "dark": False,
        "accent": "Blue",
        "bg": "#F4F6F9", "surface": "#FFFFFF", "border": "#E2E8F0", "border_strong": "#CBD5E1",
        "hover": "#EEF2FF", "disabled_bg": "#F1F5F9",
        "text": "#0F172A", "text_soft": "#1E293B", "text_label": "#334155", "text_info": "#475569",
        "muted": "#5B677A", "faint": "#94A3B8",
        "row_alt": "#F8FAFC", "row_line": "#EDF2F7", "row_hover": "#F1F5FF",
        "row_selected": "#DBEAFE", "selected_text": "#0F172A",
        "sidebar_bg": "#1E293B", "sidebar_hover": "#334155", "sidebar_text": "#CBD5E1",
        "sidebar_strong": "#FFFFFF", "topbar_bg": "#FFFFFF",
        "success_text": "#047857", "warning_text": "#B45309", "danger_text": "#DC2626",
    },
    "Ocean": {
        "description": "Deep sea blue with teal",
        "dark": True,
        "accent": "Teal",
        "bg": "#071A2B", "surface": "#0E2A42", "border": "#1D4060", "border_strong": "#2B5679",
        "hover": "#143756", "disabled_bg": "#06131F",
        "text": "#F0F9FF", "text_soft": "#E0F2FE", "text_label": "#BAE6FD", "text_info": "#A5C9E3",
        "muted": "#86ABC8", "faint": "#557A99",
        "row_alt": "#0C2439", "row_line": "#17344F", "row_hover": "#12324D",
        "row_selected": "#164A70", "selected_text": "#FFFFFF",
        "sidebar_bg": "#04121F", "sidebar_hover": "#0E2A42", "sidebar_text": "#A5C9E3",
        "sidebar_strong": "#FFFFFF", "topbar_bg": "#071A2B",
        "success_text": "#34D399", "warning_text": "#FBBF24", "danger_text": "#F87171",
    },
    "Royal Purple": {
        "description": "Colourful dark purple with pink",
        "dark": True,
        "accent": "Pink",
        "bg": "#160F2E", "surface": "#221846", "border": "#3A2C6B", "border_strong": "#4E3D8A",
        "hover": "#2E2160", "disabled_bg": "#120C25",
        "text": "#FAF5FF", "text_soft": "#EDE9FE", "text_label": "#DDD6FE", "text_info": "#C4B5FD",
        "muted": "#A9A0D2", "faint": "#6F6799",
        "row_alt": "#1D1440", "row_line": "#312560", "row_hover": "#2A1E57",
        "row_selected": "#45307F", "selected_text": "#FFFFFF",
        "sidebar_bg": "#0F0A21", "sidebar_hover": "#221846", "sidebar_text": "#C4B5FD",
        "sidebar_strong": "#FFFFFF", "topbar_bg": "#160F2E",
        "success_text": "#34D399", "warning_text": "#FBBF24", "danger_text": "#FB7185",
    },
    "Sunrise": {
        "description": "Colourful warm cream and orange",
        "dark": False,
        "accent": "Orange",
        "bg": "#FFF7ED", "surface": "#FFFFFF", "border": "#FCDDBA", "border_strong": "#F2B87E",
        "hover": "#FFEDD5", "disabled_bg": "#FBF3EA",
        "text": "#3B1D0B", "text_soft": "#4A2814", "text_label": "#6B3A1E", "text_info": "#7C4A2A",
        "muted": "#8F5F3D", "faint": "#C29A7A",
        "row_alt": "#FFFBF6", "row_line": "#FDEBD7", "row_hover": "#FFF1E2",
        "row_selected": "#FFE0C2", "selected_text": "#3B1D0B",
        "sidebar_bg": "#7C2D12", "sidebar_hover": "#9A3412", "sidebar_text": "#FED7AA",
        "sidebar_strong": "#FFFFFF", "topbar_bg": "#FFFFFF",
        "success_text": "#047857", "warning_text": "#B45309", "danger_text": "#DC2626",
    },
    "Mint": {
        "description": "Fresh light green",
        "dark": False,
        "accent": "Green",
        "bg": "#F0FDF4", "surface": "#FFFFFF", "border": "#CDEFD9", "border_strong": "#9EDDB6",
        "hover": "#DCFCE7", "disabled_bg": "#EEF7F1",
        "text": "#052E16", "text_soft": "#14532D", "text_label": "#166534", "text_info": "#3F6B52",
        "muted": "#4B7A5F", "faint": "#8FB3A0",
        "row_alt": "#F7FDF9", "row_line": "#E3F5EA", "row_hover": "#ECFDF3",
        "row_selected": "#C8F2D8", "selected_text": "#052E16",
        "sidebar_bg": "#064E3B", "sidebar_hover": "#065F46", "sidebar_text": "#A7F3D0",
        "sidebar_strong": "#FFFFFF", "topbar_bg": "#FFFFFF",
        "success_text": "#047857", "warning_text": "#B45309", "danger_text": "#DC2626",
    },
}

DEFAULT_THEME = "Midnight"

# Accent colours: (gradient start, gradient end, solid, end on hover, pressed).
# Starts are dark enough for white button text to stay readable.
ACCENTS = {
    "Blue":   ("#3B82F6", "#8B5CF6", "#2563EB", "#7C3AED", "#1D4ED8"),
    "Purple": ("#7C3AED", "#C026D3", "#6D28D9", "#A21CAF", "#5B21B6"),
    "Pink":   ("#DB2777", "#E11D48", "#BE185D", "#BE123C", "#9D174D"),
    "Red":    ("#DC2626", "#EA580C", "#B91C1C", "#C2410C", "#991B1B"),
    "Orange": ("#EA580C", "#DC2626", "#C2410C", "#B91C1C", "#9A3412"),
    "Green":  ("#059669", "#0D9488", "#047857", "#0F766E", "#065F46"),
    "Teal":   ("#0D9488", "#0284C7", "#0F766E", "#0369A1", "#115E59"),
}

THEME_DEFAULT_ACCENT = "Theme default"
CUSTOM_ACCENT = "Custom"

FONT_SCALES = {"Small": 0.9, "Normal": 1.0, "Large": 1.15}

ACCENT_ROLES = ("accent_start", "accent_end", "accent", "accent_end_hover", "accent_pressed")

# The colours currently in use (updated by apply_theme)
_current: dict = {}


# ==========================================================
# COLOUR HELPERS
# ==========================================================

def _rgb(hex_colour: str):
    hex_colour = hex_colour.lstrip("#")
    return tuple(int(hex_colour[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _hex(rgb) -> str:
    return "#" + "".join(f"{round(max(0, min(1, c)) * 255):02X}" for c in rgb)


def luminance(hex_colour: str) -> float:
    def channel(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in _rgb(hex_colour))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def _adjust(hex_colour: str, lightness=1.0, hue_shift=0.0) -> str:
    h, l, s = colorsys.rgb_to_hls(*_rgb(hex_colour))
    return _hex(colorsys.hls_to_rgb((h + hue_shift) % 1.0, max(0, min(1, l * lightness)), s))


def accent_from_colour(hex_colour: str):
    """Build the five accent shades from one chosen colour."""
    start = hex_colour.upper()
    # Darken until white text on it is readable
    for _ in range(20):
        if contrast(start, "#FFFFFF") >= 3.2:
            break
        start = _adjust(start, 0.92)
    end = _adjust(start, 1.0, 0.07)
    return (start, end, _adjust(start, 0.85), _adjust(end, 0.85), _adjust(start, 0.7))


# ==========================================================
# CURRENT SETTINGS
# ==========================================================

def _settings():
    """(theme name, accent name, custom colour, text scale) from Settings."""
    try:
        from services import settings_service
        values = settings_service.get_many(["theme", "accent_color", "custom_accent", "font_size"])
    except Exception:
        values = {}
    theme = values.get("theme") if values.get("theme") in THEMES else DEFAULT_THEME
    accent = values.get("accent_color") or THEME_DEFAULT_ACCENT
    custom = values.get("custom_accent") or "#2563EB"
    scale = FONT_SCALES.get(values.get("font_size"), 1.0)
    return theme, accent, custom, scale


def build_colours(theme: str, accent: str = THEME_DEFAULT_ACCENT, custom: str = "#2563EB") -> dict:
    """All colour roles for a theme + accent choice."""
    colours = dict(THEMES.get(theme, THEMES[DEFAULT_THEME]))

    if accent == CUSTOM_ACCENT and re.fullmatch(r"#[0-9A-Fa-f]{6}", custom or ""):
        shades = accent_from_colour(custom)
    else:
        name = accent if accent in ACCENTS else colours["accent"]
        shades = ACCENTS[name]

    colours.update(zip(ACCENT_ROLES, shades))
    colours["on_accent"] = "#FFFFFF"
    return colours


def theme_color(role: str) -> str:
    """Current colour for a role, e.g. theme_color("text") for icons."""
    if not _current:
        _current.update(build_colours(*_settings()[:3]))
    return _current.get(role, "#FFFFFF")


def is_dark() -> bool:
    if not _current:
        theme_color("text")
    return bool(_current.get("dark", True))


# ==========================================================
# APPLY
# ==========================================================

def _palette(c: dict) -> QPalette:
    """Palette so native parts (dialogs, popups) match the stylesheet."""
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(c["bg"]))
    palette.setColor(QPalette.WindowText, QColor(c["text"]))
    palette.setColor(QPalette.Base, QColor(c["bg"]))
    palette.setColor(QPalette.AlternateBase, QColor(c["surface"]))
    palette.setColor(QPalette.Text, QColor(c["text"]))
    palette.setColor(QPalette.Button, QColor(c["surface"]))
    palette.setColor(QPalette.ButtonText, QColor(c["text"]))
    palette.setColor(QPalette.Highlight, QColor(c["accent"]))
    palette.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))
    palette.setColor(QPalette.ToolTipBase, QColor(c["surface"]))
    palette.setColor(QPalette.ToolTipText, QColor(c["text"]))
    palette.setColor(QPalette.PlaceholderText, QColor(c["faint"]))
    palette.setColor(QPalette.Link, QColor(c["accent_start"]))
    return palette


def render_stylesheet(qss: str, colours: dict, scale: float = 1.0) -> str:
    """Fill in @roles and scale font sizes."""
    qss = re.sub(
        r"@([a-z_]+)\b",
        lambda m: colours.get(m.group(1), m.group(0)) if isinstance(colours.get(m.group(1)), str) else m.group(0),
        qss,
    )
    if scale != 1.0:
        qss = re.sub(
            r"font-size:\s*(\d+)px",
            lambda m: f"font-size: {max(8, round(int(m.group(1)) * scale))}px",
            qss,
        )
    return qss


def apply_theme(app: QApplication) -> None:
    """Apply the chosen theme, accent and text size to the whole app.

    Safe to call again after Settings > Appearance changes.
    """
    theme, accent, custom, scale = _settings()
    colours = build_colours(theme, accent, custom)

    _current.clear()
    _current.update(colours)

    app.setFont(QFont("Segoe UI", round(10 * scale)))
    app.setPalette(_palette(colours))

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

    app.setStyleSheet(render_stylesheet("\n".join(stylesheet), colours, scale))


def repolish(widget) -> None:
    """Re-apply the stylesheet after changing an object name or property."""
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.update()
