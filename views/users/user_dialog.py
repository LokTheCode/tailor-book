from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from services.user_service import (
    DEFAULT_ACCESS,
    PAGES,
    ROLE_LABELS,
    SUB_ADMIN,
    UserError,
    UserService,
    manageable_roles,
)


class UserDialog(QDialog):
    """Add or edit an admin / sub-admin, including their page access."""

    def __init__(self, actor, user=None, parent=None):
        super().__init__(parent)

        self.actor = actor
        self.user = user            # None = add new user
        self.saved_user = None

        self.setWindowTitle("Edit User" if user else "Add User")
        self.setMinimumWidth(520)

        self.build_ui()
        self.load()

    # ======================================================
    # UI
    # ======================================================

    def build_ui(self):

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        title = QLabel("Edit User" if self.user else "Add User")
        title.setObjectName("CardTitle")
        root.addWidget(title)

        # --------------------------------------------------
        # Details
        # --------------------------------------------------

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.name = QLineEdit()
        self.name.setPlaceholderText("Full name")

        self.email = QLineEdit()
        self.email.setPlaceholderText("name@example.com")

        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Optional")

        self.role = QComboBox()
        for role in manageable_roles(self.actor):
            self.role.addItem(ROLE_LABELS[role], role)
        self.role.currentIndexChanged.connect(self.role_changed)

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        self.confirm = QLineEdit()
        self.confirm.setEchoMode(QLineEdit.Password)

        if self.user:
            self.password.setPlaceholderText("Leave blank to keep current password")
            self.confirm.setPlaceholderText("Leave blank to keep current password")
        else:
            self.password.setPlaceholderText("At least 8 characters")
            self.confirm.setPlaceholderText("Type the password again")

        form.addRow(self._label("Name"), self.name)
        form.addRow(self._label("Email"), self.email)
        form.addRow(self._label("Phone"), self.phone)
        form.addRow(self._label("Role"), self.role)
        form.addRow(self._label("Password"), self.password)
        form.addRow(self._label("Confirm"), self.confirm)

        root.addLayout(form)

        # --------------------------------------------------
        # Access
        # --------------------------------------------------

        access_card = QFrame()
        access_card.setObjectName("InnerPanel")

        access_layout = QVBoxLayout(access_card)
        access_layout.setContentsMargins(16, 14, 16, 14)
        access_layout.setSpacing(10)

        access_title = QLabel("Page access")
        access_title.setObjectName("FieldLabel")
        access_layout.addWidget(access_title)

        access_hint = QLabel("Tick the pages this user can open.")
        access_hint.setObjectName("MutedText")
        access_layout.addWidget(access_hint)

        grid = QGridLayout()
        grid.setHorizontalSpacing(24)
        grid.setVerticalSpacing(8)

        self.access_boxes = {}
        for index, (key, label) in enumerate(PAGES.items()):
            box = QCheckBox(label)
            self.access_boxes[key] = box
            grid.addWidget(box, index // 2, index % 2)

        access_layout.addLayout(grid)

        self.users_hint = QLabel("Sub admins can't manage users.")
        self.users_hint.setObjectName("MutedText")
        access_layout.addWidget(self.users_hint)

        root.addWidget(access_card)

        # --------------------------------------------------
        # Status
        # --------------------------------------------------

        self.active = QCheckBox("Active (can log in)")
        self.active.setChecked(True)
        root.addWidget(self.active)

        # --------------------------------------------------
        # Buttons
        # --------------------------------------------------

        buttons = QHBoxLayout()
        buttons.addStretch()

        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.reject)

        save = QPushButton("Save User")
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

    # ======================================================
    # DATA
    # ======================================================

    def load(self):

        if not self.user:
            self.role_changed(apply_defaults=True)
            return

        self.name.setText(self.user["name"])
        self.email.setText(self.user["email"])
        self.phone.setText(self.user["phone"])

        index = self.role.findData(self.user["role"])
        if index >= 0:
            self.role.blockSignals(True)
            self.role.setCurrentIndex(index)
            self.role.blockSignals(False)

        for key, box in self.access_boxes.items():
            box.setChecked(key in self.user["permissions"])

        self.active.setChecked(self.user["is_active"])

        # Nobody can deactivate themselves
        if self.user["id"] == self.actor.get("id"):
            self.active.setEnabled(False)

        self.role_changed(apply_defaults=False)

    def role_changed(self, *_args, apply_defaults=None):

        role = self.role.currentData()

        # When adding a user, switching role resets ticks to that role's defaults
        if apply_defaults is None:
            apply_defaults = self.user is None

        if apply_defaults and role in DEFAULT_ACCESS:
            for key, box in self.access_boxes.items():
                box.setChecked(key in DEFAULT_ACCESS[role])

        is_sub_admin = role == SUB_ADMIN
        users_box = self.access_boxes["users"]
        users_box.setEnabled(not is_sub_admin)
        if is_sub_admin:
            users_box.setChecked(False)
        self.users_hint.setVisible(is_sub_admin)

    def save(self):

        password = self.password.text()

        if password != self.confirm.text():
            QMessageBox.warning(self, "Check password", "Password and confirmation do not match.")
            return

        permissions = [key for key, box in self.access_boxes.items() if box.isChecked()]

        try:
            if self.user:
                self.saved_user = UserService.update_user(
                    self.actor,
                    self.user["id"],
                    name=self.name.text(),
                    email=self.email.text(),
                    phone=self.phone.text(),
                    role=self.role.currentData(),
                    permissions=permissions,
                    new_password=password,
                    is_active=self.active.isChecked(),
                )
            else:
                self.saved_user = UserService.create_user(
                    self.actor,
                    name=self.name.text(),
                    email=self.email.text(),
                    phone=self.phone.text(),
                    role=self.role.currentData(),
                    permissions=permissions,
                    password=password,
                    is_active=self.active.isChecked(),
                )
        except UserError as error:
            QMessageBox.warning(self, "Can't save user", str(error))
            return

        self.accept()
