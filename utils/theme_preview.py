"""Small preview pictures for Settings > Appearance."""

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QLinearGradient, QPainter, QPen, QPixmap

from utils.theme import build_colours


def theme_preview(theme: str, accent: str, custom: str, width=200, height=120) -> QPixmap:
    """A tiny drawing of the app in the given theme: sidebar, top bar, card."""
    c = build_colours(theme, accent, custom)

    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.transparent)

    p = QPainter(pixmap)
    p.setRenderHint(QPainter.Antialiasing)
    p.setPen(Qt.NoPen)

    # Window background
    p.setBrush(QColor(c["bg"]))
    p.drawRoundedRect(QRectF(0, 0, width, height), 10, 10)

    # Sidebar with menu lines and an active item
    side_w = width * 0.26
    p.setBrush(QColor(c["sidebar_bg"]))
    p.drawRoundedRect(QRectF(0, 0, side_w, height), 10, 10)
    p.drawRect(QRectF(side_w - 10, 0, 10, height))

    gradient = QLinearGradient(0, 0, side_w, 0)
    gradient.setColorAt(0, QColor(c["accent_start"]))
    gradient.setColorAt(1, QColor(c["accent_end"]))
    p.setBrush(QBrush(gradient))
    p.drawRoundedRect(QRectF(7, 30, side_w - 14, 12), 4, 4)

    p.setBrush(QColor(c["sidebar_text"]))
    for i in range(4):
        p.drawRoundedRect(QRectF(10, 52 + i * 15, side_w * 0.55, 5), 2, 2)

    # Top bar
    p.setBrush(QColor(c["topbar_bg"]))
    p.drawRect(QRectF(side_w, 0, width - side_w, 20))
    p.setPen(QPen(QColor(c["border"]), 1))
    p.drawLine(int(side_w), 20, width, 20)
    p.setPen(Qt.NoPen)

    # Card with title, text lines and a button
    card = QRectF(side_w + 10, 30, width - side_w - 20, height - 40)
    p.setBrush(QColor(c["surface"]))
    p.setPen(QPen(QColor(c["border"]), 1))
    p.drawRoundedRect(card, 8, 8)
    p.setPen(Qt.NoPen)

    p.setBrush(QColor(c["text"]))
    p.drawRoundedRect(QRectF(card.x() + 10, card.y() + 10, card.width() * 0.5, 6), 3, 3)
    p.setBrush(QColor(c["muted"]))
    p.drawRoundedRect(QRectF(card.x() + 10, card.y() + 24, card.width() * 0.75, 4), 2, 2)
    p.drawRoundedRect(QRectF(card.x() + 10, card.y() + 34, card.width() * 0.6, 4), 2, 2)

    button = QRectF(card.right() - 52, card.bottom() - 22, 42, 13)
    gradient = QLinearGradient(button.left(), 0, button.right(), 0)
    gradient.setColorAt(0, QColor(c["accent_start"]))
    gradient.setColorAt(1, QColor(c["accent_end"]))
    p.setBrush(QBrush(gradient))
    p.drawRoundedRect(button, 5, 5)

    p.setBrush(QColor(c["success_text"]))
    p.drawEllipse(QRectF(card.x() + 10, card.bottom() - 20, 9, 9))

    p.end()
    return pixmap


def accent_swatch(start: str, end: str, size=30) -> QPixmap:
    """A round colour swatch (gradient from start to end)."""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.Antialiasing)
    gradient = QLinearGradient(0, 0, size, size)
    gradient.setColorAt(0, QColor(start))
    gradient.setColorAt(1, QColor(end))
    p.setBrush(QBrush(gradient))
    p.setPen(QPen(QColor(0, 0, 0, 60), 1))
    p.drawEllipse(QRectF(1, 1, size - 2, size - 2))
    p.end()
    return pixmap
