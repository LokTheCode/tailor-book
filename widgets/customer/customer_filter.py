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

from data.customer_crud import CUSTOMER_TYPES


class CustomerFilter(QWidget):

    filterClicked = Signal()
    resetClicked = Signal()

    def __init__(self):
        super().__init__()

        self.build_ui()

    # -----------------------------------------------------

    def build_ui(self):

        self.setObjectName("Card")
        self.setAttribute(Qt.WA_StyledBackground, True)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(16,16,16,16)

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

        # Press Enter in either box to search
        self.searchName.returnPressed.connect(self.filterClicked.emit)
        self.mobile.returnPressed.connect(self.filterClicked.emit)

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

        self.customerType.addItems(["All Customers"] + CUSTOMER_TYPES)

        layout.addWidget(self.customerType)

        # --------------------------------------------
        # City
        # --------------------------------------------


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