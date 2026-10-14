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

        self.setStyleSheet("""

        QWidget{
            background:transparent;
        }

        QLabel#Title{
            color:white;
            font-size:30px;
            font-weight:700;
        }

        QLabel#Subtitle{
            color:#9CA3AF;
            font-size:14px;
        }

        QPushButton{

            background:#1F2937;

            color:white;

            border:1px solid #374151;

            border-radius:12px;

            padding:10px 18px;

            font-size:14px;

            font-weight:600;
        }

        QPushButton:hover{

            border:1px solid #3B82F6;

            background:#273549;

        }

        QPushButton#Primary{

            background:qlineargradient(
                x1:0,y1:0,
                x2:1,y2:0,
                stop:0 #3B82F6,
                stop:1 #8B5CF6
            );

            border:none;

        }

        QPushButton#Primary:hover{

            background:qlineargradient(
                x1:0,y1:0,
                x2:1,y2:0,
                stop:0 #2563EB,
                stop:1 #7C3AED
            );

        }

        """)

        root = QHBoxLayout(self)

        root.setContentsMargins(0, 0, 0, 0)

        root.setSpacing(15)

        # ==========================================
        # Left
        # ==========================================

        left = QVBoxLayout()

        left.setSpacing(4)

        title = QLabel("Customers")

        title.setObjectName("Title")

        subtitle = QLabel(
            "Manage your tailoring customers, measurements and order history."
        )

        subtitle.setObjectName("Subtitle")

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