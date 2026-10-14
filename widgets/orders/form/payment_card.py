from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLineEdit,
    QDoubleSpinBox,
    QComboBox,
    QTextEdit,
    QPushButton
)

from PySide6.QtCore import (
    Qt,
    Signal
)

import qtawesome as qta


class PaymentCard(QFrame):

    paymentChanged = Signal()

    def __init__(self):
        super().__init__()

        self.build_ui()

    # --------------------------------------------------------

    def build_ui(self):

        self.setObjectName("PaymentCard")

        self.setStyleSheet("""

        QFrame#PaymentCard{

            background:#1F2937;

            border:1px solid #374151;

            border-radius:15px;

        }

        QLabel#Title{

            color:white;

            font-size:18px;

            font-weight:bold;

        }

        QLabel{

            color:#D1D5DB;

            font-size:13px;

        }

        QDoubleSpinBox,
        QComboBox,
        QLineEdit,
        QTextEdit{

            background:#111827;

            color:white;

            border:1px solid #374151;

            border-radius:8px;

            padding:8px;

            min-height:38px;

        }

        QTextEdit{

            min-height:80px;

        }

        QPushButton{

            background:#2563EB;

            color:white;

            border:none;

            border-radius:8px;

            padding:8px 16px;

        }

        QPushButton:hover{

            background:#1D4ED8;

        }

        """)

        root = QVBoxLayout(self)

        root.setContentsMargins(20,20,20,20)

        root.setSpacing(20)

        # =====================================================
        # Header
        # =====================================================

        header = QHBoxLayout()

        title = QLabel("Payment Information")

        title.setObjectName("Title")

        header.addWidget(title)

        header.addStretch()

        icon = QLabel()

        icon.setPixmap(

            qta.icon(
                "fa5s.wallet",
                color="#10B981"
            ).pixmap(24,24)

        )

        header.addWidget(icon)

        root.addLayout(header)

        # =====================================================
        # Pricing
        # =====================================================

        priceFrame = QFrame()

        priceLayout = QGridLayout(priceFrame)

        priceLayout.setHorizontalSpacing(15)

        priceLayout.setVerticalSpacing(12)

        # ----------------------------------------

        priceLayout.addWidget(
            QLabel("Subtotal"),
            0,
            0
        )

        self.subtotal = QDoubleSpinBox()

        self.subtotal.setRange(
            0,
            999999
        )

        self.subtotal.setPrefix("₹ ")

        self.subtotal.setDecimals(2)

        priceLayout.addWidget(
            self.subtotal,
            0,
            1
        )

        # ----------------------------------------

        priceLayout.addWidget(
            QLabel("Discount %"),
            0,
            2
        )

        self.discount = QDoubleSpinBox()

        self.discount.setRange(
            0,
            100
        )

        self.discount.setSuffix(" %")

        priceLayout.addWidget(
            self.discount,
            0,
            3
        )

        # ----------------------------------------

        priceLayout.addWidget(
            QLabel("GST %"),
            1,
            0
        )

        self.gst = QDoubleSpinBox()

        self.gst.setRange(
            0,
            100
        )

        self.gst.setValue(18)

        self.gst.setSuffix(" %")

        priceLayout.addWidget(
            self.gst,
            1,
            1
        )

        # ----------------------------------------

        priceLayout.addWidget(
            QLabel("Total"),
            1,
            2
        )

        self.total = QLineEdit()

        self.total.setReadOnly(True)

        self.total.setText("₹ 0.00")

        priceLayout.addWidget(
            self.total,
            1,
            3
        )

        root.addWidget(
            priceFrame
        )

        # =====================================================
        # PAYMENT
        # =====================================================

        paymentFrame = QFrame()

        paymentLayout = QGridLayout(paymentFrame)

        paymentLayout.setHorizontalSpacing(15)

        paymentLayout.setVerticalSpacing(12)

        # ----------------------------------------

        paymentLayout.addWidget(
            QLabel("Advance Paid"),
            0,
            0
        )

        self.advance = QDoubleSpinBox()

        self.advance.setRange(
            0,
            999999
        )

        self.advance.setDecimals(2)

        self.advance.setPrefix("₹ ")

        paymentLayout.addWidget(
            self.advance,
            0,
            1
        )

        # ----------------------------------------

        paymentLayout.addWidget(
            QLabel("Payment Mode"),
            0,
            2
        )

        self.paymentMode = QComboBox()

        self.paymentMode.addItems([

            "Cash",

            "UPI",

            "Card",

            "Bank Transfer",

            "Cheque",

            "Wallet"

        ])

        paymentLayout.addWidget(
            self.paymentMode,
            0,
            3
        )

        # ----------------------------------------

        paymentLayout.addWidget(
            QLabel("Transaction ID"),
            1,
            0
        )

        self.transactionId = QLineEdit()

        self.transactionId.setPlaceholderText(
            "Optional"
        )

        paymentLayout.addWidget(
            self.transactionId,
            1,
            1,
            1,
            3
        )

        root.addWidget(
            paymentFrame
        )

                # =====================================================
        # PAYMENT SUMMARY
        # =====================================================

        summaryFrame = QFrame()

        summaryFrame.setObjectName("SummaryFrame")

        summaryFrame.setStyleSheet("""

        QFrame#SummaryFrame{

            background:#111827;

            border:1px solid #374151;

            border-radius:10px;

        }

        QLabel#Amount{

            color:#10B981;

            font-size:22px;

            font-weight:bold;

        }

        """)

        summaryLayout = QGridLayout(summaryFrame)

        summaryLayout.setHorizontalSpacing(15)

        summaryLayout.setVerticalSpacing(12)

        # -----------------------------------------------------
        # Balance
        # -----------------------------------------------------

        summaryLayout.addWidget(
            QLabel("Balance Amount"),
            0,
            0
        )

        self.balance = QLineEdit()

        self.balance.setReadOnly(True)

        self.balance.setText("₹ 0.00")

        summaryLayout.addWidget(
            self.balance,
            0,
            1
        )

        # -----------------------------------------------------
        # Payment Status
        # -----------------------------------------------------

        summaryLayout.addWidget(
            QLabel("Payment Status"),
            0,
            2
        )

        self.paymentStatus = QLabel("Pending")

        self.paymentStatus.setObjectName("Amount")

        summaryLayout.addWidget(
            self.paymentStatus,
            0,
            3
        )

        # -----------------------------------------------------
        # Due Date
        # -----------------------------------------------------

        summaryLayout.addWidget(
            QLabel("Due Days"),
            1,
            0
        )

        self.dueDays = QComboBox()

        self.dueDays.addItems([

            "0 Day",

            "3 Days",

            "7 Days",

            "15 Days",

            "30 Days"

        ])

        summaryLayout.addWidget(
            self.dueDays,
            1,
            1
        )

        # -----------------------------------------------------
        # Receipt Required
        # -----------------------------------------------------

        summaryLayout.addWidget(
            QLabel("Receipt"),
            1,
            2
        )

        self.receipt = QComboBox()

        self.receipt.addItems([

            "Print",

            "Email",

            "WhatsApp",

            "No Receipt"

        ])

        summaryLayout.addWidget(
            self.receipt,
            1,
            3
        )

        root.addWidget(summaryFrame)

        # =====================================================
        # PAYMENT NOTES
        # =====================================================

        notesFrame = QFrame()

        notesLayout = QVBoxLayout(notesFrame)

        notesLayout.addWidget(
            QLabel("Payment Notes")
        )

        self.notes = QTextEdit()

        self.notes.setPlaceholderText(

            "Payment remarks...\n"
            "• Advance received\n"
            "• Remaining after delivery\n"
            "• Customer requested credit"

        )

        notesLayout.addWidget(
            self.notes
        )

        root.addWidget(notesFrame)

        # =====================================================
        # QUICK PAYMENT BUTTONS
        # =====================================================

        quickLayout = QHBoxLayout()

        quickLayout.addWidget(
            QLabel("Quick Advance")
        )

        self.btn25 = QPushButton("25%")

        self.btn50 = QPushButton("50%")

        self.btn75 = QPushButton("75%")

        self.btn100 = QPushButton("100%")

        quickLayout.addWidget(self.btn25)

        quickLayout.addWidget(self.btn50)

        quickLayout.addWidget(self.btn75)

        quickLayout.addWidget(self.btn100)

        quickLayout.addStretch()

        root.addLayout(quickLayout)

        # =====================================================
        # SIGNALS
        # =====================================================

        self.subtotal.valueChanged.connect(
            self.calculate_payment
        )

        self.discount.valueChanged.connect(
            self.calculate_payment
        )

        self.gst.valueChanged.connect(
            self.calculate_payment
        )

        self.advance.valueChanged.connect(
            self.calculate_payment
        )

        self.btn25.clicked.connect(
            lambda: self.set_percentage(25)
        )

        self.btn50.clicked.connect(
            lambda: self.set_percentage(50)
        )

        self.btn75.clicked.connect(
            lambda: self.set_percentage(75)
        )

        self.btn100.clicked.connect(
            lambda: self.set_percentage(100)
        )

        self.paymentMode.currentIndexChanged.connect(
            self.paymentChanged.emit
        )

        self.transactionId.textChanged.connect(
            self.paymentChanged.emit
        )

        self.notes.textChanged.connect(
            self.paymentChanged.emit
        )

        self.calculate_payment()

            # --------------------------------------------------------
    # Calculate Payment
    # --------------------------------------------------------

    def calculate_payment(self):

        subtotal = self.subtotal.value()

        discount = self.discount.value()

        gst = self.gst.value()

        advance = self.advance.value()

        # Discount

        discount_amount = subtotal * discount / 100

        taxable = subtotal - discount_amount

        # GST

        gst_amount = taxable * gst / 100

        grand_total = taxable + gst_amount

        balance = grand_total - advance

        if balance < 0:

            balance = 0

        self.total.setText(
            f"₹ {grand_total:,.2f}"
        )

        self.balance.setText(
            f"₹ {balance:,.2f}"
        )

        # Payment Status

        if advance <= 0:

            status = "Pending"

            color = "#EF4444"

        elif balance <= 0:

            status = "Paid"

            color = "#10B981"

        else:

            status = "Partial"

            color = "#F59E0B"

        self.paymentStatus.setText(status)

        self.paymentStatus.setStyleSheet(f"""
            QLabel{{
                color:{color};
                font-size:20px;
                font-weight:bold;
            }}
        """)

        self.paymentChanged.emit()

    # --------------------------------------------------------
    # Quick Percentage
    # --------------------------------------------------------

    def set_percentage(self, percent):

        subtotal = self.subtotal.value()

        discount_amount = subtotal * self.discount.value() / 100

        taxable = subtotal - discount_amount

        gst_amount = taxable * self.gst.value() / 100

        grand_total = taxable + gst_amount

        advance = grand_total * percent / 100

        self.advance.setValue(advance)

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    def validate(self):

        if self.subtotal.value() <= 0:

            return (
                False,
                "Subtotal must be greater than zero."
            )

        if self.advance.value() > (
            self.subtotal.value() * 2
        ):

            return (
                False,
                "Advance amount looks incorrect."
            )

        return (
            True,
            ""
        )

    # --------------------------------------------------------
    # Get Data
    # --------------------------------------------------------

    def get_data(self):

        return {

            "subtotal": self.subtotal.value(),

            "discount": self.discount.value(),

            "gst": self.gst.value(),

            "total": self.total.text(),

            "advance": self.advance.value(),

            "balance": self.balance.text(),

            "payment_mode":
                self.paymentMode.currentText(),

            "transaction_id":
                self.transactionId.text(),

            "payment_status":
                self.paymentStatus.text(),

            "due_days":
                self.dueDays.currentText(),

            "receipt":
                self.receipt.currentText(),

            "notes":
                self.notes.toPlainText()

        }

    # --------------------------------------------------------
    # Set Data
    # --------------------------------------------------------

    def set_data(self, data):

        self.subtotal.setValue(
            data.get("subtotal", 0)
        )

        self.discount.setValue(
            data.get("discount", 0)
        )

        self.gst.setValue(
            data.get("gst", 18)
        )

        self.advance.setValue(
            data.get("advance", 0)
        )

        self.paymentMode.setCurrentText(
            data.get(
                "payment_mode",
                "Cash"
            )
        )

        self.transactionId.setText(
            data.get(
                "transaction_id",
                ""
            )
        )

        self.dueDays.setCurrentText(
            data.get(
                "due_days",
                "0 Day"
            )
        )

        self.receipt.setCurrentText(
            data.get(
                "receipt",
                "Print"
            )
        )

        self.notes.setPlainText(
            data.get(
                "notes",
                ""
            )
        )

        self.calculate_payment()

    # --------------------------------------------------------
    # Clear
    # --------------------------------------------------------

    def clear_form(self):

        self.subtotal.setValue(0)

        self.discount.setValue(0)

        self.gst.setValue(18)

        self.advance.setValue(0)

        self.paymentMode.setCurrentIndex(0)

        self.transactionId.clear()

        self.dueDays.setCurrentIndex(0)

        self.receipt.setCurrentIndex(0)

        self.notes.clear()

        self.calculate_payment()

    # --------------------------------------------------------
    # String
    # --------------------------------------------------------

    def __str__(self):

        return (
            f"Total : {self.total.text()} | "
            f"Balance : {self.balance.text()}"
        )