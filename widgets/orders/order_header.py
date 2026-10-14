from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton
)

from PySide6.QtCore import Signal

import qtawesome as qta


class OrderHeader(QFrame):

    addOrderClicked = Signal()

    def __init__(self):
        super().__init__()

        self.build_ui()

    # ----------------------------------------------------

    def build_ui(self):

        self.setObjectName("OrderHeader")

        self.setStyleSheet("""

        QFrame#OrderHeader{

            background:#1F2937;

            border:1px solid #374151;

            border-radius:18px;

        }

        QLabel#Title{

            color:white;

            font-size:28px;

            font-weight:700;

        }

        QLabel#Subtitle{

            color:#9CA3AF;

            font-size:13px;

        }

        QPushButton{

            color:white;

            border:none;

            border-radius:10px;

            padding:12px 20px;

            min-height:46px;

            font-size:14px;

            font-weight:600;

            background:qlineargradient(
                x1:0,y1:0,
                x2:1,y2:0,
                stop:0 #3B82F6,
                stop:1 #8B5CF6
            );

        }

        QPushButton:hover{

            background:#2563EB;

        }

        """)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(25,20,25,20)

        # Left Side

        left = QVBoxLayout()

        title = QLabel("Orders")

        title.setObjectName("Title")

        subtitle = QLabel(
            "Manage tailoring orders, production and delivery."
        )

        subtitle.setObjectName("Subtitle")

        left.addWidget(title)

        left.addWidget(subtitle)

        layout.addLayout(left)

        layout.addStretch()

        # Right Side

        self.add_btn = QPushButton(" New Order")

        self.add_btn.setIcon(
            qta.icon(
                "fa5s.plus",
                color="white"
            )
        )

        self.add_btn.clicked.connect(
            self.addOrderClicked.emit
        )

        layout.addWidget(self.add_btn)