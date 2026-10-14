from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QTextEdit,
    QComboBox,
    QDateEdit,
    QDoubleSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QFrame,
    QGridLayout,
    QScrollArea,
)

from PySide6.QtCore import (
    QDate,
    Signal,
    Qt,
)

import qtawesome as qta

from data.customer_crud import get_all_customers

from data.order_crud import (
    create_order,
    update_order,
)


class OrderForm(QWidget):

    backClicked = Signal()
    orderSaved = Signal(dict)

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setObjectName(
            "OrderForm"
        )

        self.current_order_id = None

        self.setup_ui()
        self.load_customers()

    # ==========================================================
    # UI
    # ==========================================================

    def setup_ui(self):

        self.setStyleSheet("""
        /* =====================================================
           MAIN
           ===================================================== */

        QWidget#OrderForm {
            background: #111827;
            color: #F9FAFB;
            font-family: Segoe UI;
        }

        QScrollArea {
            border: none;
            background: #111827;
        }

        /* =====================================================
           HEADER
           ===================================================== */

        QLabel#Title {
            color: #FFFFFF;
            font-size: 24px;
            font-weight: 700;
        }

        QLabel#Subtitle {
            color: #9CA3AF;
            font-size: 13px;
        }

        QPushButton#BackButton {
            background: #374151;
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-size: 13px;
            font-weight: 600;
        }

        QPushButton#BackButton:hover {
            background: #4B5563;
        }

        QPushButton#BackButton:pressed {
            background: #1F2937;
        }

        /* =====================================================
           CARDS
           ===================================================== */

        QFrame#OrderCard {
            background: #18212F;
            border: 1px solid #263244;
            border-radius: 14px;
        }

        QFrame#SummaryCard {
            background: #18212F;
            border: 1px solid #263244;
            border-radius: 14px;
        }

        QFrame#ActionCard {
            background: #18212F;
            border: 1px solid #263244;
            border-radius: 14px;
        }

        QLabel#CardTitle {
            color: #F9FAFB;
            font-size: 16px;
            font-weight: 700;
        }

        QLabel#CardSubtitle {
            color: #94A3B8;
            font-size: 12px;
        }

        QLabel#FieldLabel {
            color: #CBD5E1;
            font-size: 12px;
            font-weight: 600;
        }

        QLabel#CustomerInfo {
            background: #1F2937;
            color: #CBD5E1;
            border-radius: 8px;
            padding: 10px;
            font-size: 13px;
        }

        /* =====================================================
           INPUTS
           ===================================================== */

        QLineEdit,
        QComboBox,
        QDateEdit,
        QDoubleSpinBox,
        QTextEdit {

            background: #1F2937;
            color: #F9FAFB;
            border: 1px solid #374151;
            border-radius: 9px;
            padding: 9px 11px;
            font-size: 13px;
        }

        QLineEdit,
        QComboBox,
        QDateEdit,
        QDoubleSpinBox {
            min-height: 22px;
        }

        QLineEdit:hover,
        QComboBox:hover,
        QDateEdit:hover,
        QDoubleSpinBox:hover,
        QTextEdit:hover {
            border: 1px solid #4B5563;
        }

        QLineEdit:focus,
        QComboBox:focus,
        QDateEdit:focus,
        QDoubleSpinBox:focus,
        QTextEdit:focus {
            border: 2px solid #3B82F6;
        }

        QComboBox::drop-down,
        QDateEdit::drop-down {
            border: none;
            width: 30px;
        }

        QComboBox QAbstractItemView {
            background: #1F2937;
            color: #F9FAFB;
            border: 1px solid #374151;
            selection-background-color: #2563EB;
            selection-color: white;
        }

        /* =====================================================
           SUMMARY
           ===================================================== */

        QLabel#SummaryLabel {
            color: #9CA3AF;
            font-size: 12px;
        }

        QLabel#SummaryValue {
            color: #FFFFFF;
            font-size: 20px;
            font-weight: 700;
        }

        /* =====================================================
           BUTTONS
           ===================================================== */

        QPushButton {
            border: none;
            border-radius: 9px;
            padding: 10px 18px;
            font-size: 13px;
            font-weight: 600;
        }

        QPushButton#CancelButton {
            background: #374151;
            color: #FFFFFF;
        }

        QPushButton#CancelButton:hover {
            background: #4B5563;
        }

        QPushButton#SaveButton {
            background: #2563EB;
            color: #FFFFFF;
            min-width: 140px;
        }

        QPushButton#SaveButton:hover {
            background: #3B82F6;
        }

        QPushButton#SaveButton:pressed {
            background: #1D4ED8;
        }

        /* =====================================================
           SCROLLBAR
           ===================================================== */

        QScrollBar:vertical {
            background: #111827;
            width: 8px;
            margin: 2px;
        }

        QScrollBar::handle:vertical {
            background: #374151;
            border-radius: 4px;
            min-height: 30px;
        }

        QScrollBar::handle:vertical:hover {
            background: #4B5563;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0;
        }

        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {
            background: transparent;
        }
        """)

        # ======================================================
        # MAIN
        # ======================================================

        main_layout = QVBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        # ======================================================
        # SCROLL
        # ======================================================

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setFrameShape(
            QScrollArea.NoFrame
        )

        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        # ======================================================
        # CONTAINER
        # ======================================================

        self.container = QWidget()

        self.root = QVBoxLayout(
            self.container
        )

        self.root.setContentsMargins(
            20,
            20,
            20,
            30
        )

        self.root.setSpacing(
            16
        )

        # ======================================================
        # TOP HEADER
        # ======================================================

        header_layout = QHBoxLayout()

        header_layout.setSpacing(
            12
        )

        # ------------------------------------------------------
        # TITLE
        # ------------------------------------------------------

        title_box = QVBoxLayout()

        title_box.setSpacing(
            2
        )

        self.title = QLabel(
            "Add New Order"
        )

        self.title.setObjectName(
            "Title"
        )

        self.subtitle = QLabel(
            "Create a tailoring order and record payment details."
        )

        self.subtitle.setObjectName(
            "Subtitle"
        )

        title_box.addWidget(
            self.title
        )

        title_box.addWidget(
            self.subtitle
        )

        header_layout.addLayout(
            title_box
        )

        # ------------------------------------------------------
        # PUSH BACK BUTTON RIGHT
        # ------------------------------------------------------

        header_layout.addStretch()

        # ------------------------------------------------------
        # BACK
        # ------------------------------------------------------

        self.back_btn = QPushButton(
            "←  Back"
        )

        self.back_btn.setObjectName(
            "BackButton"
        )

        self.back_btn.setCursor(
            Qt.PointingHandCursor
        )

        self.back_btn.clicked.connect(
            self.backClicked.emit
        )

        header_layout.addWidget(
            self.back_btn,
            0,
            Qt.AlignRight | Qt.AlignVCenter
        )

        self.root.addLayout(
            header_layout
        )

        # ======================================================
        # CUSTOMER + ORDER INFORMATION
        # ======================================================

        top_row = QHBoxLayout()

        top_row.setSpacing(
            16
        )

        # ======================================================
        # CUSTOMER CARD
        # ======================================================

        customer_card = QFrame()

        customer_card.setObjectName(
            "OrderCard"
        )

        customer_layout = QVBoxLayout(
            customer_card
        )

        customer_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        customer_layout.setSpacing(
            12
        )

        customer_title = QLabel(
            "Customer"
        )

        customer_title.setObjectName(
            "CardTitle"
        )

        customer_layout.addWidget(
            customer_title
        )

        customer_subtitle = QLabel(
            "Select the customer for this order."
        )

        customer_subtitle.setObjectName(
            "CardSubtitle"
        )

        customer_layout.addWidget(
            customer_subtitle
        )

        customer_label = QLabel(
            "Customer"
        )

        customer_label.setObjectName(
            "FieldLabel"
        )

        customer_layout.addWidget(
            customer_label
        )

        self.customer_search = QComboBox()

        self.customer_search.setEditable(
            True
        )

        self.customer_search.setInsertPolicy(
            QComboBox.NoInsert
        )

        self.customer_search.setPlaceholderText(
            "Select customer"
        )

        self.customer_search.setMinimumHeight(
            40
        )

        self.customer_search.currentIndexChanged.connect(
            self.customer_changed
        )

        customer_layout.addWidget(
            self.customer_search
        )

        mobile_label = QLabel(
            "Mobile"
        )

        mobile_label.setObjectName(
            "FieldLabel"
        )

        customer_layout.addWidget(
            mobile_label
        )

        self.mobile_label = QLabel(
            "—"
        )

        self.mobile_label.setObjectName(
            "CustomerInfo"
        )

        customer_layout.addWidget(
            self.mobile_label
        )

        top_row.addWidget(
            customer_card,
            1
        )

        # ======================================================
        # ORDER INFORMATION CARD
        # ======================================================

        order_card = QFrame()

        order_card.setObjectName(
            "OrderCard"
        )

        order_layout = QVBoxLayout(
            order_card
        )

        order_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        order_layout.setSpacing(
            12
        )

        order_title = QLabel(
            "Order Information"
        )

        order_title.setObjectName(
            "CardTitle"
        )

        order_layout.addWidget(
            order_title
        )

        order_subtitle = QLabel(
            "Set dates and current order status."
        )

        order_subtitle.setObjectName(
            "CardSubtitle"
        )

        order_layout.addWidget(
            order_subtitle
        )

        order_grid = QGridLayout()

        order_grid.setHorizontalSpacing(
            16
        )

        order_grid.setVerticalSpacing(
            8
        )

        # Order date
        order_date_label = QLabel(
            "Order Date"
        )

        order_date_label.setObjectName(
            "FieldLabel"
        )

        self.order_date = QDateEdit()

        self.order_date.setCalendarPopup(
            True
        )

        self.order_date.setDate(
            QDate.currentDate()
        )

        # Delivery
        delivery_date_label = QLabel(
            "Delivery Date"
        )

        delivery_date_label.setObjectName(
            "FieldLabel"
        )

        self.delivery_date = QDateEdit()

        self.delivery_date.setCalendarPopup(
            True
        )

        self.delivery_date.setDate(
            QDate.currentDate().addDays(7)
        )

        # Status
        status_label = QLabel(
            "Status"
        )

        status_label.setObjectName(
            "FieldLabel"
        )

        self.status = QComboBox()

        self.status.addItems([
            "pending",
            "measurement",
            "cutting",
            "stitching",
            "ironing",
            "trial",
            "ready",
            "delivered",
            "cancelled",
        ])

        order_grid.addWidget(
            order_date_label,
            0,
            0
        )

        order_grid.addWidget(
            delivery_date_label,
            0,
            1
        )

        order_grid.addWidget(
            self.order_date,
            1,
            0
        )

        order_grid.addWidget(
            self.delivery_date,
            1,
            1
        )

        order_grid.addWidget(
            status_label,
            2,
            0
        )

        order_grid.addWidget(
            self.status,
            3,
            0
        )

        order_grid.setColumnStretch(
            0,
            1
        )

        order_grid.setColumnStretch(
            1,
            1
        )

        order_layout.addLayout(
            order_grid
        )

        top_row.addWidget(
            order_card,
            2
        )

        self.root.addLayout(
            top_row
        )

        # ======================================================
        # GARMENT DETAILS
        # ======================================================

        garment_card = self.create_card(
            "Garment Details",
            "Specify garment, quantity, price and tailoring instructions."
        )

        garment_layout = garment_card.layout()

        garment_grid = QGridLayout()

        garment_grid.setHorizontalSpacing(
            16
        )

        garment_grid.setVerticalSpacing(
            8
        )

        # Garment
        garment_label = QLabel(
            "Garment"
        )

        garment_label.setObjectName(
            "FieldLabel"
        )

        self.cloth_type = QComboBox()

        self.cloth_type.addItems([
            "Shirt",
            "Pant",
            "Suit",
            "Kurta",
            "Blazer",
            "Sherwani",
            "Other",
        ])

        # Quantity
        quantity_label = QLabel(
            "Quantity"
        )

        quantity_label.setObjectName(
            "FieldLabel"
        )

        self.quantity = QComboBox()

        self.quantity.addItems([
            str(i)
            for i in range(1, 11)
        ])

        # Unit price
        price_label = QLabel(
            "Unit Price"
        )

        price_label.setObjectName(
            "FieldLabel"
        )

        self.unit_price = self.make_money_spin()

        # Description
        description_label = QLabel(
            "Description"
        )

        description_label.setObjectName(
            "FieldLabel"
        )

        self.description = QTextEdit()

        self.description.setPlaceholderText(
            "Enter cloth, fitting, design or stitching details..."
        )

        self.description.setMinimumHeight(
            95
        )

        garment_grid.addWidget(
            garment_label,
            0,
            0
        )

        garment_grid.addWidget(
            quantity_label,
            0,
            1
        )

        garment_grid.addWidget(
            price_label,
            0,
            2
        )

        garment_grid.addWidget(
            self.cloth_type,
            1,
            0
        )

        garment_grid.addWidget(
            self.quantity,
            1,
            1
        )

        garment_grid.addWidget(
            self.unit_price,
            1,
            2
        )

        garment_grid.addWidget(
            description_label,
            2,
            0
        )

        garment_grid.addWidget(
            self.description,
            3,
            0,
            1,
            3
        )

        garment_grid.setColumnStretch(
            0,
            1
        )

        garment_grid.setColumnStretch(
            1,
            1
        )

        garment_grid.setColumnStretch(
            2,
            1
        )

        garment_layout.addLayout(
            garment_grid
        )

        self.root.addWidget(
            garment_card
        )

        # ======================================================
        # PRICING + PAYMENT
        # ======================================================

        financial_row = QHBoxLayout()

        financial_row.setSpacing(
            16
        )

        # ======================================================
        # PRICING
        # ======================================================

        pricing_card = self.create_card(
            "Pricing",
            "Review order amount, discount and tax."
        )

        pricing_layout = pricing_card.layout()

        pricing_grid = QGridLayout()

        pricing_grid.setHorizontalSpacing(
            16
        )

        pricing_grid.setVerticalSpacing(
            8
        )

        subtotal_label = QLabel(
            "Subtotal"
        )

        subtotal_label.setObjectName(
            "FieldLabel"
        )

        self.subtotal = self.make_money_spin()

        discount_label = QLabel(
            "Discount"
        )

        discount_label.setObjectName(
            "FieldLabel"
        )

        self.discount = self.make_money_spin()

        tax_label = QLabel(
            "Tax"
        )

        tax_label.setObjectName(
            "FieldLabel"
        )

        self.tax = self.make_money_spin()

        total_label = QLabel(
            "Grand Total"
        )

        total_label.setObjectName(
            "FieldLabel"
        )

        self.total_amount = self.make_money_spin()

        self.total_amount.setReadOnly(
            True
        )

        pricing_grid.addWidget(
            subtotal_label,
            0,
            0
        )

        pricing_grid.addWidget(
            discount_label,
            0,
            1
        )

        pricing_grid.addWidget(
            self.subtotal,
            1,
            0
        )

        pricing_grid.addWidget(
            self.discount,
            1,
            1
        )

        pricing_grid.addWidget(
            tax_label,
            2,
            0
        )

        pricing_grid.addWidget(
            total_label,
            2,
            1
        )

        pricing_grid.addWidget(
            self.tax,
            3,
            0
        )

        pricing_grid.addWidget(
            self.total_amount,
            3,
            1
        )

        pricing_grid.setColumnStretch(
            0,
            1
        )

        pricing_grid.setColumnStretch(
            1,
            1
        )

        pricing_layout.addLayout(
            pricing_grid
        )

        financial_row.addWidget(
            pricing_card,
            1
        )

        # ======================================================
        # PAYMENT
        # ======================================================

        payment_card = self.create_card(
            "Payment",
            "Record advance and payment method."
        )

        payment_layout = payment_card.layout()

        payment_grid = QGridLayout()

        payment_grid.setHorizontalSpacing(
            16
        )

        payment_grid.setVerticalSpacing(
            8
        )

        advance_label = QLabel(
            "Advance"
        )

        advance_label.setObjectName(
            "FieldLabel"
        )

        self.advance_amount = self.make_money_spin()

        method_label = QLabel(
            "Payment Method"
        )

        method_label.setObjectName(
            "FieldLabel"
        )

        self.payment_method = QComboBox()

        self.payment_method.addItems([
            "cash",
            "upi",
            "card",
            "bank",
        ])

        remaining_label = QLabel(
            "Remaining"
        )

        remaining_label.setObjectName(
            "FieldLabel"
        )

        self.remaining_amount = self.make_money_spin()

        self.remaining_amount.setReadOnly(
            True
        )

        payment_grid.addWidget(
            advance_label,
            0,
            0
        )

        payment_grid.addWidget(
            method_label,
            0,
            1
        )

        payment_grid.addWidget(
            self.advance_amount,
            1,
            0
        )

        payment_grid.addWidget(
            self.payment_method,
            1,
            1
        )

        payment_grid.addWidget(
            remaining_label,
            2,
            0
        )

        payment_grid.addWidget(
            self.remaining_amount,
            3,
            0
        )

        payment_grid.setColumnStretch(
            0,
            1
        )

        payment_grid.setColumnStretch(
            1,
            1
        )

        payment_layout.addLayout(
            payment_grid
        )

        financial_row.addWidget(
            payment_card,
            1
        )

        self.root.addLayout(
            financial_row
        )

        # ======================================================
        # NOTES
        # ======================================================

        notes_card = self.create_card(
            "Notes",
            "Add special instructions, customer preferences or delivery notes."
        )

        notes_layout = notes_card.layout()

        self.notes = QTextEdit()

        self.notes.setPlaceholderText(
            "Special instructions, customer preferences, delivery notes..."
        )

        self.notes.setMinimumHeight(
            110
        )

        notes_layout.addWidget(
            self.notes
        )

        self.root.addWidget(
            notes_card
        )

        # ======================================================
        # SUMMARY
        # ======================================================

        summary_card = QFrame()

        summary_card.setObjectName(
            "SummaryCard"
        )

        summary_layout = QHBoxLayout(
            summary_card
        )

        summary_layout.setContentsMargins(
            20,
            16,
            20,
            16
        )

        summary_layout.setSpacing(
            30
        )

        self.summary_total = self.create_summary_block(
            "Grand Total",
            "₹0.00"
        )

        self.summary_advance = self.create_summary_block(
            "Advance",
            "₹0.00"
        )

        self.summary_remaining = self.create_summary_block(
            "Remaining",
            "₹0.00"
        )

        summary_layout.addWidget(
            self.summary_total
        )

        summary_layout.addWidget(
            self.summary_advance
        )

        summary_layout.addWidget(
            self.summary_remaining
        )

        summary_layout.addStretch()

        self.root.addWidget(
            summary_card
        )

        # ======================================================
        # ACTION BUTTONS
        # ======================================================

        action_card = QFrame()

        action_card.setObjectName(
            "ActionCard"
        )

        action_layout = QHBoxLayout(
            action_card
        )

        action_layout.setContentsMargins(
            20,
            14,
            20,
            14
        )

        action_layout.addStretch()

        self.cancel_btn = QPushButton(
            "Cancel"
        )

        self.cancel_btn.setObjectName(
            "CancelButton"
        )

        self.cancel_btn.setCursor(
            Qt.PointingHandCursor
        )

        self.cancel_btn.clicked.connect(
            self.backClicked.emit
        )

        self.save_btn = QPushButton(
            "  Save Order"
        )

        self.save_btn.setObjectName(
            "SaveButton"
        )

        self.save_btn.setCursor(
            Qt.PointingHandCursor
        )

        self.save_btn.setIcon(
            qta.icon(
                "fa5s.save",
                color="white"
            )
        )

        self.save_btn.clicked.connect(
            self.save_order
        )

        action_layout.addWidget(
            self.cancel_btn
        )

        action_layout.addWidget(
            self.save_btn
        )

        self.root.addWidget(
            action_card
        )

        # ======================================================
        # SCROLL
        # ======================================================

        self.scroll.setWidget(
            self.container
        )

        main_layout.addWidget(
            self.scroll
        )

        # ======================================================
        # CALCULATIONS
        # ======================================================

        self.quantity.currentTextChanged.connect(
            self.calculate_totals
        )

        self.unit_price.valueChanged.connect(
            self.calculate_totals
        )

        self.discount.valueChanged.connect(
            self.calculate_totals
        )

        self.tax.valueChanged.connect(
            self.calculate_totals
        )

        self.advance_amount.valueChanged.connect(
            self.calculate_totals
        )

    # ==========================================================
    # CARD HELPER
    # ==========================================================

    def create_card(
        self,
        title,
        subtitle=None
    ):

        card = QFrame()

        card.setObjectName(
            "OrderCard"
        )

        layout = QVBoxLayout(
            card
        )

        layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        layout.setSpacing(
            12
        )

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "CardTitle"
        )

        layout.addWidget(
            title_label
        )

        if subtitle:

            subtitle_label = QLabel(
                subtitle
            )

            subtitle_label.setObjectName(
                "CardSubtitle"
            )

            layout.addWidget(
                subtitle_label
            )

        return card

    # ==========================================================
    # MONEY FIELD
    # ==========================================================

    def make_money_spin(self):

        widget = QDoubleSpinBox()

        widget.setMaximum(
            99999999
        )

        widget.setDecimals(
            2
        )

        widget.setPrefix(
            "₹ "
        )

        widget.setMinimumHeight(
            40
        )

        return widget

    # ==========================================================
    # SUMMARY BLOCK
    # ==========================================================

    def create_summary_block(
        self,
        title,
        value
    ):

        widget = QWidget()

        layout = QVBoxLayout(
            widget
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(
            3
        )

        label = QLabel(
            title
        )

        label.setObjectName(
            "SummaryLabel"
        )

        value_label = QLabel(
            value
        )

        value_label.setObjectName(
            "SummaryValue"
        )

        layout.addWidget(
            label
        )

        layout.addWidget(
            value_label
        )

        widget.value_label = (
            value_label
        )

        return widget

    # ==========================================================
    # LOAD CUSTOMERS
    # ==========================================================

    def load_customers(self):

        try:

            customers = get_all_customers()

            self.customer_search.blockSignals(
                True
            )

            self.customer_search.clear()

            self.customer_search.addItem(
                "Select Customer",
                None
            )

            for customer in customers:

                name = customer.get(
                    "name",
                    ""
                )

                mobile = customer.get(
                    "mobile",
                    ""
                )

                customer_id = customer.get(
                    "id"
                )

                text = name

                if mobile:

                    text += f" - {mobile}"

                self.customer_search.addItem(
                    text,
                    {
                        "id": customer_id,
                        "name": name,
                        "mobile": mobile,
                    }
                )

            self.customer_search.blockSignals(
                False
            )

        except Exception as e:

            QMessageBox.warning(
                self,
                "Customer Error",
                f"Unable to load customers:\n\n{e}"
            )

    # ==========================================================
    # CUSTOMER CHANGED
    # ==========================================================

    def customer_changed(
        self,
        index
    ):

        data = (
            self.customer_search.itemData(
                index
            )
        )

        if not data:

            self.mobile_label.setText(
                "—"
            )

            return

        self.mobile_label.setText(
            data.get(
                "mobile"
            )
            or "—"
        )

    # ==========================================================
    # CALCULATE
    # ==========================================================

    def calculate_totals(self):

        quantity = int(
            self.quantity.currentText()
        )

        unit_price = (
            self.unit_price.value()
        )

        subtotal = (
            quantity
            * unit_price
        )

        discount = (
            self.discount.value()
        )

        tax = (
            self.tax.value()
        )

        total = max(
            subtotal
            - discount
            + tax,
            0
        )

        advance = (
            self.advance_amount.value()
        )

        remaining = max(
            total
            - advance,
            0
        )

        # ------------------------------------------------------
        # FIELDS
        # ------------------------------------------------------

        self.subtotal.blockSignals(
            True
        )

        self.subtotal.setValue(
            subtotal
        )

        self.subtotal.blockSignals(
            False
        )

        self.total_amount.blockSignals(
            True
        )

        self.total_amount.setValue(
            total
        )

        self.total_amount.blockSignals(
            False
        )

        self.remaining_amount.blockSignals(
            True
        )

        self.remaining_amount.setValue(
            remaining
        )

        self.remaining_amount.blockSignals(
            False
        )

        # ------------------------------------------------------
        # SUMMARY
        # ------------------------------------------------------

        self.summary_total.value_label.setText(
            f"₹{total:,.2f}"
        )

        self.summary_advance.value_label.setText(
            f"₹{advance:,.2f}"
        )

        self.summary_remaining.value_label.setText(
            f"₹{remaining:,.2f}"
        )

    # ==========================================================
    # PREPARE NEW
    # ==========================================================

    def prepare_new(self):

        self.current_order_id = None

        self.title.setText(
            "Add New Order"
        )

        self.subtitle.setText(
            "Create a tailoring order and record payment details."
        )

        self.save_btn.setText(
            "  Save Order"
        )

        self.clear_form()

    # ==========================================================
    # LOAD ORDER
    # ==========================================================

    def load_order(
        self,
        order
    ):

        self.current_order_id = (
            order["id"]
        )

        self.title.setText(
            f"Edit Order #{order['order_number']}"
        )

        self.subtitle.setText(
            "Update order, garment and payment information."
        )

        self.save_btn.setText(
            "  Update Order"
        )

        # ======================================================
        # CUSTOMER
        # ======================================================

        customer_id = (
            order.get(
                "customer_id"
            )
        )

        for i in range(
            self.customer_search.count()
        ):

            data = (
                self.customer_search.itemData(
                    i
                )
            )

            if (
                data
                and data.get("id")
                == customer_id
            ):

                self.customer_search.setCurrentIndex(
                    i
                )

                break

        # ======================================================
        # DATES
        # ======================================================

        if order.get(
            "order_date"
        ):

            self.order_date.setDate(
                QDate.fromString(
                    order["order_date"],
                    "yyyy-MM-dd"
                )
            )

        if order.get(
            "delivery_date"
        ):

            self.delivery_date.setDate(
                QDate.fromString(
                    order["delivery_date"],
                    "yyyy-MM-dd"
                )
            )

        # ======================================================
        # STATUS
        # ======================================================

        index = self.status.findText(
            order.get(
                "status",
                "pending"
            )
        )

        if index >= 0:

            self.status.setCurrentIndex(
                index
            )

        # ======================================================
        # ITEM
        # ======================================================

        item = order.get(
            "item"
        )

        if item:

            garment_index = (
                self.cloth_type.findText(
                    item.get(
                        "garment_type",
                        ""
                    )
                )
            )

            if garment_index >= 0:

                self.cloth_type.setCurrentIndex(
                    garment_index
                )

            self.quantity.setCurrentText(
                str(
                    item.get(
                        "quantity",
                        1
                    )
                )
            )

            self.unit_price.setValue(
                float(
                    item.get(
                        "unit_price",
                        0
                    )
                )
            )

            self.description.setPlainText(
                item.get(
                    "description",
                    ""
                )
            )

        # ======================================================
        # PRICING
        # ======================================================

        self.discount.setValue(
            float(
                order.get(
                    "discount",
                    0
                )
            )
        )

        self.tax.setValue(
            float(
                order.get(
                    "tax",
                    0
                )
            )
        )

        self.advance_amount.setValue(
            float(
                order.get(
                    "advance_amount",
                    0
                )
            )
        )

        # ======================================================
        # NOTES
        # ======================================================

        self.notes.setPlainText(
            order.get(
                "description",
                ""
            )
        )

        self.calculate_totals()

    # ==========================================================
    # SAVE
    # ==========================================================

    def save_order(self):

        customer_data = (
            self.customer_search.currentData()
        )

        if not customer_data:

            QMessageBox.warning(
                self,
                "Validation",
                "Please select a customer."
            )

            return

        quantity = int(
            self.quantity.currentText()
        )

        unit_price = (
            self.unit_price.value()
        )

        if unit_price <= 0:

            QMessageBox.warning(
                self,
                "Validation",
                "Please enter garment price."
            )

            return

        self.calculate_totals()

        order_data = {

            "customer_id":
                customer_data["id"],

            "order_date":
                self.order_date.date().toString(
                    "yyyy-MM-dd"
                ),

            "delivery_date":
                self.delivery_date.date().toString(
                    "yyyy-MM-dd"
                ),

            "status":
                self.status.currentText(),

            "subtotal":
                self.subtotal.value(),

            "discount":
                self.discount.value(),

            "tax":
                self.tax.value(),

            "total_amount":
                self.total_amount.value(),

            "advance_amount":
                self.advance_amount.value(),

            "remaining_amount":
                self.remaining_amount.value(),

            "description":
                self.notes.toPlainText(),

            "garment_type":
                self.cloth_type.currentText(),

            "item_description":
                self.description.toPlainText(),

            "quantity":
                quantity,

            "unit_price":
                unit_price,

            "payment_method":
                self.payment_method.currentText(),
        }

        try:

            if self.current_order_id:

                saved = update_order(
                    self.current_order_id,
                    order_data
                )

                message = (
                    "Order updated successfully."
                )

            else:

                saved = create_order(
                    order_data
                )

                message = (
                    "Order created successfully."
                )

            if saved:

                QMessageBox.information(
                    self,
                    "Success",
                    message
                )

                self.orderSaved.emit(
                    saved
                )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"Unable to save order:\n\n{e}"
            )

    # ==========================================================
    # CLEAR
    # ==========================================================

    def clear_form(self):

        self.customer_search.setCurrentIndex(
            0
        )

        self.order_date.setDate(
            QDate.currentDate()
        )

        self.delivery_date.setDate(
            QDate.currentDate().addDays(7)
        )

        self.status.setCurrentText(
            "pending"
        )

        self.cloth_type.setCurrentIndex(
            0
        )

        self.quantity.setCurrentText(
            "1"
        )

        self.unit_price.setValue(
            0
        )

        self.subtotal.setValue(
            0
        )

        self.discount.setValue(
            0
        )

        self.tax.setValue(
            0
        )

        self.total_amount.setValue(
            0
        )

        self.advance_amount.setValue(
            0
        )

        self.remaining_amount.setValue(
            0
        )

        self.description.clear()

        self.notes.clear()

        self.payment_method.setCurrentText(
            "cash"
        )

        self.mobile_label.setText(
            "—"
        )

        self.calculate_totals()