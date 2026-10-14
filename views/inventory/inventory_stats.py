from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)


class InventoryStatCard(QFrame):

    def __init__(
        self,
        title,
        value,
        description,
        object_name,
        parent=None
    ):

        super().__init__(parent)

        self.setObjectName(
            object_name
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            18, 16, 18, 16
        )

        title_label = QLabel(title)

        title_label.setObjectName(
            "InventoryStatTitle"
        )

        self.value_label = QLabel(
            str(value)
        )

        self.value_label.setObjectName(
            "InventoryStatValue"
        )

        description_label = QLabel(
            description
        )

        description_label.setObjectName(
            "InventoryStatDescription"
        )

        layout.addWidget(title_label)
        layout.addWidget(
            self.value_label
        )
        layout.addWidget(
            description_label
        )

    def set_value(self, value):

        self.value_label.setText(
            str(value)
        )


class InventoryStats(QFrame):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setObjectName(
            "InventoryStats"
        )

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            0, 0, 0, 0
        )

        layout.setSpacing(12)

        self.total_card = InventoryStatCard(
            "Total Items",
            "0",
            "Active inventory items",
            "InventoryTotalCard"
        )

        self.low_card = InventoryStatCard(
            "Low Stock",
            "0",
            "Items below threshold",
            "InventoryLowCard"
        )

        self.out_card = InventoryStatCard(
            "Out of Stock",
            "0",
            "Items requiring restock",
            "InventoryOutCard"
        )

        self.value_card = InventoryStatCard(
            "Inventory Value",
            "₹0.00",
            "Current cost value",
            "InventoryValueCard"
        )

        layout.addWidget(
            self.total_card
        )

        layout.addWidget(
            self.low_card
        )

        layout.addWidget(
            self.out_card
        )

        layout.addWidget(
            self.value_card
        )

    def set_data(self, stats):

        self.total_card.set_value(
            stats.get("total_items", 0)
        )

        self.low_card.set_value(
            stats.get("low_stock", 0)
        )

        self.out_card.set_value(
            stats.get("out_of_stock", 0)
        )

        value = stats.get(
            "inventory_value",
            0
        )

        self.value_card.set_value(
            f"₹{value:,.2f}"
        )