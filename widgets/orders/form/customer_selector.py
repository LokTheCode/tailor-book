from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QGridLayout
)

import qtawesome as qta


class CustomerSelector(QFrame):

    def __init__(self):
        super().__init__()

        self.build_ui()

    # ----------------------------------------------------

    def build_ui(self):

        self.setObjectName("Card")


        root = QVBoxLayout(self)

        root.setContentsMargins(20,20,20,20)

        root.setSpacing(20)

        # -------------------------------------

        title = QLabel("Customer Information")

        title.setObjectName("CardTitle")

        root.addWidget(title)

        # -------------------------------------

        searchLayout = QHBoxLayout()

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Search customer by name or mobile..."
        )

        self.search.addAction(
            qta.icon(
                "fa5s.search",
                color="#9CA3AF"
            ),
            QLineEdit.LeadingPosition
        )

        searchLayout.addWidget(self.search)

        self.newCustomer = QPushButton("New Customer")

        self.newCustomer.setObjectName("Primary")

        self.newCustomer.setIcon(
            qta.icon(
                "fa5s.user-plus",
                color="white"
            )
        )

        searchLayout.addWidget(self.newCustomer)

        root.addLayout(searchLayout)

        # -------------------------------------

        info = QGridLayout()

        info.setHorizontalSpacing(25)

        info.setVerticalSpacing(12)

        info.addWidget(QLabel("Customer"),0,0)
        info.addWidget(QLabel(":"),0,1)

        self.customerName = QLabel("Not Selected")

        info.addWidget(self.customerName,0,2)

        info.addWidget(QLabel("Mobile"),1,0)
        info.addWidget(QLabel(":"),1,1)

        self.mobile = QLabel("-")

        info.addWidget(self.mobile,1,2)

        info.addWidget(QLabel("Address"),2,0)
        info.addWidget(QLabel(":"),2,1)

        self.address = QLabel("-")

        info.addWidget(self.address,2,2)

        info.addWidget(QLabel("Measurements"),0,3)
        info.addWidget(QLabel(":"),0,4)

        self.measurements = QLabel("0")

        info.addWidget(self.measurements,0,5)

        info.addWidget(QLabel("Previous Orders"),1,3)
        info.addWidget(QLabel(":"),1,4)

        self.orders = QLabel("0")

        info.addWidget(self.orders,1,5)

        info.addWidget(QLabel("Pending Amount"),2,3)
        info.addWidget(QLabel(":"),2,4)

        self.pending = QLabel("₹0")

        info.addWidget(self.pending,2,5)

        root.addLayout(info)