from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QDoubleSpinBox,
    QTextEdit,
    QPushButton,
    QMessageBox,
)

from data.inventory_crud import (
    create_inventory_item,
    update_inventory_item,
)


class InventoryForm(QWidget):

    backClicked = Signal()
    saved = Signal()

    def __init__(self, parent=None):

        super().__init__(parent)

        self.editing_id = None

        self.build_ui()

    # ==========================================================
    # UI
    # ==========================================================

    def build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            20, 20, 20, 20
        )

        # ======================================================
        # HEADER
        # ======================================================

        header = QHBoxLayout()

        back_btn = QPushButton(
            "← Back"
        )

        back_btn.clicked.connect(
            self.backClicked.emit
        )

        header.addWidget(
            back_btn
        )

        self.title = QLabel(
            "Add Inventory Item"
        )

        self.title.setObjectName(
            "InventoryFormTitle"
        )

        header.addWidget(
            self.title
        )

        header.addStretch()

        layout.addLayout(
            header
        )

        # ======================================================
        # FORM
        # ======================================================

        form = QFormLayout()

        form.setSpacing(12)

        # --------------------------------------------------
        # NAME
        # --------------------------------------------------

        self.name = QLineEdit()

        self.name.setPlaceholderText(
            "e.g. Blue Cotton Fabric"
        )

        form.addRow(
            "Item Name *",
            self.name
        )

        # --------------------------------------------------
        # CATEGORY
        # --------------------------------------------------

        self.category = QComboBox()

        self.category.setEditable(True)

        self.category.addItems([
            "Fabric",
            "Buttons",
            "Lining",
            "Zipper",
            "Thread",
            "Material",
            "Other",
        ])

        form.addRow(
            "Category *",
            self.category
        )

        # --------------------------------------------------
        # SKU
        # --------------------------------------------------

        self.sku = QLineEdit()

        self.sku.setPlaceholderText(
            "Optional SKU"
        )

        form.addRow(
            "SKU",
            self.sku
        )

        # --------------------------------------------------
        # UNIT
        # --------------------------------------------------

        self.unit = QComboBox()

        self.unit.addItems([
            "meter",
            "piece",
            "packet",
            "roll",
            "kg",
            "gram",
            "liter",
            "box",
        ])

        form.addRow(
            "Unit",
            self.unit
        )

        # --------------------------------------------------
        # OPENING QUANTITY
        # --------------------------------------------------

        self.quantity = QDoubleSpinBox()

        self.quantity.setRange(
            0,
            9999999
        )

        self.quantity.setDecimals(
            2
        )

        form.addRow(
            "Opening Quantity",
            self.quantity
        )

        # --------------------------------------------------
        # MINIMUM
        # --------------------------------------------------

        self.minimum_quantity = QDoubleSpinBox()

        self.minimum_quantity.setRange(
            0,
            9999999
        )

        self.minimum_quantity.setDecimals(
            2
        )

        self.minimum_quantity.setValue(
            5
        )

        form.addRow(
            "Minimum Quantity",
            self.minimum_quantity
        )

        # --------------------------------------------------
        # COST
        # --------------------------------------------------

        self.cost_price = QDoubleSpinBox()

        self.cost_price.setRange(
            0,
            999999999
        )

        self.cost_price.setDecimals(
            2
        )

        self.cost_price.setPrefix(
            "₹ "
        )

        form.addRow(
            "Cost Price",
            self.cost_price
        )

        # --------------------------------------------------
        # SELLING
        # --------------------------------------------------

        self.selling_price = QDoubleSpinBox()

        self.selling_price.setRange(
            0,
            999999999
        )

        self.selling_price.setDecimals(
            2
        )

        self.selling_price.setPrefix(
            "₹ "
        )

        form.addRow(
            "Selling Price",
            self.selling_price
        )

        # --------------------------------------------------
        # DESCRIPTION
        # --------------------------------------------------

        self.description = QTextEdit()

        self.description.setMaximumHeight(
            100
        )

        form.addRow(
            "Description",
            self.description
        )

        layout.addLayout(
            form
        )

        layout.addStretch()

        # ======================================================
        # BUTTONS
        # ======================================================

        buttons = QHBoxLayout()

        buttons.addStretch()

        cancel = QPushButton(
            "Cancel"
        )

        cancel.clicked.connect(
            self.backClicked.emit
        )

        save = QPushButton(
            "Save Item"
        )

        save.setObjectName(
            "InventorySaveButton"
        )

        save.clicked.connect(
            self.save
        )

        buttons.addWidget(
            cancel
        )

        buttons.addWidget(
            save
        )

        layout.addLayout(
            buttons
        )

    # ==========================================================
    # NEW
    # ==========================================================

    def prepare_new(self):

        self.editing_id = None

        self.title.setText(
            "Add Inventory Item"
        )

        self.name.clear()
        self.sku.clear()

        self.category.setCurrentIndex(
            0
        )

        self.unit.setCurrentIndex(
            0
        )

        self.quantity.setValue(
            0
        )

        self.minimum_quantity.setValue(
            5
        )

        self.cost_price.setValue(
            0
        )

        self.selling_price.setValue(
            0
        )

        self.description.clear()

        self.quantity.setEnabled(
            True
        )

    # ==========================================================
    # EDIT
    # ==========================================================

    def load_item(self, item):

        self.editing_id = item["id"]

        self.title.setText(
            "Edit Inventory Item"
        )

        self.name.setText(
            item["name"]
        )

        category_index = (
            self.category.findText(
                item["category"]
            )
        )

        if category_index >= 0:

            self.category.setCurrentIndex(
                category_index
            )

        else:

            self.category.setCurrentText(
                item["category"]
            )

        self.sku.setText(
            "" if item["sku"] == "—"
            else item["sku"]
        )

        unit_index = (
            self.unit.findText(
                item["unit"]
            )
        )

        if unit_index >= 0:

            self.unit.setCurrentIndex(
                unit_index
            )

        self.quantity.setValue(
            item["quantity"]
        )

        self.minimum_quantity.setValue(
            item["minimum_quantity"]
        )

        self.cost_price.setValue(
            item["cost_price"]
        )

        self.selling_price.setValue(
            item["selling_price"]
        )

        self.description.setPlainText(
            item["description"]
        )

        # Quantity is not edited here.
        # Stock changes must create transactions.

        self.quantity.setEnabled(
            False
        )

    # ==========================================================
    # SAVE
    # ==========================================================

    def save(self):

        name = self.name.text().strip()

        category = (
            self.category.currentText()
            .strip()
        )

        if not name:

            QMessageBox.warning(
                self,
                "Validation",
                "Please enter item name."
            )

            return

        if not category:

            QMessageBox.warning(
                self,
                "Validation",
                "Please enter category."
            )

            return

        data = {

            "name":
                name,

            "category":
                category,

            "sku":
                self.sku.text().strip()
                or None,

            "unit":
                self.unit.currentText(),

            "quantity":
                self.quantity.value(),

            "minimum_quantity":
                self.minimum_quantity.value(),

            "cost_price":
                self.cost_price.value(),

            "selling_price":
                self.selling_price.value(),

            "description":
                self.description.toPlainText()
                .strip()
                or None,
        }

        try:

            if self.editing_id:

                update_inventory_item(
                    self.editing_id,
                    data
                )

            else:

                create_inventory_item(
                    data
                )

            QMessageBox.information(
                self,
                "Success",
                "Inventory item saved successfully."
            )

            self.saved.emit()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )