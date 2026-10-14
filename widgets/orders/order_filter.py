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
        

        self.setObjectName("OrderFilter")

        self.setStyleSheet("""

        QFrame#OrderFilter{

            background:#1F2937;

            border:1px solid #374151;

            border-radius:15px;

        }

        QLineEdit,
        QComboBox,
        QDateEdit{

            background:#111827;

            color:white;

            border:1px solid #374151;

            border-radius:8px;

            padding:8px;

            min-height:38px;

        }

        QLineEdit:focus,
        QComboBox:focus,
        QDateEdit:focus{

            border:2px solid #3B82F6;

        }

        QPushButton{

            background:qlineargradient(
                x1:0,y1:0,
                x2:1,y2:0,
                stop:0 #3B82F6,
                stop:1 #8B5CF6
            );

            color:white;

            border:none;

            border-radius:8px;

            padding:10px 18px;

            min-height:40px;

            font-weight:bold;

        }

        QPushButton:hover{

            background:#2563EB;

        }

        """)

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