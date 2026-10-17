from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton
)

from PySide6.QtCore import Signal

import qtawesome as qta


class MeasurementHeader(QFrame):

    addMeasurementClicked = Signal()

    def __init__(self):
        super().__init__()

        self.build_ui()

    # ----------------------------------------------------

    def build_ui(self):

        self.setObjectName("PageHeader")


        root = QHBoxLayout(self)
        
        root.setContentsMargins(0, 0, 0, 0)
        
        root.setSpacing(15)

        # ==========================================
        # Left
        # ==========================================
       
        left = QVBoxLayout()
       
        left.setSpacing(4)

        title = QLabel("Measurements")

        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Manage customer measurements, versions and garment sizes."
        )

        subtitle.setObjectName("PageSubtitle")

        left.addWidget(title)

        left.addWidget(subtitle)

        root.addLayout(left)

        root.addStretch()

        # ---------------------------------------------

        self.add_btn = QPushButton(" Add Measurement")

        self.add_btn.setObjectName("Primary")

        self.add_btn.setIcon(
            qta.icon(
                "fa5s.plus",
                color="white"
            )
        )

        self.add_btn.clicked.connect(
            self.addMeasurementClicked.emit
        )

        root.addWidget(self.add_btn)