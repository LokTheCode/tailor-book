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

        self.setObjectName("Card")


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

        root.addWidget(self.previewBtn)

        self.invoiceBtn = QPushButton(
            qta.icon(
                "fa5s.file-invoice",
                color="white"
            ),
            " Invoice"
        )

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