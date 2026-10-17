from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from services.user_service import MIN_PASSWORD_LENGTH, UserError, UserService


class ChangePasswordDialog(QDialog):
    """Lets the logged-in user change their own password."""

    def __init__(self, user, parent=None):
        super().__init__(parent)

        self.user = user

        self.setWindowTitle("Change Password")
        self.setMinimumWidth(440)

        self.build_ui()

    def build_ui(self):

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        title = QLabel("Change Password")
        title.setObjectName("CardTitle")
        root.addWidget(title)

        subtitle = QLabel(f"Signed in as {self.user.get('email', '')}")
        subtitle.setObjectName("MutedText")
        root.addWidget(subtitle)

        form = QFormLayout()
        form.setSpacing(12)

        self.current = QLineEdit()
        self.new = QLineEdit()
        self.confirm = QLineEdit()

        self.new.setPlaceholderText(f"At least {MIN_PASSWORD_LENGTH} characters")

        for field in (self.current, self.new, self.confirm):
            field.setEchoMode(QLineEdit.Password)

        form.addRow(self._label("Current password"), self.current)
        form.addRow(self._label("New password"), self.new)
        form.addRow(self._label("Confirm new"), self.confirm)

        root.addLayout(form)

        show = QCheckBox("Show passwords")
        show.toggled.connect(self.toggle_visible)
        root.addWidget(show)

        buttons = QHBoxLayout()
        buttons.addStretch()

        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.reject)

        save = QPushButton("Change Password")
        save.setObjectName("Primary")
        save.setDefault(True)
        save.clicked.connect(self.save)

        buttons.addWidget(cancel)
        buttons.addWidget(save)

        root.addLayout(buttons)

    def _label(self, text):
        label = QLabel(text)
        label.setObjectName("FieldLabel")
        return label

    def toggle_visible(self, visible):
        mode = QLineEdit.Normal if visible else QLineEdit.Password
        for field in (self.current, self.new, self.confirm):
            field.setEchoMode(mode)

    def save(self):

        try:
            UserService.change_own_password(
                self.user["id"],
                self.current.text(),
                self.new.text(),
                self.confirm.text(),
            )
        except UserError as error:
            QMessageBox.warning(self, "Can't change password", str(error))
            return

        QMessageBox.information(self, "Password changed", "Your password has been updated.")
        self.accept()
