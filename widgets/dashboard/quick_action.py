from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QGridLayout
)

from PySide6.QtCore import Qt
import qtawesome as qta


class QuickAction(QFrame):

    def __init__(self):
        super().__init__()

        self.build_ui()

    # ----------------------------------------------------

    def build_ui(self):

        self.setObjectName("QuickActions")

        root = QVBoxLayout(self)

        root.setContentsMargins(20,20,20,20)

        root.setSpacing(20)

        title = QLabel("Quick Actions")

        title.setObjectName("CardTitle")

        root.addWidget(title)

        grid = QGridLayout()

        grid.setSpacing(15)

        actions = [

            ("New Customer", "fa5s.user-plus"),

            ("Measurement", "fa5s.ruler"),

            ("New Order", "fa5s.clipboard-list"),

            ("Billing", "fa5s.file-invoice-dollar"),

            ("Delivery", "fa5s.truck"),

            ("Reports", "fa5s.chart-line"),

            ("Settings", "fa5s.cog"),

            ("Backup", "fa5s.database")

        ]

        row = 0
        col = 0

        for text, icon in actions:

            btn = QPushButton(text)

            btn.setMinimumHeight(90)

            btn.setCursor(Qt.PointingHandCursor)

            btn.setIcon(
                qta.icon(
                    icon,
                    color="white"
                )
            )

            btn.setIconSize(
                qta.icon(icon).pixmap(28,28).size()
            )

            grid.addWidget(btn,row,col)

            col += 1

            if col == 4:

                col = 0

                row += 1

        root.addLayout(grid)