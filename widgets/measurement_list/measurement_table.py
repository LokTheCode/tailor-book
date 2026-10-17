from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QPushButton,
    QWidget,
    QHBoxLayout,
)

from utils.table import fit_column, fit_to_contents, setup_table
from PySide6.QtCore import (
    Qt,
    Signal,
)

import qtawesome as qta


class MeasurementTable(QFrame):

    editClicked = Signal(dict)
    deleteClicked = Signal(dict)

    def __init__(self):

        super().__init__()

        self.current_data = []

        self.build_ui()

    # ======================================================
    # UI
    # ======================================================

    def build_ui(self):

        self.setObjectName(
            "Card"
        )


        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            15,
            15,
            15,
            15,
        )

        self.table = QTableWidget()

        self.table.setColumnCount(8)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Customer",
            "Mobile",
            "Measurement",
            "Garment",
            "Values",
            "Updated",
            "Actions",
        ])

        # Shared look: 10 rows of space, full-height rows (utils/table.py)
        setup_table(self.table)
        fit_column(self.table, 0, 80)
        fit_column(self.table, 7, 120)
        fit_to_contents(self.table, 6)

        # Double-click a row to edit it
        self.table.doubleClicked.connect(
            lambda index: self.editClicked.emit(self.current_data[index.row()])
        )

        layout.addWidget(
            self.table
        )

    # ======================================================
    # LOAD DATA
    # ======================================================

    def set_data(self, data):

        self.current_data = data or []

        self.table.setRowCount(
            len(self.current_data)
        )

        for row, item in enumerate(
            self.current_data
        ):

            self._set_item(
                row,
                0,
                f"M{item['id']:04d}",
            )

            self._set_item(
                row,
                1,
                item.get(
                    "customer_name",
                    "",
                ),
            )

            self._set_item(
                row,
                2,
                item.get(
                    "mobile",
                    "",
                ),
            )

            self._set_item(
                row,
                3,
                item.get(
                    "measurement_name",
                    "",
                ),
            )

            self._set_item(
                row,
                4,
                item.get("garment") or "-",
            )

            # How many values were filled in each section
            counts = []
            for label, key in (
                ("Upper", "upper_measurements"),
                ("Lower", "lower_measurements"),
                ("Extra", "extra_measurements"),
            ):
                filled = len(item.get(key) or {})
                if filled:
                    counts.append(f"{label} {filled}")

            self._set_item(
                row,
                5,
                " · ".join(counts) or "-",
            )

            updated = item.get("updated_at")

            updated_text = (
                updated.strftime("%d %b %Y, %I:%M %p")
                if updated
                else "-"
            )

            self._set_item(
                row,
                6,
                updated_text,
            )

            # ------------------------------------------------
            # ACTIONS
            # ------------------------------------------------

            action_widget = QWidget()

            action_widget.setObjectName("TableActions")
            action_widget.setAttribute(Qt.WA_StyledBackground, True)

            action_layout = QHBoxLayout(
                action_widget
            )

            action_layout.setContentsMargins(
                0,
                0,
                0,
                0,
            )

            action_layout.setSpacing(5)

            edit_btn = QPushButton()

            edit_btn.setIcon(
                qta.icon(
                    "fa5s.edit",
                    color="white",
                )
            )

            edit_btn.clicked.connect(
                lambda checked=False,
                data=item:
                self.editClicked.emit(data)
            )

            delete_btn = QPushButton()

            delete_btn.setObjectName("IconDanger")

            delete_btn.setIcon(
                qta.icon(
                    "fa5s.trash",
                    color="white",
                )
            )

            delete_btn.clicked.connect(
                lambda checked=False,
                data=item:
                self.deleteClicked.emit(data)
            )

            action_layout.addWidget(
                edit_btn
            )

            action_layout.addWidget(
                delete_btn
            )

            self.table.setCellWidget(
                row,
                7,
                action_widget,
            )

    # ======================================================
    # EMPTY
    # ======================================================

    def clear(self):

        self.current_data = []

        self.table.setRowCount(0)

    # ======================================================
    # ITEM
    # ======================================================

    def _set_item(
        self,
        row,
        column,
        value,
    ):

        item = QTableWidgetItem(
            str(value)
        )

        item.setTextAlignment(
            Qt.AlignCenter
        )

        self.table.setItem(
            row,
            column,
            item,
        )