from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout
)

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

import qtawesome as qta


# ==========================================================
# Hover Button
# ==========================================================

class HoverButton(QPushButton):

    def __init__(self, text, icon_name):
        super().__init__("   " + text)

        self.icon_name = icon_name
        self.active = False

        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName("MenuButton")
        self.setProperty("active", False)
        self.setMinimumHeight(48)

        self.update_icon()

    def update_icon(self):

        color = "white"

        self.setIcon(
            qta.icon(
                self.icon_name,
                color=color
            )
        )

    def enterEvent(self, event):

        if not self.active:
            self.setIcon(
                qta.icon(
                    self.icon_name,
                    color="white"
                )
            )

        super().enterEvent(event)

    def leaveEvent(self, event):

        if not self.active:
            self.setIcon(
                qta.icon(
                    self.icon_name,
                    color="white"
                )
            )

        super().leaveEvent(event)

    def setActive(self, value):

        self.active = value
        self.update_icon()


# ==========================================================
# Sidebar
# ==========================================================

class Sidebar(QWidget):

    # Emits the page key, e.g. "customers" (see services/user_service.PAGES)
    pageClicked = Signal(str)
    logoutClicked = Signal()

    # page key -> (label, icon), in display order
    MENU = [
        ("dashboard", "Dashboard", "fa5s.home"),
        ("customers", "Customers", "fa5s.users"),
        ("measurements", "Measurements", "fa5s.ruler"),
        ("orders", "Orders", "fa5s.clipboard-list"),
        ("inventory", "Inventory", "fa5s.boxes"),
        ("reports", "Reports", "fa5s.chart-line"),
        ("users", "Users", "fa5s.user-shield"),
        ("settings", "Settings", "fa5s.cog"),
    ]

    def __init__(self, allowed_pages=None):
        """allowed_pages: page keys to show. None shows every page."""
        super().__init__()

        self.setObjectName("Sidebar")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedWidth(250)

        self.allowed_pages = allowed_pages
        self.buttons = {}

        self.build_ui()

    # ------------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(15,20,15,20)

        layout.setSpacing(10)

        logo = QLabel("Dev Tailor ERP")

        logo.setObjectName("SidebarLogo")

        logo.setAlignment(Qt.AlignCenter)

        logo.setFont(QFont("Segoe UI",16,QFont.Bold))

        layout.addWidget(logo)

        layout.addSpacing(20)

        for key, label, icon in self.MENU:
            if self.allowed_pages is None or key in self.allowed_pages:
                self.add_menu(layout, key, label, icon)

        layout.addStretch()

        logout = HoverButton("Logout", "fa5s.sign-out-alt")
        logout.clicked.connect(self.logoutClicked.emit)
        layout.addWidget(logout)

    # ------------------------------------------------------

    def add_menu(self, layout, key, text, icon_name):

        btn = HoverButton(text, icon_name)

        btn.clicked.connect(
            lambda _=False, page=key: self.pageClicked.emit(page)
        )

        layout.addWidget(btn)

        self.buttons[key] = btn

    # ------------------------------------------------------

    def set_active(self, page_key):

        for key, button in self.buttons.items():

            active = key == page_key

            button.setProperty("active", active)

            button.setActive(active)

            button.style().unpolish(button)
            button.style().polish(button)
            button.update()
