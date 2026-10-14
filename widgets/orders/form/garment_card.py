from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QLineEdit,
    QCheckBox,
    QTextEdit,
    QDateEdit
)

from PySide6.QtCore import (
    Qt,
    Signal,
    QDate
)

import qtawesome as qta


class GarmentCard(QFrame):

    removeClicked = Signal()

    totalChanged = Signal()

    # --------------------------------------------------------

    def __init__(self, index=1):

        super().__init__()

        self.index = index

        self.build_ui()

    # --------------------------------------------------------

    def build_ui(self):

        self.setObjectName("GarmentCard")

        self.setStyleSheet("""

        QFrame#GarmentCard{

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

        QLineEdit,
        QTextEdit,
        QComboBox,
        QSpinBox,
        QDoubleSpinBox,
        QDateEdit{

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

        QCheckBox{

            color:white;

        }

        QPushButton{

            border:none;

            border-radius:8px;

            padding:8px 14px;

            color:white;

            background:#2563EB;

        }

        QPushButton:hover{

            background:#1D4ED8;

        }

        QPushButton#Remove{

            background:#DC2626;

        }

        QPushButton#Remove:hover{

            background:#B91C1C;

        }

        """)

        root = QVBoxLayout(self)

        root.setContentsMargins(20,20,20,20)

        root.setSpacing(20)

        # =====================================================
        # Header
        # =====================================================

        header = QHBoxLayout()

        title = QLabel(
            f"Garment #{self.index}"
        )

        title.setObjectName("Title")

        header.addWidget(title)

        header.addStretch()

        self.removeBtn = QPushButton(" Remove")

        self.removeBtn.setObjectName("Remove")

        self.removeBtn.setIcon(
            qta.icon(
                "fa5s.trash",
                color="white"
            )
        )

        self.removeBtn.clicked.connect(
            self.removeClicked.emit
        )

        header.addWidget(self.removeBtn)

        root.addLayout(header)

        # =====================================================
        # BASIC INFORMATION
        # =====================================================

        basicFrame = QFrame()

        basicLayout = QGridLayout(basicFrame)

        basicLayout.setHorizontalSpacing(15)

        basicLayout.setVerticalSpacing(12)

        # Garment

        basicLayout.addWidget(
            QLabel("Garment"),
            0,
            0
        )

        self.garment = QComboBox()

        self.garment.addItems([

            "Shirt",

            "Pant",

            "Suit",

            "Kurta",

            "Blazer",

            "Sherwani",

            "Waist Coat",

            "Safari Suit",

            "Jacket"

        ])

        basicLayout.addWidget(
            self.garment,
            0,
            1
        )

        # Quantity

        basicLayout.addWidget(
            QLabel("Quantity"),
            0,
            2
        )

        self.qty = QSpinBox()

        self.qty.setMinimum(1)

        self.qty.setMaximum(100)

        self.qty.setValue(1)

        basicLayout.addWidget(
            self.qty,
            0,
            3
        )

        # Measurement Version

        basicLayout.addWidget(
            QLabel("Measurement"),
            1,
            0
        )

        self.measurement = QComboBox()

        self.measurement.addItems([

            "Latest Measurement",

            "Version 1",

            "Version 2",

            "Version 3"

        ])

        basicLayout.addWidget(
            self.measurement,
            1,
            1
        )

        # Priority

        basicLayout.addWidget(
            QLabel("Priority"),
            1,
            2
        )

        self.priority = QComboBox()

        self.priority.addItems([

            "Normal",

            "Urgent",

            "VIP"

        ])

        basicLayout.addWidget(
            self.priority,
            1,
            3
        )

        root.addWidget(
            basicFrame
        )

        # =====================================================
        # FABRIC INFORMATION
        # =====================================================

        fabricFrame = QFrame()

        fabricLayout = QGridLayout(fabricFrame)

        fabricLayout.setHorizontalSpacing(15)

        fabricLayout.setVerticalSpacing(12)

        fabricLayout.addWidget(
            QLabel("Fabric"),
            0,
            0
        )

        self.fabric = QComboBox()

        self.fabric.addItems([

            "Customer Fabric",

            "Raymond",

            "Arvind",

            "Blackberry",

            "Cotton",

            "Linen",

            "Silk"

        ])

        fabricLayout.addWidget(
            self.fabric,
            0,
            1
        )

        fabricLayout.addWidget(
            QLabel("Color"),
            0,
            2
        )

        self.color = QComboBox()

        self.color.addItems([

            "Black",

            "Blue",

            "White",

            "Grey",

            "Brown",

            "Cream",

            "Custom"

        ])

        fabricLayout.addWidget(
            self.color,
            0,
            3
        )

        fabricLayout.addWidget(
            QLabel("Fabric Source"),
            1,
            0
        )

        self.fabricSource = QComboBox()

        self.fabricSource.addItems([

            "Customer",

            "Shop"

        ])

        fabricLayout.addWidget(
            self.fabricSource,
            1,
            1
        )

        root.addWidget(
            fabricFrame
        )

                # =====================================================
        # DESIGN & STITCHING INFORMATION
        # =====================================================

        designFrame = QFrame()

        designLayout = QGridLayout(designFrame)

        designLayout.setHorizontalSpacing(15)

        designLayout.setVerticalSpacing(12)

        # -----------------------------------------------------
        # Sleeve
        # -----------------------------------------------------

        designLayout.addWidget(
            QLabel("Sleeve"),
            0,
            0
        )

        self.sleeve = QComboBox()

        self.sleeve.addItems([

            "Half Sleeve",

            "Full Sleeve",

            "3/4 Sleeve",

            "Sleeveless",

            "Custom"

        ])

        designLayout.addWidget(
            self.sleeve,
            0,
            1
        )

        # -----------------------------------------------------
        # Collar
        # -----------------------------------------------------

        designLayout.addWidget(
            QLabel("Collar"),
            0,
            2
        )

        self.collar = QComboBox()

        self.collar.addItems([

            "Regular",

            "Chinese",

            "Mandarin",

            "Button Down",

            "Spread",

            "Custom"

        ])

        designLayout.addWidget(
            self.collar,
            0,
            3
        )

        # -----------------------------------------------------
        # Pocket
        # -----------------------------------------------------

        designLayout.addWidget(
            QLabel("Pocket"),
            1,
            0
        )

        self.pocket = QComboBox()

        self.pocket.addItems([

            "No Pocket",

            "Single",

            "Double",

            "Hidden",

            "Flap Pocket"

        ])

        designLayout.addWidget(
            self.pocket,
            1,
            1
        )

        # -----------------------------------------------------
        # Button Style
        # -----------------------------------------------------

        designLayout.addWidget(
            QLabel("Buttons"),
            1,
            2
        )

        self.buttons = QComboBox()

        self.buttons.addItems([

            "Plastic",

            "Metal",

            "Wooden",

            "Designer",

            "Customer Choice"

        ])

        designLayout.addWidget(
            self.buttons,
            1,
            3
        )

        # -----------------------------------------------------
        # Lining
        # -----------------------------------------------------

        designLayout.addWidget(
            QLabel("Lining"),
            2,
            0
        )

        self.lining = QComboBox()

        self.lining.addItems([

            "No",

            "Cotton",

            "Silk",

            "Premium"

        ])

        designLayout.addWidget(
            self.lining,
            2,
            1
        )

        # -----------------------------------------------------
        # Embroidery
        # -----------------------------------------------------

        designLayout.addWidget(
            QLabel("Embroidery"),
            2,
            2
        )

        self.embroidery = QComboBox()

        self.embroidery.addItems([

            "No",

            "Name",

            "Logo",

            "Custom"

        ])

        designLayout.addWidget(
            self.embroidery,
            2,
            3
        )

        root.addWidget(designFrame)

        # =====================================================
        # PRODUCTION INFORMATION
        # =====================================================

        productionFrame = QFrame()

        productionLayout = QGridLayout(productionFrame)

        productionLayout.setHorizontalSpacing(15)

        productionLayout.setVerticalSpacing(12)

        # -----------------------------------------------------
        # Tailor
        # -----------------------------------------------------

        productionLayout.addWidget(
            QLabel("Assigned Tailor"),
            0,
            0
        )

        self.tailor = QComboBox()

        self.tailor.addItems([

            "Auto Assign",

            "Ramesh",

            "Amit",

            "Rahul",

            "Deepak"

        ])

        productionLayout.addWidget(
            self.tailor,
            0,
            1
        )

        # -----------------------------------------------------
        # Trial Required
        # -----------------------------------------------------

        productionLayout.addWidget(
            QLabel("Trial"),
            0,
            2
        )

        self.trial = QCheckBox(
            "Trial Required"
        )

        self.trial.setChecked(True)

        productionLayout.addWidget(
            self.trial,
            0,
            3
        )

        # -----------------------------------------------------
        # Delivery Date
        # -----------------------------------------------------

        productionLayout.addWidget(
            QLabel("Delivery"),
            1,
            0
        )

        self.deliveryDate = QDateEdit()

        self.deliveryDate.setCalendarPopup(True)

        self.deliveryDate.setDate(
            QDate.currentDate().addDays(7)
        )

        productionLayout.addWidget(
            self.deliveryDate,
            1,
            1
        )

        # -----------------------------------------------------
        # Estimated Days
        # -----------------------------------------------------

        productionLayout.addWidget(
            QLabel("Estimated Days"),
            1,
            2
        )

        self.days = QSpinBox()

        self.days.setRange(1, 90)

        self.days.setValue(7)

        productionLayout.addWidget(
            self.days,
            1,
            3
        )

        root.addWidget(
            productionFrame
        )

                # =====================================================
        # PRICING INFORMATION
        # =====================================================

        pricingFrame = QFrame()

        pricingLayout = QGridLayout(pricingFrame)

        pricingLayout.setHorizontalSpacing(15)

        pricingLayout.setVerticalSpacing(12)

        # -----------------------------------------------------
        # Unit Price
        # -----------------------------------------------------

        pricingLayout.addWidget(
            QLabel("Unit Price"),
            0,
            0
        )

        self.unitPrice = QDoubleSpinBox()

        self.unitPrice.setRange(
            0,
            100000
        )

        self.unitPrice.setDecimals(2)

        self.unitPrice.setPrefix("₹ ")

        self.unitPrice.setValue(0)

        pricingLayout.addWidget(
            self.unitPrice,
            0,
            1
        )

        # -----------------------------------------------------
        # Quantity
        # -----------------------------------------------------

        pricingLayout.addWidget(
            QLabel("Quantity"),
            0,
            2
        )

        self.quantity = QSpinBox()

        self.quantity.setRange(
            1,
            999
        )

        self.quantity.setValue(1)

        pricingLayout.addWidget(
            self.quantity,
            0,
            3
        )

        # -----------------------------------------------------
        # Discount
        # -----------------------------------------------------

        pricingLayout.addWidget(
            QLabel("Discount"),
            1,
            0
        )

        self.discount = QDoubleSpinBox()

        self.discount.setRange(
            0,
            100
        )

        self.discount.setSuffix(" %")

        pricingLayout.addWidget(
            self.discount,
            1,
            1
        )

        # -----------------------------------------------------
        # GST
        # -----------------------------------------------------

        pricingLayout.addWidget(
            QLabel("GST"),
            1,
            2
        )

        self.gst = QDoubleSpinBox()

        self.gst.setRange(
            0,
            100
        )

        self.gst.setValue(18)

        self.gst.setSuffix(" %")

        pricingLayout.addWidget(
            self.gst,
            1,
            3
        )

        # -----------------------------------------------------
        # Total
        # -----------------------------------------------------

        pricingLayout.addWidget(
            QLabel("Total"),
            2,
            0
        )

        self.total = QLineEdit()

        self.total.setReadOnly(True)

        self.total.setText("₹ 0.00")

        pricingLayout.addWidget(
            self.total,
            2,
            1
        )

        root.addWidget(
            pricingFrame
        )

        # =====================================================
        # SPECIAL INSTRUCTIONS
        # =====================================================

        notesFrame = QFrame()

        notesLayout = QVBoxLayout(notesFrame)

        notesLayout.addWidget(
            QLabel("Special Instructions")
        )

        self.notes = QTextEdit()

        self.notes.setPlaceholderText(

            "Write stitching instructions...\n"
            "• Collar style\n"
            "• Pocket position\n"
            "• Fitting notes\n"
            "• Customer requests"

        )

        self.notes.setMinimumHeight(100)

        notesLayout.addWidget(
            self.notes
        )

        root.addWidget(
            notesFrame
        )

        # =====================================================
        # FOOTER
        # =====================================================

        footer = QHBoxLayout()

        footer.addStretch()

        self.totalLabel = QLabel(
            "Garment Total : ₹ 0.00"
        )

        self.totalLabel.setStyleSheet("""

        QLabel{

            color:#10B981;

            font-size:18px;

            font-weight:bold;

        }

        """)

        footer.addWidget(
            self.totalLabel
        )

        root.addLayout(
            footer
        )

        # =====================================================
        # SIGNALS
        # =====================================================

        self.unitPrice.valueChanged.connect(
            self.calculate_total
        )

        self.quantity.valueChanged.connect(
            self.calculate_total
        )

        self.discount.valueChanged.connect(
            self.calculate_total
        )

        self.gst.valueChanged.connect(
            self.calculate_total
        )

        self.calculate_total()

            # --------------------------------------------------------
    # Calculate Garment Total
    # --------------------------------------------------------

    def calculate_total(self):

        qty = self.quantity.value()

        rate = self.unitPrice.value()

        discount = self.discount.value()

        gst = self.gst.value()

        subtotal = qty * rate

        discount_amount = subtotal * discount / 100

        taxable = subtotal - discount_amount

        gst_amount = taxable * gst / 100

        grand_total = taxable + gst_amount

        self.total.setText(
            f"₹ {grand_total:,.2f}"
        )

        self.totalLabel.setText(
            f"Garment Total : ₹ {grand_total:,.2f}"
        )

        self.totalChanged.emit()

    # --------------------------------------------------------
    # Get Garment Data
    # --------------------------------------------------------

    def get_data(self):

        return {

            "garment": self.garment.currentText(),

            "measurement": self.measurement.currentText(),

            "priority": self.priority.currentText(),

            "fabric": self.fabric.currentText(),

            "color": self.color.currentText(),

            "fabric_source": self.fabricSource.currentText(),

            "sleeve": self.sleeve.currentText(),

            "collar": self.collar.currentText(),

            "pocket": self.pocket.currentText(),

            "buttons": self.buttons.currentText(),

            "lining": self.lining.currentText(),

            "embroidery": self.embroidery.currentText(),

            "tailor": self.tailor.currentText(),

            "trial_required": self.trial.isChecked(),

            "delivery_date": self.deliveryDate.date().toString(
                "yyyy-MM-dd"
            ),

            "estimated_days": self.days.value(),

            "quantity": self.quantity.value(),

            "unit_price": self.unitPrice.value(),

            "discount": self.discount.value(),

            "gst": self.gst.value(),

            "notes": self.notes.toPlainText(),

            "total": self.total.text()

        }

    # --------------------------------------------------------
    # Set Existing Data
    # --------------------------------------------------------

    def set_data(self, data):

        self.garment.setCurrentText(
            data.get("garment", "")
        )

        self.measurement.setCurrentText(
            data.get("measurement", "")
        )

        self.priority.setCurrentText(
            data.get("priority", "Normal")
        )

        self.fabric.setCurrentText(
            data.get("fabric", "")
        )

        self.color.setCurrentText(
            data.get("color", "")
        )

        self.fabricSource.setCurrentText(
            data.get("fabric_source", "Customer")
        )

        self.sleeve.setCurrentText(
            data.get("sleeve", "")
        )

        self.collar.setCurrentText(
            data.get("collar", "")
        )

        self.pocket.setCurrentText(
            data.get("pocket", "")
        )

        self.buttons.setCurrentText(
            data.get("buttons", "")
        )

        self.lining.setCurrentText(
            data.get("lining", "")
        )

        self.embroidery.setCurrentText(
            data.get("embroidery", "")
        )

        self.tailor.setCurrentText(
            data.get("tailor", "")
        )

        self.trial.setChecked(
            data.get("trial_required", True)
        )

        self.days.setValue(
            data.get("estimated_days", 7)
        )

        self.quantity.setValue(
            data.get("quantity", 1)
        )

        self.unitPrice.setValue(
            data.get("unit_price", 0)
        )

        self.discount.setValue(
            data.get("discount", 0)
        )

        self.gst.setValue(
            data.get("gst", 18)
        )

        self.notes.setPlainText(
            data.get("notes", "")
        )

        self.calculate_total()

    # --------------------------------------------------------
    # Clear Form
    # --------------------------------------------------------

    def clear_form(self):

        self.garment.setCurrentIndex(0)

        self.measurement.setCurrentIndex(0)

        self.priority.setCurrentIndex(0)

        self.fabric.setCurrentIndex(0)

        self.color.setCurrentIndex(0)

        self.fabricSource.setCurrentIndex(0)

        self.sleeve.setCurrentIndex(0)

        self.collar.setCurrentIndex(0)

        self.pocket.setCurrentIndex(0)

        self.buttons.setCurrentIndex(0)

        self.lining.setCurrentIndex(0)

        self.embroidery.setCurrentIndex(0)

        self.tailor.setCurrentIndex(0)

        self.trial.setChecked(True)

        self.days.setValue(7)

        self.quantity.setValue(1)

        self.unitPrice.setValue(0)

        self.discount.setValue(0)

        self.gst.setValue(18)

        self.notes.clear()

        self.calculate_total()

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    def validate(self):

        if self.garment.currentText().strip() == "":

            return False, "Please select a garment."

        if self.quantity.value() <= 0:

            return False, "Quantity must be greater than zero."

        if self.unitPrice.value() <= 0:

            return False, "Enter a valid unit price."

        return True, ""

    # --------------------------------------------------------
    # String Representation
    # --------------------------------------------------------

    def __str__(self):

        return (
            f"{self.garment.currentText()} "
            f"x {self.quantity.value()}"
        )