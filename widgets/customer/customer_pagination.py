from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QSizePolicy
)

from PySide6.QtCore import Qt, Signal

import qtawesome as qta


class CustomerPagination(QFrame):

    pageChanged = Signal(int)
    pageSizeChanged = Signal(int)

    def __init__(self):
        super().__init__()

        self.current_page = 1
        self.total_pages = 1

        self.build_ui()

    # ----------------------------------------------------

    def build_ui(self):

        self.setObjectName("CustomerPagination")

        self.setStyleSheet("""

        QFrame#CustomerPagination{

            background:#1F2937;

            border:1px solid #374151;

            border-radius:15px;

        }

        QLabel{

            background:Transparent;

            color:white;

            font-size:13px;

        }

        QPushButton{

            background:Transparent;

            color:white;

            border:1px solid #374151;

            border-radius:8px;

            min-width:36px;

            min-height:36px;

            font-weight:600;

        }

        QPushButton:hover{

            background:#2563EB;

            border:1px solid #3B82F6;

        }

        QPushButton:disabled{

            background:#0F172A;

            color:#6B7280;

            border:1px solid #374151;

        }

        QComboBox{

            background:Transparent;

            color:white;

            border:1px solid #374151;

            border-radius:8px;

            padding:6px;

            min-width:60px;

            min-height:24px;

        }

        """)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(15,12,15,12)

        layout.setSpacing(10)

        # ------------------------------------------------

        self.info = QLabel(
            "Showing 1 - 10 of 0 Customers"
        )

        layout.addWidget(self.info)

        layout.addStretch()

        # ------------------------------------------------

        layout.addWidget(
            QLabel("Rows")
        )

        self.page_size = QComboBox()

        self.page_size.addItems([
            "10",
            "25",
            "50",
            "100"
        ])

        self.page_size.currentTextChanged.connect(
            self.change_page_size
        )

        layout.addWidget(
            self.page_size
        )

        # ------------------------------------------------

        self.first_btn = QPushButton()

        self.first_btn.setIcon(
            qta.icon(
                "fa5s.angle-double-left",
                color="white"
            )
        )

        self.first_btn.clicked.connect(
            lambda: self.goto_page(1)
        )

        layout.addWidget(
            self.first_btn
        )

        # ------------------------------------------------

        self.prev_btn = QPushButton()

        self.prev_btn.setIcon(
            qta.icon(
                "fa5s.angle-left",
                color="white"
            )
        )

        self.prev_btn.clicked.connect(
            self.previous_page
        )

        layout.addWidget(
            self.prev_btn
        )

        # ------------------------------------------------

        self.page_label = QLabel(
            "Page 1 / 1"
        )

        self.page_label.setAlignment(
            Qt.AlignCenter
        )

        self.page_label.setMinimumWidth(
            100
        )

        layout.addWidget(
            self.page_label
        )

        # ------------------------------------------------

        self.next_btn = QPushButton()

        self.next_btn.setIcon(
            qta.icon(
                "fa5s.angle-right",
                color="white"
            )
        )

        self.next_btn.clicked.connect(
            self.next_page
        )

        layout.addWidget(
            self.next_btn
        )

        # ------------------------------------------------

        self.last_btn = QPushButton()

        self.last_btn.setIcon(
            qta.icon(
                "fa5s.angle-double-right",
                color="white"
            )
        )

        self.last_btn.clicked.connect(
            lambda: self.goto_page(
                self.total_pages
            )
        )

        layout.addWidget(
            self.last_btn
        )

        self.update_buttons()

    # ----------------------------------------------------

    def set_pagination(
        self,
        current,
        total,
        total_records
    ):

        self.current_page = max(1, current)

        self.total_pages = max(1, total)

        page_size = int(
            self.page_size.currentText()
        )

        start = (self.current_page - 1) * page_size + 1

        end = min(
            self.current_page * page_size,
            total_records
        )

        if total_records == 0:

            start = 0

            end = 0

        self.info.setText(

            f"Showing {start} - {end} of {total_records} Customers"

        )

        self.page_label.setText(

            f"Page {self.current_page} / {self.total_pages}"

        )

        self.update_buttons()

    # ----------------------------------------------------

    def update_buttons(self):

        self.first_btn.setEnabled(
            self.current_page > 1
        )

        self.prev_btn.setEnabled(
            self.current_page > 1
        )

        self.next_btn.setEnabled(
            self.current_page < self.total_pages
        )

        self.last_btn.setEnabled(
            self.current_page < self.total_pages
        )

    # ----------------------------------------------------

    def goto_page(self, page):

        if page < 1:

            return

        if page > self.total_pages:

            return

        self.current_page = page

        self.pageChanged.emit(page)

        self.update_buttons()

    # ----------------------------------------------------

    def next_page(self):

        self.goto_page(
            self.current_page + 1
        )

    # ----------------------------------------------------

    def previous_page(self):

        self.goto_page(
            self.current_page - 1
        )

    # ----------------------------------------------------

    def change_page_size(self):

        self.pageSizeChanged.emit(

            int(
                self.page_size.currentText()
            )

        )