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
            "MeasurementTable"
        )

        self.setStyleSheet("""
        
        QFrame#MeasurementTable {

            background:#1F2937;

            border:1px solid #374151;

            border-radius:16px;

        }

        QTableWidget {

            background:#1F2937;

            color:white;

            border:none;

            gridline-color:#374151;

            alternate-background-color:#111827;

            selection-background-color:#2563EB;

            font-size:13px;

        }

        QHeaderView::section {

            background:#111827;

            color:white;

            border:none;

            padding:12px;

            font-weight:bold;

        }

        QPushButton {

            background:#263244;

            color:white;

            border:1px solid #374151;

            border-radius:7px;

            min-width:32px;

            min-height:30px;

        }

        QPushButton:hover {

            background:#2563EB;

            border-color:#3B82F6;

        }

        """)

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

            "Upper",

            "Lower",

            "Updated",

            "Actions",

        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.verticalHeader().hide()

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.setSortingEnabled(
            False
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

            upper = item.get(
                "upper_measurements",
                {},
            )

            lower = item.get(
                "lower_measurements",
                {},
            )

            self._set_item(
                row,
                4,
                f"{len(upper)} fields",
            )

            self._set_item(
                row,
                5,
                f"{len(lower)} fields",
            )

            updated = item.get(
                "updated_at"
            )

            if updated:

                updated_text = (
                    updated.strftime(
                        "%d %b %Y"
                    )
                )

            else:

                updated_text = "-"

            self._set_item(
                row,
                6,
                updated_text,
            )

            # ------------------------------------------------
            # ACTIONS
            # ------------------------------------------------

            action_widget = QWidget()

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