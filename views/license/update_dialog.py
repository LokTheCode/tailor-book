"""'A new version is available' dialog: shows release notes and opens the download."""

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QDialog, QDialogButtonBox, QLabel, QMessageBox, QPushButton, QTextEdit, QVBoxLayout,
)

from config import APP_NAME, APP_VERSION
from services import license_service
from utils.background import run_in_background


class UpdateDialog(QDialog):

    def __init__(self, info, parent=None):
        super().__init__(parent)
        self.info = info
        self.setWindowTitle("Update available")
        self.setMinimumWidth(480)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 18)
        layout.setSpacing(12)

        title = QLabel(f"{APP_NAME} {info.get('version')} is available")
        title.setObjectName("SectionTitle")
        title.setStyleSheet("font-size: 18px; font-weight: 700;")
        layout.addWidget(title)

        details = f"You have version {APP_VERSION}."
        if info.get("released"):
            details += f" The new version was released on {info['released']}"
            details += f" ({info['size_mb']} MB)." if info.get("size_mb") else "."
        layout.addWidget(QLabel(details))

        if info.get("notes"):
            notes = QTextEdit()
            notes.setReadOnly(True)
            notes.setPlainText(info["notes"])
            notes.setMaximumHeight(180)
            layout.addWidget(QLabel("What's new:"))
            layout.addWidget(notes)

        how = QLabel(
            "Click Download to get the installer in your browser. When it has downloaded, "
            f"close {APP_NAME} and run the installer. Your customers, orders and settings are kept."
        )
        how.setWordWrap(True)
        layout.addWidget(how)

        buttons = QDialogButtonBox()
        self.download_btn = QPushButton(" Download update")
        self.download_btn.setObjectName("Primary")
        self.download_btn.setCursor(Qt.PointingHandCursor)
        buttons.addButton(self.download_btn, QDialogButtonBox.AcceptRole)
        later = buttons.addButton("Later", QDialogButtonBox.RejectRole)
        later.setCursor(Qt.PointingHandCursor)
        self.download_btn.clicked.connect(self.download)
        later.clicked.connect(self.reject)
        layout.addWidget(buttons)

    def download(self):
        self.download_btn.setEnabled(False)
        self.download_btn.setText(" Getting your download link...")
        run_in_background(license_service.download_link, self.open_link, self.failed)

    def open_link(self, url):
        QDesktopServices.openUrl(QUrl(url))
        self.accept()

    def failed(self, error):
        self.download_btn.setEnabled(True)
        self.download_btn.setText(" Download update")
        QMessageBox.warning(
            self,
            "Download",
            f"{error}\n\nYou can also download the update from our website with your email and license key.",
        )
        page = self.info.get("download_page")
        if page:
            QDesktopServices.openUrl(QUrl(page))
