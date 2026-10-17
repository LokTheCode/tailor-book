from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QGridLayout,
    QVBoxLayout,
)
from PySide6.QtCore import Qt


class DynamicMeasurementSection(QFrame):

    def __init__(
        self,
        title: str,
        fields: list,
        parent=None,
    ):
        super().__init__(parent)

        self.fields = {}
        self.field_config = fields

        self.setObjectName("Card")

        self.setup_ui(title)

    # ======================================================
    # UI
    # ======================================================

    def setup_ui(self, title):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        layout.setSpacing(16)

        # --------------------------------------------------
        # TITLE
        # --------------------------------------------------

        title_label = QLabel(title)

        title_label.setObjectName(
            "CardTitle"
        )

        layout.addWidget(title_label)

        # --------------------------------------------------
        # GRID
        # --------------------------------------------------

        grid = QGridLayout()

        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(14)

        for index, (label, key) in enumerate(
            self.field_config
        ):

            row = index // 3
            column = index % 3

            field_container = QVBoxLayout()

            field_label = QLabel(label)

            field_label.setObjectName(
                "FieldLabel"
            )

            field = QLineEdit()

            field.setPlaceholderText(
                f"Enter {label}"
            )

            field_container.addWidget(
                field_label
            )

            field_container.addWidget(
                field
            )

            container = QFrame()

            container.setLayout(
                field_container
            )

            grid.addWidget(
                container,
                row,
                column,
            )

            self.fields[key] = field

        layout.addLayout(grid)

    # ======================================================
    # GET DATA
    # ======================================================

    def get_data(self) -> dict:

        data = {}

        for key, field in self.fields.items():

            value = field.text().strip()

            data[key] = value

        return data

    # ======================================================
    # SET DATA
    # ======================================================

    def set_data(self, data: dict | None):

        data = data or {}

        for key, field in self.fields.items():

            value = data.get(key, "")

            if value is None:
                value = ""

            field.setText(str(value))

    # ======================================================
    # CLEAR
    # ======================================================

    def clear(self):

        for field in self.fields.values():

            field.clear()