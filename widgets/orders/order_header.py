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

        self.setObjectName("PageHeader")


        layout = QHBoxLayout(self)

        layout.setContentsMargins(25,20,25,20)

        # Left Side

        left = QVBoxLayout()

        title = QLabel("Orders")

        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Manage tailoring orders, production and delivery."
        )

        subtitle.setObjectName("PageSubtitle")

        left.addWidget(title)

        left.addWidget(subtitle)

        layout.addLayout(left)

        layout.addStretch()

        # Right Side

        self.add_btn = QPushButton(" New Order")

        self.add_btn.setObjectName("Primary")

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