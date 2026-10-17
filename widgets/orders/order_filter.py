from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QDateEdit
)

from PySide6.QtCore import (
    Signal,
    QDate
)

import qtawesome as qta


class OrderFilter(QFrame):

    searchChanged = Signal(str)

    statusChanged = Signal(str)

    paymentChanged = Signal(str)

    tailorChanged = Signal(str)

    dateChanged = Signal()

    refreshClicked = Signal()

    def __init__(self):
        super().__init__()

        self.build_ui()

    # ----------------------------------------------------

    def build_ui(self):
        

        self.setObjectName("Card")


        layout = QHBoxLayout(self)

        layout.setContentsMargins(15,15,15,15)

        layout.setSpacing(12)

        # ------------------------------------------------
        # Search
        # ------------------------------------------------

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Search Customer / Mobile / Order No..."
        )

        self.search.addAction(

            qta.icon(
                "fa5s.search",
                color="#9CA3AF"
            ),

            QLineEdit.LeadingPosition

        )

        self.search.textChanged.connect(
            self.searchChanged.emit
        )

        layout.addWidget(
            self.search,
            2
        )

        # ------------------------------------------------
        # Order Status
        # ------------------------------------------------

        self.status = QComboBox()

        self.status.addItems([

            "All Status",

            "Received",

            "Measurement",

            "Cutting",

            "Stitching",

            "Ironing",

            "Trial",

            "Ready",

            "Delivered",

            "Cancelled"

        ])

        self.status.currentTextChanged.connect(
            self.statusChanged.emit
        )

        layout.addWidget(
            self.status
        )

        # ------------------------------------------------
        # Payment
        # ------------------------------------------------

        self.payment = QComboBox()

        self.payment.addItems([

            "All Payments",

            "Paid",

            "Partial",

            "Pending"

        ])

        self.payment.currentTextChanged.connect(
            self.paymentChanged.emit
        )

        layout.addWidget(
            self.payment
        )

        # ------------------------------------------------
        # Tailor
        # ------------------------------------------------

        self.tailor = QComboBox()

        self.tailor.addItems([

            "All Tailors",

            "Amit",

            "Rahul",

            "Deepak"

        ])

        self.tailor.currentTextChanged.connect(
            self.tailorChanged.emit
        )

        layout.addWidget(
            self.tailor
        )

        # ------------------------------------------------
        # Delivery Date
        # ------------------------------------------------

        self.date = QDateEdit()

        self.date.setCalendarPopup(True)

        self.date.setDate(
            QDate.currentDate()
        )

        self.date.dateChanged.connect(
            self.dateChanged.emit
        )

        layout.addWidget(
            self.date
        )

        # ------------------------------------------------
        # Refresh
        # ------------------------------------------------

        self.refresh = QPushButton(" Refresh")

        self.refresh.setObjectName("Primary")

        self.refresh.setIcon(
            qta.icon(
                "fa5s.sync-alt",
                color="white"
            )
        )

        self.refresh.clicked.connect(
            self.refreshClicked.emit
        )

        layout.addWidget(
            self.refresh
        )

    # ----------------------------------------------------
    # GET FILTERS
    # ----------------------------------------------------

    def get_filters(self):

        return {
            "search": self.search.text().strip(),

            "status": (
                ""
                if self.status.currentText() == "All Status"
                else self.status.currentText()
            ),

            "payment": (
                ""
                if self.payment.currentText() == "All Payments"
                else self.payment.currentText()
            ),

            "tailor": (
                ""
                if self.tailor.currentText() == "All Tailors"
                else self.tailor.currentText()
            ),

            "date": self.date.date().toString(
                "yyyy-MM-dd"
            ),
        }