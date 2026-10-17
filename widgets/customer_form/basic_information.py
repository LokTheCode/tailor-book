from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
)


class BasicInformation(QFrame):

    def __init__(self):
        super().__init__()
        self.build_ui()

    def build_ui(self):
        self.setObjectName("Card")

        layout = QGridLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(18)

        # Title
        title = QLabel("Basic Information")
        title.setObjectName("CardTitle")
        layout.addWidget(title, 0, 0, 1, 4)

        # Name & Mobile
        layout.addWidget(QLabel("Customer Name *"), 1, 0)
        self.name = QLineEdit()
        self.name.setPlaceholderText("Enter customer name")
        layout.addWidget(self.name, 1, 1)

        layout.addWidget(QLabel("Mobile Number *"), 1, 2)
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("9876543210")
        self.mobile.setMaxLength(10)
        layout.addWidget(self.mobile, 1, 3)

        # Alt Mobile & Email
        layout.addWidget(QLabel("Alternate Mobile"), 2, 0)
        self.alt_mobile = QLineEdit()
        self.alt_mobile.setPlaceholderText("Optional")
        self.alt_mobile.setMaxLength(10)
        layout.addWidget(self.alt_mobile, 2, 1)

        layout.addWidget(QLabel("Email"), 2, 2)
        self.email = QLineEdit()
        self.email.setPlaceholderText("example@email.com")
        layout.addWidget(self.email, 2, 3)

        # Gender & Type
        layout.addWidget(QLabel("Gender"), 3, 0)
        self.gender = QComboBox()
        self.gender.addItems(["Male", "Female", "Other"])
        layout.addWidget(self.gender, 3, 1)

        layout.addWidget(QLabel("Customer Type"), 3, 2)
        self.customer_type = QComboBox()
        self.customer_type.addItems(["Regular", "VIP", "Wholesale", "Corporate"])
        layout.addWidget(self.customer_type, 3, 3)

        # Reference
        layout.addWidget(QLabel("Reference By"), 4, 0)
        self.reference = QLineEdit()
        self.reference.setPlaceholderText("Friend / Social Media / Walk-in")
        layout.addWidget(self.reference, 4, 1, 1, 3)

        # Address
        layout.addWidget(QLabel("Address"), 5, 0)
        self.address = QTextEdit()
        self.address.setPlaceholderText("Enter customer address...")
        self.address.setFixedHeight(100)
        layout.addWidget(self.address, 6, 0, 1, 4)

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

    def set_data(self, data):
        self.name.setText(data.get("name", ""))
        self.mobile.setText(data.get("mobile", ""))
        self.alt_mobile.setText(data.get("alternate_mobile", ""))
        self.email.setText(data.get("email", ""))
        self.reference.setText(data.get("reference", ""))
        self.address.setPlainText(data.get("address", ""))
        self.gender.setCurrentText(data.get("gender", "Male"))
        self.customer_type.setCurrentText(data.get("customer_type", "Regular"))