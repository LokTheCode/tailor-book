from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout
)

from PySide6.QtCore import Qt

import qtawesome as qta


class OrderSummary(QFrame):

    def __init__(self):
        super().__init__()

        self.build_ui()

    # -----------------------------------------------------

    def build_ui(self):

        self.setObjectName("Card")


        root = QVBoxLayout(self)

        root.setContentsMargins(20,20,20,20)

        root.setSpacing(18)

        # =====================================================
        # Header
        # =====================================================

        header = QHBoxLayout()

        title = QLabel("Order Summary")

        title.setObjectName("CardTitle")

        header.addWidget(title)

        header.addStretch()

        icon = QLabel()

        icon.setPixmap(

            qta.icon(
                "fa5s.clipboard-list",
                color="#3B82F6"
            ).pixmap(24,24)

        )

        header.addWidget(icon)

        root.addLayout(header)

        # =====================================================
        # Summary Grid
        # =====================================================

        grid = QGridLayout()

        grid.setHorizontalSpacing(20)

        grid.setVerticalSpacing(12)

        row = 0

        self.customer = self.create_row(
            grid,
            row,
            "Customer"
        )
        row += 1

        self.mobile = self.create_row(
            grid,
            row,
            "Mobile"
        )
        row += 1

        self.garments = self.create_row(
            grid,
            row,
            "Garments"
        )
        row += 1

        self.quantity = self.create_row(
            grid,
            row,
            "Quantity"
        )
        row += 1

        self.delivery = self.create_row(
            grid,
            row,
            "Delivery"
        )
        row += 1

        self.status = self.create_row(
            grid,
            row,
            "Status"
        )
        row += 1

        self.payment = self.create_row(
            grid,
            row,
            "Payment"
        )

        root.addLayout(grid)

        # =====================================================
        # Divider
        # =====================================================

        line = QFrame()

        line.setObjectName("Separator")


        root.addWidget(line)

        # =====================================================
        # Amounts
        # =====================================================

        amountGrid = QGridLayout()

        self.subtotal = self.create_row(
            amountGrid,
            0,
            "Subtotal"
        )

        self.discount = self.create_row(
            amountGrid,
            1,
            "Discount"
        )

        self.gst = self.create_row(
            amountGrid,
            2,
            "GST"
        )

        self.advance = self.create_row(
            amountGrid,
            3,
            "Advance"
        )

        self.balance = self.create_row(
            amountGrid,
            4,
            "Balance"
        )

        root.addLayout(amountGrid)

        # =====================================================
        # Total Card
        # =====================================================

        totalCard = QFrame()

        totalCard.setObjectName("InnerPanel")


        totalLayout = QVBoxLayout(totalCard)

        totalLayout.setAlignment(Qt.AlignCenter)

        lbl = QLabel("GRAND TOTAL")

        lbl.setAlignment(Qt.AlignCenter)

        totalLayout.addWidget(lbl)

        self.total = QLabel("₹ 0.00")

        self.total.setObjectName("AmountText")

        self.total.setAlignment(Qt.AlignCenter)

        totalLayout.addWidget(self.total)

        root.addWidget(totalCard)

        root.addStretch()

        self.clear()

    # -----------------------------------------------------

    def create_row(
        self,
        layout,
        row,
        title
    ):

        lbl = QLabel(title)

        value = QLabel("-")

        value.setObjectName("ValueText")

        value.setAlignment(
            Qt.AlignRight |
            Qt.AlignVCenter
        )

        layout.addWidget(
            lbl,
            row,
            0
        )

        layout.addWidget(
            value,
            row,
            1
        )

        return value

    # -----------------------------------------------------

    def set_customer(
        self,
        name,
        mobile
    ):

        self.customer.setText(name)

        self.mobile.setText(mobile)

    # -----------------------------------------------------

    def set_garments(
        self,
        garments,
        qty
    ):

        self.garments.setText(
            str(garments)
        )

        self.quantity.setText(
            str(qty)
        )

    # -----------------------------------------------------

    def set_delivery(
        self,
        date,
        status
    ):

        self.delivery.setText(date)

        self.status.setText(status)

    # -----------------------------------------------------

    def set_payment_status(
        self,
        status
    ):

        self.payment.setText(status)

    # -----------------------------------------------------

    def set_amounts(
        self,
        subtotal,
        discount,
        gst,
        advance,
        balance,
        total
    ):

        self.subtotal.setText(
            f"₹ {subtotal:,.2f}"
        )

        self.discount.setText(
            f"{discount}%"
        )

        self.gst.setText(
            f"{gst}%"
        )

        self.advance.setText(
            f"₹ {advance:,.2f}"
        )

        self.balance.setText(
            f"₹ {balance:,.2f}"
        )

        self.total.setText(
            f"₹ {total:,.2f}"
        )

    # -----------------------------------------------------

    def clear(self):

        self.customer.setText("-")

        self.mobile.setText("-")

        self.garments.setText("0")

        self.quantity.setText("0")

        self.delivery.setText("-")

        self.status.setText("New")

        self.payment.setText("Pending")

        self.subtotal.setText("₹ 0.00")

        self.discount.setText("0%")

        self.gst.setText("0%")

        self.advance.setText("₹ 0.00")

        self.balance.setText("₹ 0.00")

        self.total.setText("₹ 0.00")