from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton
)

from PySide6.QtCore import Qt, Signal

import qtawesome as qta


class MeasurementActionButtons(QWidget):

    viewClicked = Signal()
    editClicked = Signal()
    compareClicked = Signal()
    duplicateClicked = Signal()
    printClicked = Signal()
    deleteClicked = Signal()

    def __init__(self):
        super().__init__()

        self.build_ui()

    # ----------------------------------------------------

    def build_ui(self):

        self.setObjectName("TableActions")
        self.setAttribute(Qt.WA_StyledBackground, True)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0,0,0,0)

        layout.setSpacing(6)

        # ---------------------------------------------
        # View
        # ---------------------------------------------

        self.viewBtn = QPushButton()

        self.viewBtn.setToolTip(
            "View Measurement"
        )

        self.viewBtn.setIcon(
            qta.icon(
                "fa5s.eye",
                color="#60A5FA"
            )
        )

        self.viewBtn.clicked.connect(
            self.viewClicked.emit
        )

        layout.addWidget(self.viewBtn)

        # ---------------------------------------------
        # Edit
        # ---------------------------------------------

        self.editBtn = QPushButton()

        self.editBtn.setToolTip(
            "Edit Measurement"
        )

        self.editBtn.setIcon(
            qta.icon(
                "fa5s.edit",
                color="#34D399"
            )
        )

        self.editBtn.clicked.connect(
            self.editClicked.emit
        )

        layout.addWidget(self.editBtn)

        # ---------------------------------------------
        # Duplicate
        # ---------------------------------------------

        self.duplicateBtn = QPushButton()

        self.duplicateBtn.setToolTip(
            "Duplicate Measurement"
        )

        self.duplicateBtn.setIcon(
            qta.icon(
                "fa5s.copy",
                color="#FBBF24"
            )
        )

        self.duplicateBtn.clicked.connect(
            self.duplicateClicked.emit
        )

        layout.addWidget(self.duplicateBtn)

        # ---------------------------------------------
        # Compare
        # ---------------------------------------------

        self.compareBtn = QPushButton()

        self.compareBtn.setToolTip(
            "Compare Versions"
        )

        self.compareBtn.setIcon(
            qta.icon(
                "fa5s.balance-scale",
                color="#A78BFA"
            )
        )

        self.compareBtn.clicked.connect(
            self.compareClicked.emit
        )

        layout.addWidget(self.compareBtn)

        # ---------------------------------------------
        # Print
        # ---------------------------------------------

        self.printBtn = QPushButton()

        self.printBtn.setToolTip(
            "Print Measurement"
        )

        self.printBtn.setIcon(
            qta.icon(
                "fa5s.print",
                color="#22D3EE"
            )
        )

        self.printBtn.clicked.connect(
            self.printClicked.emit
        )

        layout.addWidget(self.printBtn)

        # ---------------------------------------------
        # Delete
        # ---------------------------------------------

        self.deleteBtn = QPushButton()

        self.deleteBtn.setObjectName("IconDanger")

        self.deleteBtn.setToolTip(
            "Delete Measurement"
        )

        self.deleteBtn.setIcon(
            qta.icon(
                "fa5s.trash",
                color="#F87171"
            )
        )

        self.deleteBtn.clicked.connect(
            self.deleteClicked.emit
        )

        layout.addWidget(self.deleteBtn)