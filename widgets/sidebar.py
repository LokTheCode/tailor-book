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

        self.setFixedWidth(250)

        self.buttons = {}

        self.build_ui()

    # ------------------------------------------------------

    def build_ui(self):

        self.setStyleSheet("""
        

        QLabel#Logo{
            color:#ffffff;
            font-size:22px;
            font-weight:bold;
            padding:20px;
            text-transform:uppercase;
        }

        QPushButton{

            background:transparent;

            color:white;

            border:none;

            text-align:left;

            padding:14px 20px;

            font-size:15px;

            border-radius:10px;

        }

        QPushButton:hover{

            background:qlineargradient(
                x1:0,y1:0,
                x2:1,y2:0,
                stop:0 #3B82F6,
                stop:1 #8B5CF6
            );

            color:white;

        }

        QPushButton#Active{

            background:qlineargradient(
                x1:0,y1:0,
                x2:1,y2:0,
                stop:0 #3B82F6,
                stop:1 #8B5CF6
            );

            color:white;

            font-weight:bold;

        }

        """)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(15,20,15,20)

        layout.setSpacing(10)

        logo = QLabel("Dev Tailor ERP")

        logo.setObjectName("Logo")

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

                button.setObjectName("Active")

                button.setActive(True)

            else:

                button.setObjectName("")

                button.setActive(False)

            button.style().unpolish(button)
            button.style().polish(button)
            button.update()