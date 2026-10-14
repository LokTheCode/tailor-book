from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QComboBox,
    QDoubleSpinBox,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
)

from data.inventory_crud import (
    stock_in,
    stock_out,
    adjust_stock,
)


class StockTransactionDialog(QDialog):

    saved = Signal()

    def __init__(
        self,
        item,
        parent=None
    ):

        super().__init__(parent)

        self.item = item

        self.setWindowTitle(
            "Stock Transaction"
        )

        self.resize(
            450,
            420
        )

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel(
            self.item["name"]
        )

        title.setObjectName(
            "StockDialogTitle"
        )

        layout.addWidget(
            title
        )

        current = QLabel(
            f'Current Stock: '
            f'{self.item["quantity"]:g} '
            f'{self.item["unit"]}'
        )

        layout.addWidget(
            current
        )

        form = QFormLayout()

        # ======================================================
        # TRANSACTION TYPE
        # ======================================================

        self.transaction_type = QComboBox()

        self.transaction_type.addItems([
            "Stock In",
            "Stock Out",
            "Adjustment",
        ])

        self.transaction_type.currentTextChanged.connect(
            self.on_type_changed
        )

        form.addRow(
            "Transaction",
            self.transaction_type
        )

        # ======================================================
        # QUANTITY
        # ======================================================

        self.quantity = QDoubleSpinBox()

        self.quantity.setRange(
            0,
            9999999
        )

        self.quantity.setDecimals(
            2
        )

        form.addRow(
            "Quantity",
            self.quantity
        )

        # ======================================================
        # REFERENCE
        # ======================================================

        self.reference = QComboBox()

        self.reference.addItems([
            "MANUAL",
            "PURCHASE",
            "ORDER",
        ])

        form.addRow(
            "Reference",
            self.reference
        )

        # ======================================================
        # NOTES
        # ======================================================

        self.notes = QTextEdit()

        self.notes.setMaximumHeight(
            100
        )

        form.addRow(
            "Notes",
            self.notes
        )

        layout.addLayout(
            form
        )

        layout.addStretch()

        buttons = QHBoxLayout()

        cancel = QPushButton(
            "Cancel"
        )

        cancel.clicked.connect(
            self.reject
        )

        save = QPushButton(
            "Save Transaction"
        )

        save.setObjectName(
            "StockSaveButton"
        )

        save.clicked.connect(
            self.save
        )

        buttons.addStretch()

        buttons.addWidget(
            cancel
        )

        buttons.addWidget(
            save
        )

        layout.addLayout(
            buttons
        )

    def on_type_changed(self, value):

        if value == "Adjustment":

            self.quantity.setValue(
                self.item["quantity"]
            )

        else:

            self.quantity.setValue(
                0
            )

    def save(self):

        transaction = (
            self.transaction_type.currentText()
        )

        quantity = self.quantity.value()

        notes = (
            self.notes.toPlainText()
            .strip()
            or None
        )

        try:

            if transaction == "Stock In":

                stock_in(
                    item_id=self.item["id"],
                    quantity=quantity,
                    reference_type=self.reference.currentText(),
                    notes=notes,
                )

            elif transaction == "Stock Out":

                stock_out(
                    item_id=self.item["id"],
                    quantity=quantity,
                    reference_type=self.reference.currentText(),
                    notes=notes,
                )

            else:

                adjust_stock(
                    item_id=self.item["id"],
                    new_quantity=quantity,
                    notes=notes,
                )

            QMessageBox.information(
                self,
                "Success",
                "Stock updated successfully."
            )

            self.saved.emit()

            self.accept()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Stock Error",
                str(e)
            )