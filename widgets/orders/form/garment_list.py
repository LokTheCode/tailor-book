from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QWidget
)

from PySide6.QtCore import Signal

import qtawesome as qta

from widgets.orders.form.garment_card import GarmentCard


class GarmentList(QFrame):

    garmentAdded = Signal()

    garmentRemoved = Signal()

    def __init__(self):
        super().__init__()

        self.cards = []

        self.build_ui()

    # ----------------------------------------------------

    def build_ui(self):

        self.setObjectName("GarmentList")

        self.setStyleSheet("""

        QFrame#GarmentList{

            background:#1F2937;

            border:1px solid #374151;

            border-radius:15px;

        }

        QLabel#Title{

            color:white;

            font-size:18px;

            font-weight:bold;

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

        root.setSpacing(15)

        # -----------------------------------------
        # Header
        # -----------------------------------------

        top = QHBoxLayout()

        title = QLabel("Garments")

        title.setObjectName("Title")

        top.addWidget(title)

        top.addStretch()

        self.addBtn = QPushButton(" Add Garment")

        self.addBtn.setIcon(
            qta.icon(
                "fa5s.plus",
                color="white"
            )
        )

        self.addBtn.clicked.connect(
            self.add_garment
        )

        top.addWidget(self.addBtn)

        root.addLayout(top)

        # -----------------------------------------
        # Scroll Area
        # -----------------------------------------

        scroll = QScrollArea()

        scroll.setWidgetResizable(True)

        scroll.setMinimumHeight(350)

        scroll.setStyleSheet("""

        QScrollArea{

            border:none;

            background:transparent;

        }

        """)

        self.container = QWidget()

        self.layout = QVBoxLayout(self.container)

        self.layout.setSpacing(15)

        self.layout.setContentsMargins(0,0,0,0)

        scroll.setWidget(self.container)

        root.addWidget(scroll)

        # First Card

        self.add_garment()

    # ----------------------------------------------------

    def add_garment(self):

        card = GarmentCard()

        card.removeClicked.connect(
            lambda: self.remove_garment(card)
        )

        self.cards.append(card)

        self.layout.addWidget(card)

        self.garmentAdded.emit()

    # ----------------------------------------------------

    def remove_garment(self, card):

        if len(self.cards) == 1:
            return

        self.cards.remove(card)

        self.layout.removeWidget(card)

        card.deleteLater()

        self.garmentRemoved.emit()