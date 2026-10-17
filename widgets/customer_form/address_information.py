from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QTextEdit,
    QGridLayout,
    QComboBox
)


class AddressInformation(QFrame):

    def __init__(self):
        super().__init__()

        self.build_ui()

    # ----------------------------------------------------

    def build_ui(self):

        self.setObjectName("Card")


        layout = QGridLayout(self)

        layout.setContentsMargins(25,25,25,25)

        layout.setHorizontalSpacing(20)

        layout.setVerticalSpacing(18)

        # ----------------------------------------------------

        title = QLabel("Address Information")

        title.setObjectName("CardTitle")

        layout.addWidget(title,0,0,1,4)

        # ----------------------------------------------------
        # Address
        # ----------------------------------------------------

        layout.addWidget(QLabel("House / Flat No."),1,0)

        self.house_no = QLineEdit()

        self.house_no.setPlaceholderText(
            "House / Flat Number"
        )

        layout.addWidget(self.house_no,1,1)

        layout.addWidget(QLabel("Building / Society"),1,2)

        self.building = QLineEdit()

        self.building.setPlaceholderText(
            "Building / Society"
        )

        layout.addWidget(self.building,1,3)

        # ----------------------------------------------------

        layout.addWidget(QLabel("Street"),2,0)

        self.street = QLineEdit()

        self.street.setPlaceholderText(
            "Street Name"
        )

        layout.addWidget(self.street,2,1)

        layout.addWidget(QLabel("Area / Locality"),2,2)

        self.area = QLineEdit()

        self.area.setPlaceholderText(
            "Area"
        )

        layout.addWidget(self.area,2,3)

        # ----------------------------------------------------

        layout.addWidget(QLabel("Landmark"),3,0)

        self.landmark = QLineEdit()

        self.landmark.setPlaceholderText(
            "Nearby Landmark"
        )

        layout.addWidget(self.landmark,3,1)

        layout.addWidget(QLabel("Pincode"),3,2)

        self.pincode = QLineEdit()

        self.pincode.setPlaceholderText(
            "Pincode"
        )

        layout.addWidget(self.pincode,3,3)

        # ----------------------------------------------------

        layout.addWidget(QLabel("City"),4,0)

        self.city = QLineEdit()

        self.city.setPlaceholderText(
            "City"
        )

        layout.addWidget(self.city,4,1)

        layout.addWidget(QLabel("State"),4,2)

        self.state = QComboBox()

        self.state.addItems([

            "Select State",

            "Andhra Pradesh",

            "Arunachal Pradesh",

            "Assam",

            "Bihar",

            "Chhattisgarh",

            "Delhi",

            "Goa",

            "Gujarat",

            "Haryana",

            "Himachal Pradesh",

            "Jharkhand",

            "Karnataka",

            "Kerala",

            "Madhya Pradesh",

            "Maharashtra",

            "Odisha",

            "Punjab",

            "Rajasthan",

            "Tamil Nadu",

            "Telangana",

            "Uttar Pradesh",

            "Uttarakhand",

            "West Bengal"

        ])

        layout.addWidget(self.state,4,3)

        # ----------------------------------------------------

        layout.addWidget(QLabel("Country"),5,0)

        self.country = QComboBox()

        self.country.addItems([
            "India"
        ])

        layout.addWidget(self.country,5,1)

        # ----------------------------------------------------

        layout.addWidget(QLabel("Complete Address"),6,0)

        self.full_address = QTextEdit()

        self.full_address.setPlaceholderText(
            "Complete Address..."
        )

        layout.addWidget(
            self.full_address,
            7,
            0,
            1,
            4
        )

    # ----------------------------------------------------

    def get_data(self):

        return {

            "house_no": self.house_no.text(),

            "building": self.building.text(),

            "street": self.street.text(),

            "area": self.area.text(),

            "landmark": self.landmark.text(),

            "pincode": self.pincode.text(),

            "city": self.city.text(),

            "state": self.state.currentText(),

            "country": self.country.currentText(),

            "address": self.full_address.toPlainText()

        }

    # ----------------------------------------------------

    def clear_form(self):

        self.house_no.clear()

        self.building.clear()

        self.street.clear()

        self.area.clear()

        self.landmark.clear()

        self.pincode.clear()

        self.city.clear()

        self.full_address.clear()

        self.state.setCurrentIndex(0)

        self.country.setCurrentIndex(0)

    # ----------------------------------------------------

    def set_data(self, data):

        self.house_no.setText(
            data.get("house_no","")
        )

        self.building.setText(
            data.get("building","")
        )

        self.street.setText(
            data.get("street","")
        )

        self.area.setText(
            data.get("area","")
        )

        self.landmark.setText(
            data.get("landmark","")
        )

        self.pincode.setText(
            data.get("pincode","")
        )

        self.city.setText(
            data.get("city","")
        )

        self.full_address.setPlainText(
            data.get("address","")
        )

        state = data.get("state","")

        if state:
            self.state.setCurrentText(state)

        country = data.get("country","India")

        self.country.setCurrentText(country)