from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton
)

from PySide6.QtCore import Signal

import qtawesome as qta


class NotesCard(QFrame):

    notesChanged = Signal()

    def __init__(self):
        super().__init__()

        self.build_ui()

    # ---------------------------------------------------------

    def build_ui(self):

        self.setObjectName("Card")


        root = QVBoxLayout(self)

        root.setContentsMargins(20,20,20,20)

        root.setSpacing(15)

        # =====================================================
        # Header
        # =====================================================

        header = QHBoxLayout()

        title = QLabel("Order Notes")

        title.setObjectName("CardTitle")

        header.addWidget(title)

        header.addStretch()

        icon = QLabel()

        icon.setPixmap(

            qta.icon(
                "fa5s.sticky-note",
                color="#F59E0B"
            ).pixmap(22,22)

        )

        header.addWidget(icon)

        root.addLayout(header)

        # =====================================================
        # Notes
        # =====================================================

        self.notes = QTextEdit()

        self.notes.setPlaceholderText(

            "Write anything about this order...\n\n"

            "Examples:\n"

            "• Customer requested slim fit.\n"

            "• Trial after 5 PM.\n"

            "• Deliver before festival.\n"

            "• Match previous fitting.\n"

            "• Use premium buttons."

        )

        self.notes.setMinimumHeight(180)

        root.addWidget(self.notes)

        # =====================================================
        # Quick Notes
        # =====================================================

        quick = QHBoxLayout()

        self.btnUrgent = QPushButton("Urgent")
        self.btnUrgent.setObjectName("ChipButton")

        self.btnTrial = QPushButton("Trial Required")
        self.btnTrial.setObjectName("ChipButton")

        self.btnExpress = QPushButton("Express")
        self.btnExpress.setObjectName("ChipButton")

        self.btnDelivery = QPushButton("Home Delivery")
        self.btnDelivery.setObjectName("ChipButton")

        quick.addWidget(self.btnUrgent)

        quick.addWidget(self.btnTrial)

        quick.addWidget(self.btnExpress)

        quick.addWidget(self.btnDelivery)

        quick.addStretch()

        root.addLayout(quick)

        # =====================================================
        # Signals
        # =====================================================

        self.notes.textChanged.connect(
            self.notesChanged.emit
        )

        self.btnUrgent.clicked.connect(
            lambda: self.append_note(
                "Urgent Order"
            )
        )

        self.btnTrial.clicked.connect(
            lambda: self.append_note(
                "Trial Required"
            )
        )

        self.btnExpress.clicked.connect(
            lambda: self.append_note(
                "Express Delivery"
            )
        )

        self.btnDelivery.clicked.connect(
            lambda: self.append_note(
                "Home Delivery"
            )
        )

    # ---------------------------------------------------------

    def append_note(self, text):

        current = self.notes.toPlainText().strip()

        if current:

            current += "\n"

        current += f"• {text}"

        self.notes.setPlainText(current)

        cursor = self.notes.textCursor()

        cursor.movePosition(cursor.End)

        self.notes.setTextCursor(cursor)

    # ---------------------------------------------------------

    def get_data(self):

        return {

            "notes": self.notes.toPlainText()

        }

    # ---------------------------------------------------------

    def set_data(self, data):

        self.notes.setPlainText(

            data.get("notes", "")

        )

    # ---------------------------------------------------------

    def clear_form(self):

        self.notes.clear()

    # ---------------------------------------------------------

    def validate(self):

        return True, ""

    # ---------------------------------------------------------

    def __str__(self):

        return self.notes.toPlainText()