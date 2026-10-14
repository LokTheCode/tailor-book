from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QDateEdit,
)

from PySide6.QtCore import (
    Signal,
    QDate,
)

import qtawesome as qta


class MeasurementFilter(QFrame):

    searchChanged = Signal(str)

    garmentChanged = Signal(str)

    dateChanged = Signal(object)

    refreshClicked = Signal()

    clearClicked = Signal()

    def __init__(self):

        super().__init__()

        self.build_ui()

    # ======================================================
    # UI
    # ======================================================

    def build_ui(self):

        self.setObjectName(
            "MeasurementFilter"
        )

        self.setStyleSheet("""
        
        QLineEdit,
        QComboBox,
        QDateEdit {

            background:#1F2937;

            color:white;

            border:1px solid #374151;

            border-radius:12px;

            padding:10px 12px;

            font-size:13px;

        }

        QLineEdit:focus,
        QComboBox:focus,
        QDateEdit:focus {

            border:2px solid #3B82F6;

        }

        QPushButton {

            background:#1F2937;

            color:white;

            border:1px solid #374151;

            border-radius:12px;

            padding:10px 12px;

            font-weight:600;

        }

        QPushButton:hover {

            background:#293548;

            border-color:#3B82F6;

        }

        QPushButton#Primary {

            border:none;

            background:qlineargradient(
                x1:0,y1:0,
                x2:1,y2:0,
                stop:0 #3B82F6,
                stop:1 #8B5CF6
            );

        }

        """)

        root = QHBoxLayout(self)

        root.setContentsMargins(
            20,
            15,
            20,
            15,
        )

        root.setSpacing(12)

        # ==================================================
        # SEARCH
        # ==================================================

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Search Customer / Mobile / Measurement..."
        )

        self.search.addAction(
            qta.icon(
                "fa5s.search",
                color="#9CA3AF",
            ),
            QLineEdit.LeadingPosition,
        )

        self.search.textChanged.connect(
            self.searchChanged.emit
        )

        root.addWidget(
            self.search,
            3,
        )

        # ==================================================
        # GARMENT
        # ==================================================

        self.garment = QComboBox()

        self.garment.addItems([

            "All Garments",

            "Shirt",

            "Pant",

            "Suit",

            "Kurta",

            "Blazer",

            "Sherwani",

        ])

        self.garment.currentTextChanged.connect(
            self.garmentChanged.emit
        )

        root.addWidget(
            self.garment,
            1,
        )

        # ==================================================
        # DATE
        # ==================================================

        self.date = QDateEdit()

        self.date.setCalendarPopup(
            True
        )

        self.date.setDate(
            QDate.currentDate()
        )

        root.addWidget(
            self.date
        )

        # ==================================================
        # ALL DATES
        # ==================================================

        self.clear_date = QPushButton(
            "All Dates"
        )

        self.clear_date.clicked.connect(
            self.clear_date_filter
        )

        root.addWidget(
            self.clear_date
        )

        # ==================================================
        # REFRESH
        # ==================================================

        self.refresh = QPushButton(
            " Refresh"
        )

        self.refresh.setObjectName(
            "Primary"
        )

        self.refresh.setIcon(
            qta.icon(
                "fa5s.sync-alt",
                color="white",
            )
        )

        self.refresh.clicked.connect(
            self.refreshClicked.emit
        )

        root.addWidget(
            self.refresh
        )

        self.date.dateChanged.connect(
            self.date_changed
        )

    # ======================================================
    # DATE
    # ======================================================

    def date_changed(self, date):

        self.dateChanged.emit(
            date
        )

    # ======================================================
    # CLEAR DATE
    # ======================================================

    def clear_date_filter(self):

        self.dateChanged.emit(
            None
        )

    # ======================================================
    # GET FILTERS
    # ======================================================

    def get_filters(self):

        return {

            "search":
                self.search.text().strip(),

            "garment":
                self.garment.currentText(),

            "date":
                self.date.date(),

        }