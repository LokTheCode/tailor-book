from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout
)

from PySide6.QtCore import Qt, Signal

import qtawesome as qta


class CustomerHeader(QWidget):

    addCustomerClicked = Signal()
    exportClicked = Signal()
    refreshClicked = Signal()

    def __init__(self):
        super().__init__()

        self.build_ui()

    # --------------------------------------------------------

    def build_ui(self):


        root = QHBoxLayout(self)

        root.setContentsMargins(0, 0, 0, 0)

        root.setSpacing(15)

        # ==========================================
        # Left
        # ==========================================

        left = QVBoxLayout()

        left.setSpacing(4)

        title = QLabel("Customers")

        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Manage your tailoring customers, measurements and order history."
        )

        subtitle.setObjectName("PageSubtitle")

        left.addWidget(title)

        left.addWidget(subtitle)

        root.addLayout(left)

        root.addStretch()

        # ==========================================
        # Refresh
        # ==========================================

        refresh = QPushButton(" Refresh")

        refresh.setIcon(
            qta.icon(
                "fa5s.sync-alt",
                color="white"
            )
        )

        refresh.clicked.connect(
            self.refreshClicked.emit
        )

        root.addWidget(refresh)

        # ==========================================
        # Export
        # ==========================================

        export = QPushButton(" Export")

        export.setIcon(
            qta.icon(
                "fa5s.file-export",
                color="white"
            )
        )

        export.clicked.connect(
            self.exportClicked.emit
        )

        root.addWidget(export)

        # ==========================================
        # Add Customer
        # ==========================================

        add = QPushButton(" Add Customer")

        add.setObjectName("Primary")

        add.setIcon(
            qta.icon(
                "fa5s.user-plus",
                color="white"
            )
        )

        add.clicked.connect(
            self.addCustomerClicked.emit
        )

        root.addWidget(add)