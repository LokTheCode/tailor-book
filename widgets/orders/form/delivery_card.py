from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QComboBox,
    QDateEdit,
    QTextEdit,
    QCheckBox,
    QSpinBox,
    QPushButton
)

from PySide6.QtCore import (
    Qt,
    Signal,
    QDate
)

import qtawesome as qta


class DeliveryCard(QFrame):

    dataChanged = Signal()

    def __init__(self):
        super().__init__()

        self.build_ui()

    # --------------------------------------------------------

    def build_ui(self):

        self.setObjectName("DeliveryCard")

        self.setStyleSheet("""

        QFrame#DeliveryCard{

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

        QComboBox,
        QDateEdit,
        QTextEdit,
        QSpinBox{

            background:#111827;

            color:white;

            border:1px solid #374151;

            border-radius:8px;

            padding:8px;

            min-height:38px;

        }

        QTextEdit{

            min-height:90px;

        }

        QCheckBox{

            color:white;

            spacing:8px;

        }

        """)

        root = QVBoxLayout(self)

        root.setContentsMargins(20,20,20,20)

        root.setSpacing(20)

        # =====================================================
        # Header
        # =====================================================

        header = QHBoxLayout()

        title = QLabel("Delivery Information")

        title.setObjectName("Title")

        header.addWidget(title)

        header.addStretch()

        icon = QLabel()

        icon.setPixmap(

            qta.icon(
                "fa5s.truck",
                color="#3B82F6"
            ).pixmap(24,24)

        )

        header.addWidget(icon)

        root.addLayout(header)

        # =====================================================
        # Delivery Dates
        # =====================================================

        dateFrame = QFrame()

        dateLayout = QGridLayout(dateFrame)

        dateLayout.setHorizontalSpacing(15)

        dateLayout.setVerticalSpacing(12)

        # -----------------------------------------------------
        # Order Date
        # -----------------------------------------------------

        dateLayout.addWidget(
            QLabel("Order Date"),
            0,
            0
        )

        self.orderDate = QDateEdit()

        self.orderDate.setCalendarPopup(True)

        self.orderDate.setDate(
            QDate.currentDate()
        )

        dateLayout.addWidget(
            self.orderDate,
            0,
            1
        )

        # -----------------------------------------------------
        # Delivery Date
        # -----------------------------------------------------

        dateLayout.addWidget(
            QLabel("Delivery Date"),
            0,
            2
        )

        self.deliveryDate = QDateEdit()

        self.deliveryDate.setCalendarPopup(True)

        self.deliveryDate.setDate(
            QDate.currentDate().addDays(7)
        )

        dateLayout.addWidget(
            self.deliveryDate,
            0,
            3
        )

        # -----------------------------------------------------
        # Trial Date
        # -----------------------------------------------------

        dateLayout.addWidget(
            QLabel("Trial Date"),
            1,
            0
        )

        self.trialDate = QDateEdit()

        self.trialDate.setCalendarPopup(True)

        self.trialDate.setDate(
            QDate.currentDate().addDays(5)
        )

        dateLayout.addWidget(
            self.trialDate,
            1,
            1
        )

        # -----------------------------------------------------
        # Estimated Days
        # -----------------------------------------------------

        dateLayout.addWidget(
            QLabel("Estimated Days"),
            1,
            2
        )

        self.days = QSpinBox()

        self.days.setRange(
            1,
            365
        )

        self.days.setValue(7)

        dateLayout.addWidget(
            self.days,
            1,
            3
        )

        root.addWidget(
            dateFrame
        )

        # =====================================================
        # Delivery Options
        # =====================================================

        optionFrame = QFrame()

        optionLayout = QGridLayout(optionFrame)

        optionLayout.setHorizontalSpacing(15)

        optionLayout.setVerticalSpacing(12)

        # -----------------------------------------------------
        # Priority
        # -----------------------------------------------------

        optionLayout.addWidget(
            QLabel("Priority"),
            0,
            0
        )

        self.priority = QComboBox()

        self.priority.addItems([

            "Normal",

            "Urgent",

            "VIP"

        ])

        optionLayout.addWidget(
            self.priority,
            0,
            1
        )

        # -----------------------------------------------------
        # Trial Required
        # -----------------------------------------------------

        optionLayout.addWidget(
            QLabel("Trial Required"),
            0,
            2
        )

        self.trialRequired = QCheckBox(
            "Yes"
        )

        self.trialRequired.setChecked(True)

        optionLayout.addWidget(
            self.trialRequired,
            0,
            3
        )

        root.addWidget(
            optionFrame
        )

                # =====================================================
        # DELIVERY DETAILS
        # =====================================================

        detailFrame = QFrame()

        detailLayout = QGridLayout(detailFrame)

        detailLayout.setHorizontalSpacing(15)

        detailLayout.setVerticalSpacing(12)

        # -----------------------------------------------------
        # Delivery Method
        # -----------------------------------------------------

        detailLayout.addWidget(
            QLabel("Delivery Method"),
            0,
            0
        )

        self.deliveryMethod = QComboBox()

        self.deliveryMethod.addItems([

            "Customer Pickup",

            "Home Delivery",

            "Courier",

            "Transport",

            "Other"

        ])

        detailLayout.addWidget(
            self.deliveryMethod,
            0,
            1
        )

        # -----------------------------------------------------
        # Delivery Status
        # -----------------------------------------------------

        detailLayout.addWidget(
            QLabel("Delivery Status"),
            0,
            2
        )

        self.deliveryStatus = QComboBox()

        self.deliveryStatus.addItems([

            "Pending",

            "Ready",

            "Dispatched",

            "Delivered"

        ])

        detailLayout.addWidget(
            self.deliveryStatus,
            0,
            3
        )

        # -----------------------------------------------------
        # Assigned Tailor
        # -----------------------------------------------------

        detailLayout.addWidget(
            QLabel("Assigned Tailor"),
            1,
            0
        )

        self.tailor = QComboBox()

        self.tailor.addItems([

            "Auto Assign",

            "Ramesh",

            "Rahul",

            "Amit",

            "Deepak"

        ])

        detailLayout.addWidget(
            self.tailor,
            1,
            1
        )

        # -----------------------------------------------------
        # Delivery Person
        # -----------------------------------------------------

        detailLayout.addWidget(
            QLabel("Delivery Person"),
            1,
            2
        )

        self.deliveryPerson = QComboBox()

        self.deliveryPerson.addItems([

            "Not Assigned",

            "Shop Staff",

            "Courier Partner"

        ])

        detailLayout.addWidget(
            self.deliveryPerson,
            1,
            3
        )

        root.addWidget(detailFrame)

        # =====================================================
        # DELIVERY ADDRESS
        # =====================================================

        addressFrame = QFrame()

        addressLayout = QVBoxLayout(addressFrame)

        addressLayout.setSpacing(10)

        addressLayout.addWidget(
            QLabel("Delivery Address")
        )

        self.deliveryAddress = QTextEdit()

        self.deliveryAddress.setPlaceholderText(

            "Enter complete delivery address..."

        )

        self.deliveryAddress.setMaximumHeight(90)

        addressLayout.addWidget(
            self.deliveryAddress
        )

        root.addWidget(
            addressFrame
        )

        # =====================================================
        # DELIVERY NOTES
        # =====================================================

        notesFrame = QFrame()

        notesLayout = QVBoxLayout(notesFrame)

        notesLayout.setSpacing(10)

        notesLayout.addWidget(
            QLabel("Delivery Notes")
        )

        self.deliveryNotes = QTextEdit()

        self.deliveryNotes.setPlaceholderText(

            "Special delivery instructions...\n"
            "• Call before delivery\n"
            "• Evening delivery only\n"
            "• Urgent delivery\n"
            "• Packing instructions"

        )

        notesLayout.addWidget(
            self.deliveryNotes
        )

        root.addWidget(
            notesFrame
        )

        # =====================================================
        # SIGNALS
        # =====================================================

        self.orderDate.dateChanged.connect(
            self.dataChanged.emit
        )

        self.deliveryDate.dateChanged.connect(
            self.dataChanged.emit
        )

        self.trialDate.dateChanged.connect(
            self.dataChanged.emit
        )

        self.days.valueChanged.connect(
            self.update_delivery_date
        )

        self.priority.currentIndexChanged.connect(
            self.dataChanged.emit
        )

        self.deliveryMethod.currentIndexChanged.connect(
            self.dataChanged.emit
        )

        self.deliveryStatus.currentIndexChanged.connect(
            self.dataChanged.emit
        )

        self.tailor.currentIndexChanged.connect(
            self.dataChanged.emit
        )

        self.deliveryPerson.currentIndexChanged.connect(
            self.dataChanged.emit
        )

        self.deliveryAddress.textChanged.connect(
            self.dataChanged.emit
        )

        self.deliveryNotes.textChanged.connect(
            self.dataChanged.emit
        )

        self.trialRequired.toggled.connect(
            self.dataChanged.emit
        )

            # --------------------------------------------------------
    # Update Delivery Date
    # --------------------------------------------------------

    def update_delivery_date(self):

        delivery = self.orderDate.date().addDays(
            self.days.value()
        )

        self.deliveryDate.setDate(
            delivery
        )

        self.dataChanged.emit()

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    def validate(self):

        if self.deliveryDate.date() < self.orderDate.date():

            return (
                False,
                "Delivery date cannot be before order date."
            )

        if (
            self.trialRequired.isChecked()
            and
            self.trialDate.date() > self.deliveryDate.date()
        ):

            return (
                False,
                "Trial date must be before delivery date."
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

            "order_date":
                self.orderDate.date().toString(
                    "yyyy-MM-dd"
                ),

            "delivery_date":
                self.deliveryDate.date().toString(
                    "yyyy-MM-dd"
                ),

            "trial_date":
                self.trialDate.date().toString(
                    "yyyy-MM-dd"
                ),

            "estimated_days":
                self.days.value(),

            "priority":
                self.priority.currentText(),

            "trial_required":
                self.trialRequired.isChecked(),

            "delivery_method":
                self.deliveryMethod.currentText(),

            "delivery_status":
                self.deliveryStatus.currentText(),

            "assigned_tailor":
                self.tailor.currentText(),

            "delivery_person":
                self.deliveryPerson.currentText(),

            "delivery_address":
                self.deliveryAddress.toPlainText(),

            "delivery_notes":
                self.deliveryNotes.toPlainText()

        }

    # --------------------------------------------------------
    # Set Data
    # --------------------------------------------------------

    def set_data(self, data):

        if data.get("order_date"):

            self.orderDate.setDate(
                QDate.fromString(
                    data["order_date"],
                    "yyyy-MM-dd"
                )
            )

        if data.get("delivery_date"):

            self.deliveryDate.setDate(
                QDate.fromString(
                    data["delivery_date"],
                    "yyyy-MM-dd"
                )
            )

        if data.get("trial_date"):

            self.trialDate.setDate(
                QDate.fromString(
                    data["trial_date"],
                    "yyyy-MM-dd"
                )
            )

        self.days.setValue(
            data.get(
                "estimated_days",
                7
            )
        )

        self.priority.setCurrentText(
            data.get(
                "priority",
                "Normal"
            )
        )

        self.trialRequired.setChecked(
            data.get(
                "trial_required",
                True
            )
        )

        self.deliveryMethod.setCurrentText(
            data.get(
                "delivery_method",
                "Customer Pickup"
            )
        )

        self.deliveryStatus.setCurrentText(
            data.get(
                "delivery_status",
                "Pending"
            )
        )

        self.tailor.setCurrentText(
            data.get(
                "assigned_tailor",
                "Auto Assign"
            )
        )

        self.deliveryPerson.setCurrentText(
            data.get(
                "delivery_person",
                "Not Assigned"
            )
        )

        self.deliveryAddress.setPlainText(
            data.get(
                "delivery_address",
                ""
            )
        )

        self.deliveryNotes.setPlainText(
            data.get(
                "delivery_notes",
                ""
            )
        )

    # --------------------------------------------------------
    # Clear Form
    # --------------------------------------------------------

    def clear_form(self):

        self.orderDate.setDate(
            QDate.currentDate()
        )

        self.days.setValue(7)

        self.deliveryDate.setDate(
            QDate.currentDate().addDays(7)
        )

        self.trialDate.setDate(
            QDate.currentDate().addDays(5)
        )

        self.priority.setCurrentIndex(0)

        self.trialRequired.setChecked(True)

        self.deliveryMethod.setCurrentIndex(0)

        self.deliveryStatus.setCurrentIndex(0)

        self.tailor.setCurrentIndex(0)

        self.deliveryPerson.setCurrentIndex(0)

        self.deliveryAddress.clear()

        self.deliveryNotes.clear()

    # --------------------------------------------------------
    # String Representation
    # --------------------------------------------------------

    def __str__(self):

        return (
            f"Delivery : "
            f"{self.deliveryDate.date().toString('dd MMM yyyy')}"
        )