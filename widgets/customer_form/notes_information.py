from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QTextEdit,
    QGridLayout
)


class NotesInformation(QFrame):

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

        # --------------------------------------------

        title = QLabel("Customer Notes")

        title.setObjectName("CardTitle")

        layout.addWidget(title,0,0,1,2)

        # --------------------------------------------

        layout.addWidget(
            QLabel("Special Stitching Instructions"),
            1,
            0
        )

        self.stitching_notes = QTextEdit()

        self.stitching_notes.setPlaceholderText(
            "Example:\n• Slim Fit\n• Double Stitch\n• Hidden Pocket\n• Loose Collar"
        )

        layout.addWidget(
            self.stitching_notes,
            2,
            0
        )

        # --------------------------------------------

        layout.addWidget(
            QLabel("Internal Staff Notes"),
            1,
            1
        )

        self.staff_notes = QTextEdit()

        self.staff_notes.setPlaceholderText(
            "Visible only to staff..."
        )

        layout.addWidget(
            self.staff_notes,
            2,
            1
        )

        # --------------------------------------------

        layout.addWidget(
            QLabel("Delivery Instructions"),
            3,
            0
        )

        self.delivery_notes = QTextEdit()

        self.delivery_notes.setPlaceholderText(
            "Delivery preferences..."
        )

        layout.addWidget(
            self.delivery_notes,
            4,
            0
        )

        # --------------------------------------------

        layout.addWidget(
            QLabel("Additional Remarks"),
            3,
            1
        )

        self.remarks = QTextEdit()

        self.remarks.setPlaceholderText(
            "Other important information..."
        )

        layout.addWidget(
            self.remarks,
            4,
            1
        )

    # ----------------------------------------------------

    def get_data(self):

        return {

            "stitching_notes":
                self.stitching_notes.toPlainText(),

            "staff_notes":
                self.staff_notes.toPlainText(),

            "delivery_notes":
                self.delivery_notes.toPlainText(),

            "remarks":
                self.remarks.toPlainText()

        }

    # ----------------------------------------------------

    def clear_form(self):

        self.stitching_notes.clear()

        self.staff_notes.clear()

        self.delivery_notes.clear()

        self.remarks.clear()

    # ----------------------------------------------------

    def set_data(self,data):

        self.stitching_notes.setPlainText(
            data.get(
                "stitching_notes",
                ""
            )
        )

        self.staff_notes.setPlainText(
            data.get(
                "staff_notes",
                ""
            )
        )

        self.delivery_notes.setPlainText(
            data.get(
                "delivery_notes",
                ""
            )
        )

        self.remarks.setPlainText(
            data.get(
                "remarks",
                ""
            )
        )