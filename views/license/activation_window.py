"""Activation screen shown before login until this PC has a license."""

from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtGui import QAction, QDesktopServices, QFont
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton

import qtawesome as qta

from config import APP_NAME, SUPPORT_EMAIL, SUPPORT_PHONE
from services import license_service
from utils.background import run_in_background
from views.login.login_window import LoginWindow


class ActivationWindow(LoginWindow):
    """Same look as the login screen, with a license key field instead."""

    activated = Signal(object)

    def __init__(self, message=""):
        super().__init__()
        if message:
            self.show_error(message)

    def build_ui(self):
        self.create_background()
        self.create_overlay()
        self.create_login_card()
        self.create_header()
        self.create_activation_form()
        self.create_social_section()
        self.create_footer()

    def create_activation_form(self):
        divider = QLabel("──────── Activate your copy ────────")
        divider.setObjectName("LoginDivider")
        divider.setAlignment(Qt.AlignCenter)
        self.card_layout.addWidget(divider)
        self.card_layout.addSpacing(12)

        intro = QLabel(
            "Enter the license key from your purchase email. Each key works on one computer."
        )
        intro.setObjectName("LoginSubtitle")
        intro.setWordWrap(True)
        intro.setAlignment(Qt.AlignCenter)
        self.card_layout.addWidget(intro)
        self.card_layout.addSpacing(16)

        self.key_input = QLineEdit()
        self.key_input.setObjectName("Email")
        self.key_input.setPlaceholderText("TB-XXXXX-XXXXX-XXXXX-XXXXX")
        self.key_input.setFixedHeight(50)
        self.key_input.setFont(QFont("Consolas", 13))
        self.key_input.addAction(
            QAction(qta.icon("fa5s.key", color="#A7B0C3"), "", self),
            QLineEdit.LeadingPosition,
        )
        self.key_input.returnPressed.connect(self.handle_activate)
        self.card_layout.addWidget(self.key_input)
        self.card_layout.addSpacing(10)

        self.status = QLabel("")
        self.status.setObjectName("LoginSubtitle")
        self.status.setWordWrap(True)
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setMinimumHeight(44)
        self.card_layout.addWidget(self.status)
        self.card_layout.addSpacing(6)

        self.activate_btn = QPushButton("ACTIVATE")
        self.activate_btn.setObjectName("LoginButton")
        self.activate_btn.setFixedHeight(55)
        self.activate_btn.setCursor(Qt.PointingHandCursor)
        self.activate_btn.clicked.connect(self.handle_activate)
        self.card_layout.addWidget(self.activate_btn)
        self.card_layout.addSpacing(16)

        links = QHBoxLayout()
        buy = QLabel("<a href='buy'>Don't have a key? Buy a license</a>")
        buy.setObjectName("LoginLink")
        buy.linkActivated.connect(self.open_buy_page)
        links.addStretch()
        links.addWidget(buy)
        links.addStretch()
        self.card_layout.addLayout(links)

        if not license_service.configured():
            self.show_error(
                "This copy of the app has no license server set up. "
                "Please download the installer again from the official website."
            )
            self.activate_btn.setEnabled(False)

    def show_error(self, text):
        self.status.setStyleSheet("color: #F87171;")
        self.status.setText(text)

    def handle_activate(self):
        key = self.key_input.text()
        if not license_service.normalize_key(key):
            self.show_error("That doesn't look like a license key. It should look like TB-XXXXX-XXXXX-XXXXX-XXXXX.")
            return

        self.activate_btn.setEnabled(False)
        self.activate_btn.setText("ACTIVATING...")
        self.status.setStyleSheet("")
        self.status.setText("Contacting the license server...")
        run_in_background(lambda: license_service.activate(key), self.on_activated, self.on_failed)

    def on_activated(self, license_):
        self.activate_btn.setText("ACTIVATED")
        self.activated.emit(license_)

    def on_failed(self, error):
        self.activate_btn.setEnabled(True)
        self.activate_btn.setText("ACTIVATE")
        if isinstance(error, license_service.LicenseError):
            message = str(error)
            if error.code == "in_use":
                contact = SUPPORT_PHONE or SUPPORT_EMAIL
                if contact:
                    message += f" ({contact})"
        else:
            message = f"Activation failed: {error}"
        self.show_error(message)

    def open_buy_page(self, *_):
        url = license_service.buy_url()
        if url:
            QDesktopServices.openUrl(QUrl(url))
        else:
            self.show_error(f"Contact {APP_NAME} support to buy a license.")
