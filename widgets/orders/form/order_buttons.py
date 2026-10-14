from PySide6.QtWidgets import (
    QFrame,
    QPushButton,
    QHBoxLayout,
    QMessageBox
)

from PySide6.QtCore import Signal

import qtawesome as qta


class OrderButtons(QFrame):

    saveClicked = Signal()
    savePrintClicked = Signal()
    previewClicked = Signal()
    invoiceClicked = Signal()
    resetClicked = Signal()
    cancelClicked = Signal()

    # -----------------------------------------------------

    def __init__(self):
        super().__init__()

        self.build_ui()

    # -----------------------------------------------------

    def build_ui(self):

        self.setObjectName("OrderButtons")

        self.setStyleSheet("""

        QFrame#OrderButtons{

            background:#1F2937;

            border:1px solid #374151;

            border-radius:15px;

        }

        QPushButton{

            color:white;

            border:none;

            border-radius:8px;

            padding:12px 20px;

            font-size:13px;

            min-height:42px;

        }

        QPushButton#Primary{

            background:#2563EB;

        }

        QPushButton#Primary:hover{

            background:#1D4ED8;

        }

        QPushButton#Success{

            background:#10B981;

        }

        QPushButton#Success:hover{

            background:#059669;

        }

        QPushButton#Warning{

            background:#F59E0B;

        }

        QPushButton#Warning:hover{

            background:#D97706;

        }

        QPushButton#Danger{

            background:#DC2626;

        }

        QPushButton#Danger:hover{

            background:#B91C1C;

        }

        QPushButton#Gray{

            background:#4B5563;

        }

        QPushButton#Gray:hover{

            background:#374151;

        }

        """)

        root = QHBoxLayout(self)

        root.setContentsMargins(20,15,20,15)

        root.setSpacing(10)

        # =====================================================
        # Left Buttons
        # =====================================================

        self.previewBtn = QPushButton(
            qta.icon(
                "fa5s.eye",
                color="white"
            ),
            " Preview"
        )

        self.previewBtn.setObjectName("Gray")

        root.addWidget(self.previewBtn)

        self.invoiceBtn = QPushButton(
            qta.icon(
                "fa5s.file-invoice",
                color="white"
            ),
            " Invoice"
        )

        self.invoiceBtn.setObjectName("Gray")

        root.addWidget(self.invoiceBtn)

        root.addStretch()

        # =====================================================
        # Right Buttons
        # =====================================================

        self.resetBtn = QPushButton(
            qta.icon(
                "fa5s.undo",
                color="white"
            ),
            " Reset"
        )

        self.resetBtn.setObjectName("Warning")

        root.addWidget(self.resetBtn)

        self.cancelBtn = QPushButton(
            qta.icon(
                "fa5s.times",
                color="white"
            ),
            " Cancel"
        )

        self.cancelBtn.setObjectName("Danger")

        root.addWidget(self.cancelBtn)

        self.saveBtn = QPushButton(
            qta.icon(
                "fa5s.save",
                color="white"
            ),
            " Save Order"
        )

        self.saveBtn.setObjectName("Primary")

        root.addWidget(self.saveBtn)

        self.savePrintBtn = QPushButton(
            qta.icon(
                "fa5s.print",
                color="white"
            ),
            " Save & Print"
        )

        self.savePrintBtn.setObjectName("Success")

        root.addWidget(self.savePrintBtn)

        # =====================================================
        # Signals
        # =====================================================

        self.previewBtn.clicked.connect(
            self.previewClicked.emit
        )

        self.invoiceBtn.clicked.connect(
            self.invoiceClicked.emit
        )

        self.resetBtn.clicked.connect(
            self.on_reset
        )

        self.cancelBtn.clicked.connect(
            self.cancelClicked.emit
        )

        self.saveBtn.clicked.connect(
            self.saveClicked.emit
        )

        self.savePrintBtn.clicked.connect(
            self.savePrintClicked.emit
        )

    # -----------------------------------------------------

    def on_reset(self):

        reply = QMessageBox.question(

            self,

            "Reset Order",

            "Clear all order information?",

            QMessageBox.Yes |

            QMessageBox.No

        )

        if reply == QMessageBox.Yes:

            self.resetClicked.emit()

    # -----------------------------------------------------

    def enable_save(self, enabled=True):

        self.saveBtn.setEnabled(enabled)

        self.savePrintBtn.setEnabled(enabled)

    # -----------------------------------------------------

    def enable_print(self, enabled=True):

        self.invoiceBtn.setEnabled(enabled)

    # -----------------------------------------------------

    def set_edit_mode(self):

        self.saveBtn.setText(" Update Order")

        self.savePrintBtn.setText(" Update & Print")

    # -----------------------------------------------------

    def set_create_mode(self):

        self.saveBtn.setText(" Save Order")

        self.savePrintBtn.setText(" Save & Print")