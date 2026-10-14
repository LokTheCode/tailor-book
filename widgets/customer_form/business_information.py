from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QComboBox,
    QDoubleSpinBox,
    QGridLayout
)


class BusinessInformation(QFrame):

    def __init__(self):
        super().__init__()

        self.build_ui()

    # ----------------------------------------------------

    def build_ui(self):

        self.setObjectName("BusinessInformation")

        self.setStyleSheet("""

        QFrame#BusinessInformation{

            background:#1F2937;

            border:1px solid #374151;

            border-radius:18px;

        }

        QLabel#Title{

            color:white;

            font-size:18px;

            font-weight:bold;

        }

        QLabel{

            color:#E5E7EB;

            font-size:13px;

            font-weight:600;

        }

        QLineEdit,
        QComboBox,
        QDoubleSpinBox{

            background:#111827;

            color:white;

            border:1px solid #374151;

            border-radius:10px;

            padding:8px;

            min-height:42px;

        }

        QLineEdit:focus,
        QComboBox:focus,
        QDoubleSpinBox:focus{

            border:2px solid #3B82F6;

        }

        """)

        layout = QGridLayout(self)

        layout.setContentsMargins(25,25,25,25)

        layout.setHorizontalSpacing(20)

        layout.setVerticalSpacing(18)

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        title = QLabel("Business Information")

        title.setObjectName("Title")

        layout.addWidget(title,0,0,1,4)

        # ----------------------------------------------------
        # GST Number
        # ----------------------------------------------------

        layout.addWidget(QLabel("GST Number"),1,0)

        self.gst = QLineEdit()

        self.gst.setPlaceholderText(
            "22AAAAA0000A1Z5"
        )

        layout.addWidget(self.gst,1,1)

        # ----------------------------------------------------
        # PAN Number
        # ----------------------------------------------------

        layout.addWidget(QLabel("PAN Number"),1,2)

        self.pan = QLineEdit()

        self.pan.setPlaceholderText(
            "ABCDE1234F"
        )

        layout.addWidget(self.pan,1,3)

        # ----------------------------------------------------
        # Aadhaar
        # ----------------------------------------------------

        layout.addWidget(QLabel("Aadhaar Number"),2,0)

        self.aadhaar = QLineEdit()

        self.aadhaar.setPlaceholderText(
            "1234 5678 9012"
        )

        layout.addWidget(self.aadhaar,2,1)

        # ----------------------------------------------------
        # Occupation
        # ----------------------------------------------------

        layout.addWidget(QLabel("Occupation"),2,2)

        self.occupation = QLineEdit()

        self.occupation.setPlaceholderText(
            "Business / Job / Student"
        )

        layout.addWidget(self.occupation,2,3)

        # ----------------------------------------------------
        # Company Name
        # ----------------------------------------------------

        layout.addWidget(QLabel("Company Name"),3,0)

        self.company = QLineEdit()

        self.company.setPlaceholderText(
            "Optional"
        )

        layout.addWidget(self.company,3,1)

        # ----------------------------------------------------
        # Company GST
        # ----------------------------------------------------

        layout.addWidget(QLabel("Company GST"),3,2)

        self.company_gst = QLineEdit()

        self.company_gst.setPlaceholderText(
            "Optional"
        )

        layout.addWidget(self.company_gst,3,3)

        # ----------------------------------------------------
        # Customer Category
        # ----------------------------------------------------

        layout.addWidget(QLabel("Customer Category"),4,0)

        self.category = QComboBox()

        self.category.addItems([

            "Regular",

            "VIP",

            "Wholesale",

            "Retail",

            "Corporate"

        ])

        layout.addWidget(self.category,4,1)

        # ----------------------------------------------------
        # Referred By
        # ----------------------------------------------------

        layout.addWidget(QLabel("Referred By"),4,2)

        self.reference = QLineEdit()

        self.reference.setPlaceholderText(
            "Friend / Social Media / Existing Customer"
        )

        layout.addWidget(self.reference,4,3)

        # ----------------------------------------------------
        # Credit Limit
        # ----------------------------------------------------

        layout.addWidget(QLabel("Credit Limit"),5,0)

        self.credit_limit = QDoubleSpinBox()

        self.credit_limit.setMaximum(99999999)

        self.credit_limit.setPrefix("₹ ")

        self.credit_limit.setDecimals(2)

        layout.addWidget(self.credit_limit,5,1)

        # ----------------------------------------------------
        # Discount
        # ----------------------------------------------------

        layout.addWidget(QLabel("Default Discount (%)"),5,2)

        self.discount = QDoubleSpinBox()

        self.discount.setRange(0,100)

        self.discount.setSuffix(" %")

        self.discount.setDecimals(2)

        layout.addWidget(self.discount,5,3)

            # ----------------------------------------------------

    def get_data(self):

        return {

            "gst": self.gst.text(),

            "pan": self.pan.text(),

            "aadhaar": self.aadhaar.text(),

            "occupation": self.occupation.text(),

            "company": self.company.text(),

            "company_gst": self.company_gst.text(),

            "category": self.category.currentText(),

            "reference": self.reference.text(),

            "credit_limit": self.credit_limit.value(),

            "discount": self.discount.value(),

            "loyalty_points": self.loyalty_points.value(),

            "payment_mode": self.payment_mode.currentText(),

            "customer_since": self.customer_since.text(),

            "tax_exemption": self.tax_exemption.currentText(),

            "remarks": self.remarks.text()

        }

    # ----------------------------------------------------

    def clear_form(self):

        self.gst.clear()

        self.pan.clear()

        self.aadhaar.clear()

        self.occupation.clear()

        self.company.clear()

        self.company_gst.clear()

        self.reference.clear()

        self.customer_since.clear()

        self.remarks.clear()

        self.credit_limit.setValue(0)

        self.discount.setValue(0)

        self.loyalty_points.setValue(0)

        self.category.setCurrentIndex(0)

        self.payment_mode.setCurrentIndex(0)

        self.tax_exemption.setCurrentIndex(0)

    # ----------------------------------------------------

    def set_data(self, data):

        self.gst.setText(data.get("gst",""))

        self.pan.setText(data.get("pan",""))

        self.aadhaar.setText(data.get("aadhaar",""))

        self.occupation.setText(data.get("occupation",""))

        self.company.setText(data.get("company",""))

        self.company_gst.setText(data.get("company_gst",""))

        self.reference.setText(data.get("reference",""))

        self.customer_since.setText(
            data.get("customer_since","")
        )

        self.remarks.setText(
            data.get("remarks","")
        )

        self.credit_limit.setValue(
            float(data.get("credit_limit",0))
        )

        self.discount.setValue(
            float(data.get("discount",0))
        )

        self.loyalty_points.setValue(
            float(data.get("loyalty_points",0))
        )

        self.category.setCurrentText(
            data.get("category","Regular")
        )

        self.payment_mode.setCurrentText(
            data.get("payment_mode","Cash")
        )

        self.tax_exemption.setCurrentText(
            data.get("tax_exemption","No")
        )