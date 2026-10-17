from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
)


class InventoryHeader(QFrame):

    addItemClicked = Signal()
    refreshClicked = Signal()

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setObjectName(
            "PageHeader"
        )

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            20, 16, 20, 16
        )

        # ======================================================
        # TITLE
        # ======================================================

        title_layout = QVBoxLayout()

        title = QLabel(
            "Inventory"
        )

        title.setObjectName(
            "PageTitle"
        )

        subtitle = QLabel(
            "Manage fabrics, buttons, zippers and other materials"
        )

        subtitle.setObjectName(
            "PageSubtitle"
        )

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        layout.addLayout(title_layout)

        layout.addStretch()

        # ======================================================
        # REFRESH
        # ======================================================

        refresh_btn = QPushButton(
            "↻ Refresh"
        )

        refresh_btn.clicked.connect(
            self.refreshClicked.emit
        )

        # ======================================================
        # ADD
        # ======================================================

        add_btn = QPushButton(
            "+ Add Inventory"
        )

        add_btn.setObjectName(
            "Primary"
        )

        add_btn.clicked.connect(
            self.addItemClicked.emit
        )

        layout.addWidget(refresh_btn)
        layout.addWidget(add_btn)