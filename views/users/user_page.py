from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

import qtawesome as qta
from utils.theme import theme_color

from services.user_service import PAGES, UserError, UserService, manageable_roles
from views.users.user_dialog import UserDialog
from utils.table import setup_table


class UserPage(QWidget):
    """Lists admins and sub-admins (never the super admin) and manages them."""

    COLUMNS = ["Name", "Email", "Phone", "Role", "Access", "Status", "Actions"]

    def __init__(self, actor, parent=None):
        super().__init__(parent)

        self.actor = actor
        self.users = []

        self.build_ui()
        self.refresh()

    # ======================================================
    # UI
    # ======================================================

    def build_ui(self):

        root = QVBoxLayout(self)
        root.setContentsMargins(30, 25, 30, 25)
        root.setSpacing(20)

        # --------------------------------------------------
        # Header
        # --------------------------------------------------

        header = QFrame()
        header.setObjectName("PageHeader")

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        titles = QVBoxLayout()
        titles.setSpacing(4)

        title = QLabel("Users")
        title.setObjectName("PageTitle")

        subtitle = QLabel("Add admins and sub admins, and choose which pages they can open.")
        subtitle.setObjectName("PageSubtitle")

        titles.addWidget(title)
        titles.addWidget(subtitle)

        header_layout.addLayout(titles)
        header_layout.addStretch()

        refresh = QPushButton(" Refresh")
        refresh.setIcon(qta.icon("fa5s.sync-alt", color=theme_color("text")))
        refresh.clicked.connect(self.refresh)
        header_layout.addWidget(refresh)

        self.add_button = QPushButton(" Add User")
        self.add_button.setObjectName("Primary")
        self.add_button.setIcon(qta.icon("fa5s.user-plus", color="white"))
        self.add_button.clicked.connect(self.add_user)
        header_layout.addWidget(self.add_button)

        root.addWidget(header)

        # --------------------------------------------------
        # Table
        # --------------------------------------------------

        card = QFrame()
        card.setObjectName("Card")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(12, 12, 12, 12)
        card_layout.setSpacing(10)

        self.count_label = QLabel()
        self.count_label.setObjectName("MutedText")
        card_layout.addWidget(self.count_label)

        self.table = QTableWidget(0, len(self.COLUMNS))
        self.table.setHorizontalHeaderLabels(self.COLUMNS)
        # Shared look: 10 rows of space, full-height rows (utils/table.py)
        setup_table(self.table)
        self.table.doubleClicked.connect(lambda index: self.edit_user(self.users[index.row()]))

        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(4, QHeaderView.Stretch)
        for column in (2, 3, 5):
            header_view.setSectionResizeMode(column, QHeaderView.ResizeToContents)
        header_view.setSectionResizeMode(6, QHeaderView.Fixed)
        self.table.setColumnWidth(6, 140)

        card_layout.addWidget(self.table)

        root.addWidget(card, 1)

        self.add_button.setEnabled(bool(manageable_roles(self.actor)))

    # ======================================================
    # DATA
    # ======================================================

    def refresh(self):

        self.users = UserService.list_users(self.actor)

        self.table.setRowCount(len(self.users))

        for row, user in enumerate(self.users):

            if len(user["permissions"]) == len(PAGES):
                access = "All pages"
            else:
                access = ", ".join(PAGES[p] for p in user["permissions"]) or "No pages"

            values = [
                user["name"],
                user["email"],
                user["phone"] or "-",
                user["role_label"],
                access,
                "Active" if user["is_active"] else "Inactive",
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setToolTip(value)
                if column == 5:
                    item.setForeground(QColor(theme_color("success_text" if user["is_active"] else "muted")))
                self.table.setItem(row, column, item)

            self.table.setCellWidget(row, 6, self._actions(user))

        count = len(self.users)
        self.count_label.setText(
            f"{count} user{'s' if count != 1 else ''}"
            if count else "No users yet. Click Add User to create one."
        )

    def _actions(self, user):

        actions = QWidget()
        actions.setObjectName("TableActions")
        actions.setAttribute(Qt.WA_StyledBackground, True)

        layout = QHBoxLayout(actions)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignCenter)

        edit = QPushButton()
        edit.setIcon(qta.icon("fa5s.edit", color="#60A5FA"))
        edit.setToolTip("Edit user and access")
        edit.setCursor(Qt.PointingHandCursor)
        edit.clicked.connect(lambda _=False, u=user: self.edit_user(u))

        toggle = QPushButton()
        if user["is_active"]:
            toggle.setIcon(qta.icon("fa5s.user-slash", color="#F59E0B"))
            toggle.setToolTip("Deactivate (block login)")
        else:
            toggle.setIcon(qta.icon("fa5s.user-check", color="#10B981"))
            toggle.setToolTip("Activate (allow login)")
        toggle.setCursor(Qt.PointingHandCursor)
        toggle.clicked.connect(lambda _=False, u=user: self.toggle_active(u))

        delete = QPushButton()
        delete.setObjectName("IconDanger")
        delete.setIcon(qta.icon("fa5s.trash-alt", color="#EF4444"))
        delete.setToolTip("Delete user")
        delete.setCursor(Qt.PointingHandCursor)
        delete.clicked.connect(lambda _=False, u=user: self.delete_user(u))

        layout.addWidget(edit)
        layout.addWidget(toggle)
        layout.addWidget(delete)

        return actions

    # ======================================================
    # ACTIONS
    # ======================================================

    def add_user(self):
        dialog = UserDialog(self.actor, parent=self)
        if dialog.exec():
            self.refresh()

    def edit_user(self, user):
        dialog = UserDialog(self.actor, user=user, parent=self)
        if dialog.exec():
            self.refresh()

    def toggle_active(self, user):
        try:
            UserService.set_active(self.actor, user["id"], not user["is_active"])
        except UserError as error:
            QMessageBox.warning(self, "Can't change status", str(error))
            return
        self.refresh()

    def delete_user(self, user):

        reply = QMessageBox.question(
            self,
            "Delete user",
            f"Delete {user['name']} ({user['email']})?\n\nThey will no longer be able to log in. "
            "This can't be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        try:
            UserService.delete_user(self.actor, user["id"])
        except UserError as error:
            QMessageBox.warning(self, "Can't delete user", str(error))
            return

        self.refresh()
