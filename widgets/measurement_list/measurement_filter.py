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

from services import settings_service


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
            "Card"
        )


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

        self.garment.addItems(
            ["All Garments"] + settings_service.get_list("garment_types")
        )

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

        # The minimum date is shown as "All dates" (no date filter)
        self.date.setMinimumDate(QDate(2000, 1, 1))
        self.date.setSpecialValueText("All dates")
        self.date.setDisplayFormat("dd MMM yyyy")
        self.date.setDate(self.date.minimumDate())

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

    def clear_date_filter(self):

        # Setting the minimum date shows "All dates" and emits dateChanged
        self.date.setDate(
            self.date.minimumDate()
        )

    def get_filters(self):

        date = self.date.date()

        return {
            "search":
                self.search.text().strip(),
            "garment":
                self.garment.currentText(),
            "date":
                None if date == self.date.minimumDate() else date,
        }
