from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
)

from data.customer_crud import CUSTOMER_TYPES, GENDERS, normalize_type


class BasicInformation(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("Card")

        layout = QGridLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(18)

        # Title
        title = QLabel("Basic Information")
        title.setObjectName("CardTitle")
        layout.addWidget(title, 0, 0, 1, 4)

        # Only digits can be typed into the mobile fields
        digits = QRegularExpressionValidator(QRegularExpression(r"\d{0,10}"), self)

        # Name & Mobile
        layout.addWidget(self._label("Customer Name *"), 1, 0)
        self.name = QLineEdit()
        self.name.setPlaceholderText("Enter customer name")
        self.name.setMaxLength(100)
        layout.addWidget(self.name, 1, 1)

        layout.addWidget(self._label("Mobile Number *"), 1, 2)
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("10 digits, e.g. 9876543210")
        self.mobile.setMaxLength(10)
        self.mobile.setValidator(digits)
        layout.addWidget(self.mobile, 1, 3)

        # Alt Mobile & Email
        layout.addWidget(self._label("Alternate Mobile"), 2, 0)
        self.alt_mobile = QLineEdit()
        self.alt_mobile.setPlaceholderText("Optional")
        self.alt_mobile.setMaxLength(10)
        self.alt_mobile.setValidator(digits)
        layout.addWidget(self.alt_mobile, 2, 1)

        layout.addWidget(self._label("Email"), 2, 2)
        self.email = QLineEdit()
        self.email.setPlaceholderText("Optional, e.g. name@email.com")
        self.email.setMaxLength(100)
        layout.addWidget(self.email, 2, 3)

        # Gender & Type
        layout.addWidget(self._label("Gender"), 3, 0)
        self.gender = QComboBox()
        self.gender.addItems(GENDERS)
        layout.addWidget(self.gender, 3, 1)

        layout.addWidget(self._label("Customer Type"), 3, 2)
        self.customer_type = QComboBox()
        self.customer_type.addItems(CUSTOMER_TYPES)
        layout.addWidget(self.customer_type, 3, 3)

        # Reference & Status
        layout.addWidget(self._label("Reference By"), 4, 0)
        self.reference = QLineEdit()
        self.reference.setPlaceholderText("Friend / Social Media / Walk-in")
        self.reference.setMaxLength(50)
        layout.addWidget(self.reference, 4, 1)

        layout.addWidget(self._label("Status"), 4, 2)
        self.status = QComboBox()
        self.status.addItems(["Active", "Inactive"])
        self.status.setToolTip("Inactive customers are hidden from new orders and measurements")
        layout.addWidget(self.status, 4, 3)

        # Address
        layout.addWidget(self._label("Address"), 5, 0)
        self.address = QTextEdit()
        self.address.setPlaceholderText("Enter customer address...")
        self.address.setFixedHeight(100)
        layout.addWidget(self.address, 6, 0, 1, 4)

    def _label(self, text):
        label = QLabel(text)
        label.setObjectName("FieldLabel")
        return label

    def get_data(self):
        return {
            "name": self.name.text().strip(),
            "mobile": self.mobile.text().strip(),
            "alternate_mobile": self.alt_mobile.text().strip(),
            "email": self.email.text().strip(),
            "gender": self.gender.currentText(),
            "customer_type": self.customer_type.currentText(),
            "reference": self.reference.text().strip(),
            "address": self.address.toPlainText().strip(),
            "is_active": self.status.currentText() == "Active",
        }

    def clear_form(self):
        self.name.clear()
        self.mobile.clear()
        self.alt_mobile.clear()
        self.email.clear()
        self.reference.clear()
        self.address.clear()
        self.gender.setCurrentIndex(0)
        self.customer_type.setCurrentIndex(0)
        self.status.setCurrentIndex(0)

    def set_data(self, data):
        self.name.setText(data.get("name", ""))
        self.mobile.setText(data.get("mobile", ""))
        self.alt_mobile.setText(data.get("alternate_mobile", ""))
        self.email.setText(data.get("email", ""))
        self.reference.setText(data.get("reference", ""))
        self.address.setPlainText(data.get("address", ""))
        self.gender.setCurrentText(data.get("gender") or "Male")
        self.customer_type.setCurrentText(normalize_type(data.get("customer_type")))
        self.status.setCurrentText("Active" if data.get("is_active", True) else "Inactive")
        self.name.setFocus()
