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

from config import DEBUG
from utils.style_loader import load_style
from services.auth_service import AuthService


class LoginWindow(QWidget):

    # Signal to notify main.py when login succeeds, passing the authenticated admin object
    login_successful = Signal(object)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dev Tailor ERP")
        self.resize(1600, 850)

        self.debug = DEBUG

        self.build_ui()

        if self.debug:
            load_style(self, "assets/styles/debug.qss")
        else:
            load_style(self, "assets/styles/login.qss")

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
        bg = QPixmap("assets/images/tailor_bg.png")

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
        bg = QPixmap("assets/images/tailor_bg.png")

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
        self.overlay.setGeometry(self.rect())
        self.overlay.setStyleSheet("""
        background:qlineargradient(
            x1:0, y1:0, x2:1, y2:1,
            stop:0 rgba(20,35,90,180),
            stop:1 rgba(90,30,150,180)
        );
        """)

    def create_login_card(self):
        self.card = QFrame()
        self.card.setObjectName("LoginCard")
        self.card.setFixedSize(650, 660)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 12)
        shadow.setColor(QColor(0, 0, 0, 180))

        self.card.setStyleSheet("""
        QFrame{
            background:rgba(22,25,40,225);
            border-radius:22px;
        }
        """)

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
        title = QLabel("Welcome to Dev Tailor")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.card_layout.addWidget(title)

        subtitle = QLabel("Smart Tailoring Management System")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Segoe UI", 12))
        self.card_layout.addWidget(subtitle)

        self.card_layout.addSpacing(15)

    def create_login_form(self):
        # Divider
        divider = QLabel("──────────── Login ────────────")
        divider.setAlignment(Qt.AlignCenter)
        divider.setStyleSheet("color:#9096A5;font-size:14px;")

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
        remember.setStyleSheet("""
            color:white;
            font-size:13px;
        """)

        row.addWidget(remember)
        row.addStretch()

        forgot = QLabel("<a href='#'>Forgot Password?</a>")
        forgot.setOpenExternalLinks(False)
        forgot.setStyleSheet("""
            color:#6D8DFF;
            font-size:13px;
        """)

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
        admin = AuthService.authenticate_user(email_str, password_str)

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
        self.card_layout.addStretch()

        divider = QLabel("──────────── OR ────────────")
        divider.setAlignment(Qt.AlignCenter)
        divider.setStyleSheet("color:#9096A5;font-size:14px;")
        self.card_layout.addWidget(divider)

        title = QLabel("Connect With Us")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color:#C8CDD9;
            font-size:13px;
        """)
        self.card_layout.addWidget(title)
        self.card_layout.addSpacing(15)

        social = QHBoxLayout()
        social.setSpacing(20)
        social.setAlignment(Qt.AlignCenter)

        icons = [
            ("fa5b.facebook-f", "#1877F2"),
            ("fa5b.instagram", "#E4405F"),
            ("fa5b.linkedin-in", "#0A66C2"),
            ("fa5s.globe", "#10B981")
        ]

        for icon_name, color in icons:
            btn = QPushButton()
            btn.setFixedSize(48, 48)
            btn.setIcon(
                qta.icon(icon_name, color="white")
            )
            btn.setIconSize(btn.size() * 0.45)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background:{color};
                    border:none;
                    border-radius:24px;
                }}
                QPushButton:hover {{
                    background:white;
                    color:{color};
                    border:2px solid {color};
                }}
            """)

            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(18)
            shadow.setOffset(0, 4)
            shadow.setColor(QColor(0, 0, 0, 120))

            btn.setGraphicsEffect(shadow)
            social.addWidget(btn)

        self.card_layout.addLayout(social)
        self.card_layout.addSpacing(20)

    def create_footer(self):
        footer = QLabel("© 2026 Dev Tailor ERP")
        footer.setStyleSheet("""
            color:#C8CDD9;
            font-size:13px;
        """)
        footer.setAlignment(Qt.AlignCenter)
        footer.setObjectName("Footer")
        self.card_layout.addSpacing(20)
        self.card_layout.addWidget(footer)