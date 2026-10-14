from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QLineEdit,
    QSizePolicy
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

import qtawesome as qta
from datetime import datetime


class TopBar(QWidget):

    def __init__(self):
        super().__init__()

        self.setFixedHeight(75)

        self.build_ui()

    # ----------------------------------------------------

    def build_ui(self):

        self.setStyleSheet("""

       

        QLabel#Title{

            color:#ffffff;

            font-size:24px;

            font-weight:bold;

        }

        QLabel#Date{

            color:#ffffff;

            font-size:16px;

        }

        

        QLineEdit#Search{
            border-bottom:1px solid #D1D5DB;
            border-radius:10px;
            padding-left:10px;
            font-size:14px;
            color:#FFFFFF;
        }

        QLineEdit:focus{

            border:2px solid #3B82F6;

        }

        QPushButton{

            background:qlineargradient(
                x1:0,y1:0,
                x2:1,y2:0,
                stop:0 #3B82F6,
                stop:1 #8B5CF6
            );

            border:none;

            border-radius:8px;

            padding:8px;

        }

        QPushButton:hover{

            background:#F3F4F6;

        }

        QPushButton#Profile{

            background:#2563EB;

            color:white;

            font-weight:bold;

            padding:10px 18px;

            border-radius:10px;

        }

        QPushButton#Profile:hover{

            background:#1D4ED8;

        }

        """)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(25, 10, 25, 10)

        layout.setSpacing(15)

        # ------------------------------------------------
        # Title
        # ------------------------------------------------

        # self.title = QLabel("Dashboard")

        # self.title.setObjectName("Title")

        # self.title.setFont(QFont("Segoe UI", 18, QFont.Bold))

        # layout.addWidget(self.title)

        layout.addSpacing(25)

        # ------------------------------------------------
        # Search Box
        # ------------------------------------------------

        self.search = QLineEdit()

        self.search.setObjectName("Search")

        self.search.setPlaceholderText(
            "Search Customer / Measurement / Order..."
        )

        self.search.setFixedHeight(42)

        self.search.setMinimumWidth(320)

        search_icon = qta.icon(
            "fa5s.search",
            color="#6B7280"
        )

        self.search.addAction(
            search_icon,
            QLineEdit.LeadingPosition
        )

        layout.addWidget(self.search)

        layout.addStretch()

        # ------------------------------------------------
        # Today's Date
        # ------------------------------------------------

        today = datetime.now().strftime("%d %b %Y")

        self.dateLabel = QLabel(today)

        self.dateLabel.setObjectName("Date")

        layout.addWidget(self.dateLabel)

        # ------------------------------------------------
        # Notification
        # ------------------------------------------------

        self.notificationBtn = QPushButton()

        self.notificationBtn.setIcon(

            qta.icon(
                "fa5s.bell",
                color="#ffffff"
            )

        )

        self.notificationBtn.setFixedSize(42,42)

        layout.addWidget(self.notificationBtn)

        # ------------------------------------------------
        # Profile
        # ------------------------------------------------

        self.profileBtn = QPushButton("Admin")
        

        self.profileBtn.setObjectName("Profile")

        self.profileBtn.setIcon(

            qta.icon(
                "fa5s.user-circle",
                color="white"
            )

        )

        self.profileBtn.setFixedHeight(42)

        layout.addWidget(self.profileBtn)

    # ----------------------------------------------------

    # def setTitle(self, title):

    #     self.title.setText(title)