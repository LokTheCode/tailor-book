from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def load_style(widget, file):
    style_path = BASE_DIR / file

    with open(style_path, "r", encoding="utf8") as f:
        widget.setStyleSheet(f.read())