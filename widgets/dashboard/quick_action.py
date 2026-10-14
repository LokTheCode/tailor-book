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

        self.setStyleSheet("""

        QFrame{

            background:#1B2333;

            border-radius:18px;

        }

        QLabel#Title{

            color:white;

            font-size:20px;

            font-weight:bold;

        }

        QPushButton{

            background:#111827;

            border:1px solid #374151;

            border-radius:14px;

            color:white;

            font-size:14px;

            font-weight:600;

            padding:18px;

            text-align:left;

        }

        QPushButton:hover{

            border:2px solid #3B82F6;

            background:qlineargradient(
                x1:0,
                y1:0,
                x2:1,
                y2:1,
                stop:0 #3B82F6,
                stop:1 #8B5CF6
            );

        }

        """)

        root = QVBoxLayout(self)

        root.setContentsMargins(20,20,20,20)

        root.setSpacing(20)

        title = QLabel("Quick Actions")

        title.setObjectName("Title")

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