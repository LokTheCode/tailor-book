from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QMessageBox
)

from PySide6.QtGui import (
    QColor,
    QPixmap,
    QPalette,
    QBrush,
    QFont,
    QAction
)

from PySide6.QtCore import Qt, Signal

import qtawesome as qta

from services.user_service import UserService
from utils.screen import fit_to_screen
from utils.brand import app_icon, asset, logo_pixmap
from config import APP_NAME, APP_TAGLINE, APP_VERSION, APP_WEBSITE, SUPPORT_EMAIL, SUPPORT_PHONE
from datetime import date


class LoginWindow(QWidget):

    # Signal to notify main.py when login succeeds, passing the authenticated admin object
    login_successful = Signal(object)

    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(app_icon())
        # Fits any screen; AppManager then opens it maximised
        fit_to_screen(self, min_width=760, min_height=700)


        self.build_ui()


    def build_ui(self):
        self.create_background()
        self.create_overlay()
        self.create_login_card()
        self.create_header()
        self.create_login_form()
        self.create_social_section()
        self.create_footer()

    def create_background(self):
        palette = QPalette()
        bg = QPixmap(asset("assets/images/tailor_bg.png"))

        palette.setBrush(
            QPalette.Window,
            QBrush(
                bg.scaled(
                    self.size(),
                    Qt.IgnoreAspectRatio,
                    Qt.SmoothTransformation
                )
            )
        )

        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        palette = QPalette()
        bg = QPixmap(asset("assets/images/tailor_bg.png"))

        palette.setBrush(
            QPalette.Window,
            QBrush(
                bg.scaled(
                    self.size(),
                    Qt.IgnoreAspectRatio,
                    Qt.SmoothTransformation
                )
            )
        )

        self.setPalette(palette)
        self.overlay.setGeometry(self.rect())

    def create_overlay(self):
        self.overlay = QFrame(self)
        self.overlay.setObjectName("LoginOverlay")
        self.overlay.setGeometry(self.rect())

    def create_login_card(self):
        self.card = QFrame()
        self.card.setObjectName("LoginCard")
        self.card.setFixedSize(650, 660)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 12)
        shadow.setColor(QColor(0, 0, 0, 180))


        self.card.setGraphicsEffect(shadow)

        self.overlay_layout = QVBoxLayout(self.overlay)
        self.overlay_layout.setContentsMargins(0, 0, 0, 0)
        self.overlay_layout.setAlignment(Qt.AlignCenter)
        self.overlay_layout.addWidget(self.card)

        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setContentsMargins(50, 35, 50, 35)
        self.card_layout.setSpacing(10)
        self.card_layout.setAlignment(Qt.AlignTop)

    def create_header(self):
        logo = QLabel()
        logo.setPixmap(logo_pixmap(72))
        logo.setAlignment(Qt.AlignCenter)
        self.card_layout.addWidget(logo)
        self.card_layout.addSpacing(4)

        title = QLabel(f"Welcome to {APP_NAME}")
        title.setObjectName("LoginTitle")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.card_layout.addWidget(title)

        subtitle = QLabel(APP_TAGLINE)
        subtitle.setObjectName("LoginSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Segoe UI", 12))
        self.card_layout.addWidget(subtitle)

        self.card_layout.addSpacing(15)

    def create_login_form(self):
        # Divider
        divider = QLabel("──────────── Login ────────────")
        divider.setObjectName("LoginDivider")
        divider.setAlignment(Qt.AlignCenter)

        self.card_layout.addWidget(divider)
        self.card_layout.addSpacing(20)

        # ---------------- Email ----------------
        self.email = QLineEdit()
        self.email.setObjectName("Email")
        self.email.setPlaceholderText("Enter your email")
        self.email.setFixedHeight(50)

        email_icon = qta.icon("fa5s.envelope", color="#A7B0C3")
        self.email.addAction(
            QAction(email_icon, "", self),
            QLineEdit.LeadingPosition
        )

        self.card_layout.addWidget(self.email)
        self.card_layout.addSpacing(25)

        # ---------------- Password ----------------
        self.password = QLineEdit()
        self.password.setObjectName("Password")
        self.password.setPlaceholderText("Enter your password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFixedHeight(50)

        lock_icon = qta.icon("fa5s.lock", color="#A7B0C3")
        self.password.addAction(
            QAction(lock_icon, "", self),
            QLineEdit.LeadingPosition
        )

        self.eye_action = QAction(
            qta.icon("fa5s.eye", color="#A7B0C3"),
            "",
            self
        )
        self.eye_action.triggered.connect(self.toggle_password)

        self.password.addAction(
            self.eye_action,
            QLineEdit.TrailingPosition
        )

        # Allow pressing Enter in password field to trigger login
        self.password.returnPressed.connect(self.handle_login)

        self.card_layout.addWidget(self.password)
        self.card_layout.addSpacing(25)

        # ---------------- Remember ----------------
        row = QHBoxLayout()

        remember = QCheckBox("Remember Me")

        row.addWidget(remember)
        row.addStretch()

        forgot = QLabel("<a href='#'>Forgot Password?</a>")
        forgot.setObjectName("LoginLink")
        forgot.setOpenExternalLinks(False)
        forgot.linkActivated.connect(self.forgot_password)

        row.addWidget(forgot)

        self.card_layout.addLayout(row)
        self.card_layout.addSpacing(25)

        # ---------------- Login Button ----------------
        self.login_btn = QPushButton("LOGIN")
        self.login_btn.setObjectName("LoginButton")
        self.login_btn.setFixedHeight(55)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        
        # Connect click event to backend handler
        self.login_btn.clicked.connect(self.handle_login)

        self.card_layout.addWidget(self.login_btn)
        self.card_layout.addSpacing(25)

    def handle_login(self):
        """Authenticates input against database via AuthService."""
        email_str = self.email.text().strip()
        password_str = self.password.text().strip()

        if not email_str or not password_str:
            QMessageBox.warning(
                self, 
                "Input Error", 
                "Please enter both Email and Password."
            )
            return

        # Query backend database
        # Returns a user dict (id, name, email, role, permissions) or None
        admin = UserService.authenticate(email_str, password_str)

        if admin:
            # Broadcast successful authentication signal
            self.login_successful.emit(admin)
        else:
            QMessageBox.critical(
                self, 
                "Login Failed", 
                "Invalid Email or Password. Please try again."
            )

    def toggle_password(self):
        if self.password.echoMode() == QLineEdit.Password:
            self.password.setEchoMode(QLineEdit.Normal)
            self.eye_action.setIcon(
                qta.icon("fa5s.eye-slash", color="#A7B0C3")
            )
        else:
            self.password.setEchoMode(QLineEdit.Password)
            self.eye_action.setIcon(
                qta.icon("fa5s.eye", color="#A7B0C3")
            )

    def create_social_section(self):
        """Product support details (config.py), shown when filled in."""
        self.card_layout.addStretch()

        contacts = [x for x in (SUPPORT_PHONE, SUPPORT_EMAIL, APP_WEBSITE) if x]
        if not contacts:
            return

        support = QLabel("Need help?  " + "  ·  ".join(contacts))
        support.setObjectName("LoginFooter")
        support.setAlignment(Qt.AlignCenter)
        support.setWordWrap(True)
        support.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.card_layout.addWidget(support)

    def forgot_password(self, *_):
        QMessageBox.information(
            self,
            "Forgot password",
            "Ask your shop's main administrator to set a new password for you "
            "in Users (edit your account and type a new password).\n\n"
            "If you are the main administrator and can't log in, contact "
            f"{APP_NAME} support"
            + (f": {SUPPORT_PHONE or SUPPORT_EMAIL}" if (SUPPORT_PHONE or SUPPORT_EMAIL) else ".")
        )

    def create_footer(self):
        footer = QLabel(f"© {date.today().year} {APP_NAME}  ·  Version {APP_VERSION}")
        footer.setAlignment(Qt.AlignCenter)
        footer.setObjectName("LoginFooter")
        self.card_layout.addSpacing(20)
        self.card_layout.addWidget(footer)