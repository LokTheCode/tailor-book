from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
    QHBoxLayout,
)


class InventoryActionButtons(QWidget):

    viewClicked = Signal(dict)
    editClicked = Signal(dict)
    stockClicked = Signal(dict)
    deleteClicked = Signal(dict)

    def __init__(
        self,
        item,
        parent=None
    ):

        super().__init__(parent)

        self.item = item

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            4, 2, 4, 2
        )

        layout.setSpacing(4)

        # --------------------------------------------------
        # STOCK
        # --------------------------------------------------

        stock_btn = QPushButton(
            "Stock"
        )

        stock_btn.setObjectName(
            "InventoryStockButton"
        )

        stock_btn.clicked.connect(
            lambda checked=False, item=item:
                self.stockClicked.emit(item)
        )

        # --------------------------------------------------
        # EDIT
        # --------------------------------------------------

        edit_btn = QPushButton(
            "Edit"
        )

        edit_btn.setObjectName(
            "InventoryEditButton"
        )

        edit_btn.clicked.connect(
            lambda checked=False, item=item:
                self.editClicked.emit(item)
        )

        # --------------------------------------------------
        # DELETE
        # --------------------------------------------------

        delete_btn = QPushButton(
            "Delete"
        )

        delete_btn.setObjectName(
            "InventoryDeleteButton"
        )

        delete_btn.clicked.connect(
            lambda checked=False, item=item:
                self.deleteClicked.emit(item)
        )

        layout.addWidget(stock_btn)
        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)


class InventoryTable(QWidget):

    viewClicked = Signal(dict)
    editClicked = Signal(dict)
    stockClicked = Signal(dict)
    deleteClicked = Signal(dict)

    def __init__(self, parent=None):

        super().__init__(parent)

        self.items = []

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            0, 0, 0, 0
        )

        self.table = QTableWidget()

        self.table.setColumnCount(9)

        self.table.setHorizontalHeaderLabels([
            "Item",
            "Category",
            "SKU",
            "Quantity",
            "Unit",
            "Cost Price",
            "Selling Price",
            "Stock Status",
            "Actions",
        ])

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.verticalHeader().setVisible(
            False
        )

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            0,
            QHeaderView.Stretch
        )

        for column in range(1, 9):

            header.setSectionResizeMode(
                column,
                QHeaderView.ResizeToContents
            )

        layout.addWidget(
            self.table
        )

    # ==========================================================
    # DATA
    # ==========================================================

    def set_data(self, items):

        self.items = items or []

        self.table.setRowCount(0)

        if not self.items:

            self.table.insertRow(0)

            item = QTableWidgetItem(
                "No inventory items found"
            )

            item.setTextAlignment(
                Qt.AlignCenter
            )

            self.table.setItem(
                0,
                0,
                item
            )

            self.table.setSpan(
                0,
                0,
                1,
                9
            )

            return

        for row, item in enumerate(
            self.items
        ):

            self.table.insertRow(row)

            self.set_item(
                row,
                0,
                item["name"]
            )

            self.set_item(
                row,
                1,
                item["category"]
            )

            self.set_item(
                row,
                2,
                item["sku"]
            )

            self.set_item(
                row,
                3,
                f'{item["quantity"]:g}'
            )

            self.set_item(
                row,
                4,
                item["unit"]
            )

            self.set_item(
                row,
                5,
                f'₹{item["cost_price"]:,.2f}'
            )

            self.set_item(
                row,
                6,
                f'₹{item["selling_price"]:,.2f}'
            )

            status = item[
                "stock_status"
            ]

            status_item = QTableWidgetItem(
                status
            )

            status_item.setTextAlignment(
                Qt.AlignCenter
            )

            self.table.setItem(
                row,
                7,
                status_item
            )

            actions = InventoryActionButtons(
                item
            )

            actions.viewClicked.connect(
                self.viewClicked.emit
            )

            actions.editClicked.connect(
                self.editClicked.emit
            )

            actions.stockClicked.connect(
                self.stockClicked.emit
            )

            actions.deleteClicked.connect(
                self.deleteClicked.emit
            )

            self.table.setCellWidget(
                row,
                8,
                actions
            )

            self.table.setRowHeight(
                row,
                55
            )

    def set_item(
        self,
        row,
        column,
        value
    ):

        item = QTableWidgetItem(
            str(value)
        )

        item.setTextAlignment(
            Qt.AlignVCenter
        )

        self.table.setItem(
            row,
            column,
            item
        )

    def clear(self):

        self.items = []

        self.table.setRowCount(0)