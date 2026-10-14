from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QComboBox,
    QSizePolicy
)

from PySide6.QtCore import Qt, Signal

import qtawesome as qta


class CustomerFilter(QWidget):

    filterClicked = Signal()
    resetClicked = Signal()

    def __init__(self):
        super().__init__()

        self.build_ui()

    # -----------------------------------------------------

    def build_ui(self):

        self.setStyleSheet("""

        QWidget{
            background:transparent;
        }

        QLineEdit,
        QComboBox{

            background:#1F2937;

            color:white;

            border:1px solid #374151;

            border-radius:12px;

            padding:10px 10px;

            font-size:13px;
        }

        QLineEdit:focus,
        QComboBox:focus{

            border:2px solid #3B82F6;

        }

        QComboBox::drop-down{

            border:none;
            width:28px;

        }

        QComboBox::down-arrow{

            image:none;

        }

        QPushButton{

            background:#1F2937;

            color:white;

            border:1px solid #374151;

            border-radius:12px;

            padding:10px 10px;

            font-weight:600;
        }

        QPushButton:hover{

            background:#293548;

            border:1px solid #3B82F6;

        }

        QPushButton#Primary{

            border:none;

            background:qlineargradient(
                x1:0,y1:0,
                x2:1,y2:0,
                stop:0 #3B82F6,
                stop:1 #8B5CF6
            );

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

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0,0,0,0)

        layout.setSpacing(15)

        # --------------------------------------------
        # Search Name
        # --------------------------------------------

        self.searchName = QLineEdit()

        self.searchName.setPlaceholderText(
            "Search Name..."
        )

        self.searchName.addAction(
            qta.icon(
                "fa5s.search",
                color="#9CA3AF"
            ),
            QLineEdit.LeadingPosition
        )

        self.searchName.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        layout.addWidget(
            self.searchName,
            2
        )

        # --------------------------------------------
        # Mobile
        # --------------------------------------------

        self.mobile = QLineEdit()

        self.mobile.setPlaceholderText(
            "Mobile Number..."
        )

        self.mobile.addAction(
            qta.icon(
                "fa5s.mobile-alt",
                color="#9CA3AF"
            ),
            QLineEdit.LeadingPosition
        )

        layout.addWidget(
            self.mobile,
            2
        )

        # --------------------------------------------
        # Status
        # --------------------------------------------

        self.status = QComboBox()

        self.status.addItems([
            "All Status",
            "Active",
            "Inactive"
        ])

        layout.addWidget(self.status)

        # --------------------------------------------
        # Customer Type
        # --------------------------------------------

        self.customerType = QComboBox()

        self.customerType.addItems([
            "All Customers",
            "Regular",
            "VIP",
            "Wholesale"
        ])

        layout.addWidget(self.customerType)

        # --------------------------------------------
        # City
        # --------------------------------------------

        self.city = QComboBox()

        self.city.addItems([
            "All Cities",
            "Delhi",
            "Mumbai",
            "Jaipur",
            "Lucknow"
        ])

        layout.addWidget(self.city)

        # --------------------------------------------
        # Reset
        # --------------------------------------------

        reset = QPushButton(" Reset")

        reset.setIcon(
            qta.icon(
                "fa5s.undo-alt",
                color="white"
            )
        )

        reset.clicked.connect(
            self.resetClicked.emit
        )

        layout.addWidget(reset)

        # --------------------------------------------
        # Search Button
        # --------------------------------------------

        search = QPushButton(" Search")

        search.setObjectName("Primary")

        search.setIcon(
            qta.icon(
                "fa5s.search",
                color="white"
            )
        )

        search.clicked.connect(
            self.filterClicked.emit
        )

        layout.addWidget(search)