from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame,
    QLineEdit,
    QTextEdit,
    QListWidget,
    QFileDialog
)

import qtawesome as qta


class SettingPage(QWidget):

    def __init__(self):
        super().__init__()

        self.build_ui()

    # ------------------------------------------------------

    def build_ui(self):

        root = QHBoxLayout(self)

        root.setContentsMargins(25,25,25,25)

        root.setSpacing(20)

        # ==================================================
        # LEFT MENU
        # ==================================================

        left = QFrame()

        left.setObjectName("Card")

        left.setFixedWidth(220)

        leftLayout = QVBoxLayout(left)

        leftLayout.setContentsMargins(16, 16, 16, 16)

        title = QLabel("Settings")

        title.setObjectName("CardTitle")

        leftLayout.addWidget(title)

        self.menu = QListWidget()

        self.menu.addItems([

            "🏠 General",

            "🏢 Shop Details",

            "🧾 Invoice",

            "💬 WhatsApp",

            "💾 Backup",

            "📏 Measurements",

            "🎨 Appearance",

            "ℹ About"

        ])

        leftLayout.addWidget(self.menu)

        root.addWidget(left)

        # ==================================================
        # RIGHT CONTENT
        # ==================================================

        right = QWidget()

        rightLayout = QVBoxLayout(right)

        heading = QLabel("Shop Information")

        heading.setObjectName("PageTitle")

        rightLayout.addWidget(heading)

        card = QFrame()

        card.setObjectName("Card")

        grid = QGridLayout(card)

        grid.setContentsMargins(24, 24, 24, 24)

        grid.setSpacing(14)

        # ----------------------------------------

        self.shopName = QLineEdit()

        self.owner = QLineEdit()

        self.mobile = QLineEdit()

        self.email = QLineEdit()

        self.address = QTextEdit()

        self.address.setFixedHeight(90)

        # ----------------------------------------

        grid.addWidget(QLabel("Shop Name"),0,0)

        grid.addWidget(self.shopName,0,1)

        grid.addWidget(QLabel("Owner Name"),1,0)

        grid.addWidget(self.owner,1,1)

        grid.addWidget(QLabel("Mobile"),2,0)

        grid.addWidget(self.mobile,2,1)

        grid.addWidget(QLabel("Email"),3,0)

        grid.addWidget(self.email,3,1)

        grid.addWidget(QLabel("Address"),4,0)

        grid.addWidget(self.address,4,1)

        # ----------------------------------------
        # Logo
        # ----------------------------------------

        upload = QPushButton(" Upload Logo")

        upload.setIcon(
            qta.icon(
                "fa5s.image",
                color="white"
            )
        )

        upload.setObjectName("Primary")

        upload.clicked.connect(self.upload_logo)

        grid.addWidget(QLabel("Shop Logo"),5,0)

        grid.addWidget(upload,5,1)

        rightLayout.addWidget(card)

        rightLayout.addStretch()

        # ----------------------------------------
        # SAVE
        # ----------------------------------------

        bottom = QHBoxLayout()

        bottom.addStretch()

        save = QPushButton(" Save Settings")

        save.setObjectName("Primary")

        save.setIcon(
            qta.icon(
                "fa5s.save",
                color="white"
            )
        )

        bottom.addWidget(save)

        rightLayout.addLayout(bottom)

        root.addWidget(right,1)

    # ------------------------------------------------------

    def upload_logo(self):

        QFileDialog.getOpenFileName(
            self,
            "Select Logo",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )