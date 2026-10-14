from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton
)

from PySide6.QtCore import Signal

import qtawesome as qta


class OrderActionButtons(QWidget):

    viewClicked = Signal()
    editClicked = Signal()
    invoiceClicked = Signal()
    printClicked = Signal()
    paymentClicked = Signal()
    timelineClicked = Signal()
    deleteClicked = Signal()

    def __init__(self):
        super().__init__()

        self.build_ui()

    # ----------------------------------------------------

    def build_ui(self):

        self.setStyleSheet("""

        QPushButton{

            background:#111827;

            border:1px solid #374151;

            border-radius:8px;

            min-width:34px;
            max-width:34px;

            min-height:34px;
            max-height:34px;

        }

        QPushButton:hover{

            background:#2563EB;

            border:1px solid #3B82F6;

        }

        """)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0,0,0,0)

        layout.setSpacing(5)

        # --------------------------------------------
        # View
        # --------------------------------------------

        self.viewBtn = QPushButton()

        self.viewBtn.setToolTip("View Order")

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

        # --------------------------------------------
        # Edit
        # --------------------------------------------

        self.editBtn = QPushButton()

        self.editBtn.setToolTip("Edit Order")

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

        # --------------------------------------------
        # Invoice
        # --------------------------------------------

        self.invoiceBtn = QPushButton()

        self.invoiceBtn.setToolTip("Invoice")

        self.invoiceBtn.setIcon(
            qta.icon(
                "fa5s.file-invoice",
                color="#FBBF24"
            )
        )

        self.invoiceBtn.clicked.connect(
            self.invoiceClicked.emit
        )

        layout.addWidget(self.invoiceBtn)

        # --------------------------------------------
        # Payment
        # --------------------------------------------

        self.paymentBtn = QPushButton()

        self.paymentBtn.setToolTip("Receive Payment")

        self.paymentBtn.setIcon(
            qta.icon(
                "fa5s.wallet",
                color="#10B981"
            )
        )

        self.paymentBtn.clicked.connect(
            self.paymentClicked.emit
        )

        layout.addWidget(self.paymentBtn)

        # --------------------------------------------
        # Timeline
        # --------------------------------------------

        self.timelineBtn = QPushButton()

        self.timelineBtn.setToolTip("Production Timeline")

        self.timelineBtn.setIcon(
            qta.icon(
                "fa5s.stream",
                color="#A78BFA"
            )
        )

        self.timelineBtn.clicked.connect(
            self.timelineClicked.emit
        )

        layout.addWidget(self.timelineBtn)

        # --------------------------------------------
        # Print
        # --------------------------------------------

        self.printBtn = QPushButton()

        self.printBtn.setToolTip("Print Order")

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

        # --------------------------------------------
        # Delete
        # --------------------------------------------

        self.deleteBtn = QPushButton()

        self.deleteBtn.setToolTip("Delete Order")

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