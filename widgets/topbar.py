from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QLineEdit,
    QMenu,
    QSizePolicy
)

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

import qtawesome as qta
from utils.theme import theme_color
from datetime import datetime


class TopBar(QWidget):

    changePasswordClicked = Signal()
    logoutClicked = Signal()

    def __init__(self):
        super().__init__()

        self.setObjectName("TopBar")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedHeight(75)

        self.build_ui()

    # ----------------------------------------------------

    def build_ui(self):


        layout = QHBoxLayout(self)

        layout.setContentsMargins(25, 10, 25, 10)

        layout.setSpacing(15)

        # ------------------------------------------------
        # Title
        # ------------------------------------------------

        # self.title = QLabel("Dashboard")

        # self.title.setObjectName("TopBarTitle")

        # self.title.setFont(QFont("Segoe UI", 18, QFont.Bold))

        # layout.addWidget(self.title)

        layout.addSpacing(25)

        # ------------------------------------------------
        # Search Box
        # ------------------------------------------------

        self.search = QLineEdit()

        self.search.setObjectName("TopBarSearch")

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

        self.dateLabel.setObjectName("TopBarDate")

        layout.addWidget(self.dateLabel)

        # ------------------------------------------------
        # Notification
        # ------------------------------------------------

        self.notificationBtn = QPushButton()

        self.notificationBtn.setIcon(

            qta.icon(
                "fa5s.bell",
                color=theme_color("text")
            )

        )

        self.notificationBtn.setObjectName("IconButton")
        self.notificationBtn.setFixedSize(42,42)

        layout.addWidget(self.notificationBtn)

        # ------------------------------------------------
        # Profile
        # ------------------------------------------------

        self.profileBtn = QPushButton("Admin")
        

        self.profileBtn.setObjectName("Primary")

        self.profileBtn.setIcon(

            qta.icon(
                "fa5s.user-circle",
                color="white"
            )

        )

        self.profileBtn.setFixedHeight(42)

        self.profileBtn.setCursor(Qt.PointingHandCursor)

        # Profile menu: change password / logout
        menu = QMenu(self.profileBtn)

        change_password = menu.addAction(
            qta.icon("fa5s.key", color=theme_color("text_label")),
            "Change Password"
        )
        change_password.triggered.connect(self.changePasswordClicked.emit)

        menu.addSeparator()

        logout = menu.addAction(
            qta.icon("fa5s.sign-out-alt", color="#F87171"),
            "Logout"
        )
        logout.triggered.connect(self.logoutClicked.emit)

        self.profileBtn.setMenu(menu)
        self.profileBtn.setProperty("hasMenu", True)

        layout.addWidget(self.profileBtn)

    # ----------------------------------------------------

    # def setTitle(self, title):

    #     self.title.setText(title)

    # ----------------------------------------------------

    def set_user(self, user):
        """Show the logged-in user's name and role on the profile button."""
        name = user.get("name") or "User"
        role = user.get("role_label", "")
        self.profileBtn.setText(f" {name}")
        self.profileBtn.setToolTip(f"{user.get('email', '')}\n{role}".strip())
