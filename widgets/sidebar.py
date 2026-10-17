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

    dashboardClicked = Signal()
    customerClicked = Signal()
    measurementClicked = Signal()
    orderClicked = Signal()
    inventoryClicked = Signal()
    reportClicked = Signal()
    settingClicked = Signal()
    logoutClicked = Signal()

    def __init__(self):
        super().__init__()

        self.setObjectName("Sidebar")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedWidth(250)

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

        self.add_menu(layout,"Dashboard","fa5s.home",self.dashboardClicked)

        self.add_menu(layout,"Customers","fa5s.users",self.customerClicked)

        self.add_menu(layout,"Measurements","fa5s.ruler",self.measurementClicked)

        self.add_menu(layout,"Orders","fa5s.clipboard-list",self.orderClicked)

        self.add_menu(layout,"Inventory","fa5s.boxes",self.inventoryClicked)

        self.add_menu(layout,"Reports","fa5s.chart-line",self.reportClicked)

        self.add_menu(layout,"Settings","fa5s.cog",self.settingClicked)

        layout.addStretch()

        self.add_menu(layout,"Logout","fa5s.sign-out-alt",self.logoutClicked)

        self.set_active("Dashboard")

    # ------------------------------------------------------

    def add_menu(self, layout, text, icon_name, signal):

        btn = HoverButton(text, icon_name)

        btn.clicked.connect(signal.emit)

        btn.clicked.connect(
            lambda _, name=text: self.set_active(name)
        )

        layout.addWidget(btn)

        self.buttons[text] = btn

    # ------------------------------------------------------

    def set_active(self, menu_name):

        for name, button in self.buttons.items():

            if name == menu_name:

                button.setProperty("active", True)

                button.setActive(True)

            else:

                button.setProperty("active", False)

                button.setActive(False)

            button.style().unpolish(button)
            button.style().polish(button)
            button.update()