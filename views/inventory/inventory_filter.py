from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QLabel,
)


class InventoryFilter(QFrame):

    filterChanged = Signal(dict)

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setObjectName(
            "InventoryFilter"
        )

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            16, 12, 16, 12
        )

        layout.setSpacing(10)

        # ======================================================
        # SEARCH
        # ======================================================

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Search item, SKU or category..."
        )

        self.search.setObjectName(
            "InventorySearch"
        )

        self.search.textChanged.connect(
            self.emit_filter
        )

        layout.addWidget(
            self.search,
            2
        )

        # ======================================================
        # CATEGORY
        # ======================================================

        category_label = QLabel(
            "Category"
        )

        layout.addWidget(
            category_label
        )

        self.category = QComboBox()

        self.category.addItem(
            "All Categories"
        )

        self.category.currentTextChanged.connect(
            self.emit_filter
        )

        layout.addWidget(
            self.category
        )

        # ======================================================
        # STOCK
        # ======================================================

        stock_label = QLabel(
            "Stock"
        )

        layout.addWidget(
            stock_label
        )

        self.stock = QComboBox()

        self.stock.addItems([
            "All Stock",
            "In Stock",
            "Low Stock",
            "Out of Stock",
        ])

        self.stock.currentTextChanged.connect(
            self.emit_filter
        )

        layout.addWidget(
            self.stock
        )

    # ==========================================================
    # CATEGORY DATA
    # ==========================================================

    def set_categories(
        self,
        categories
    ):

        current = self.category.currentText()

        self.category.blockSignals(True)

        self.category.clear()

        self.category.addItem(
            "All Categories"
        )

        for category in categories:

            self.category.addItem(
                category
            )

        index = self.category.findText(
            current
        )

        if index >= 0:

            self.category.setCurrentIndex(
                index
            )

        self.category.blockSignals(False)

    # ==========================================================
    # EMIT
    # ==========================================================

    def emit_filter(self):

        self.filterChanged.emit({

            "search":
                self.search.text().strip(),

            "category":
                self.category.currentText(),

            "stock_status":
                self.stock.currentText(),

        })

    def get_filters(self):

        return {

            "search":
                self.search.text().strip(),

            "category":
                self.category.currentText(),

            "stock_status":
                self.stock.currentText(),

        }