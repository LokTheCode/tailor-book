from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox
)

from PySide6.QtCore import Signal

import qtawesome as qta
from utils.theme import theme_color


class OrderPagination(QFrame):

    pageChanged = Signal(int)
    pageSizeChanged = Signal(int)

    def __init__(self):
        super().__init__()

        self.current_page = 1
        self.total_pages = 1

        self.build_ui()

    # ----------------------------------------------------

    def build_ui(self):

        self.setObjectName("Pagination")


        layout = QHBoxLayout(self)

        layout.setContentsMargins(15,12,15,12)

        layout.setSpacing(10)

        # ----------------------------

        self.info = QLabel(
            "Showing 0 - 0 of 0 Orders"
        )

        layout.addWidget(self.info)

        layout.addStretch()

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

        layout.addWidget(self.page_size)

        # ----------------------------

        self.first = QPushButton()

        self.first.setIcon(
            qta.icon(
                "fa5s.angle-double-left",
                color=theme_color("text")
            )
        )

        self.first.clicked.connect(
            lambda: self.goto_page(1)
        )

        layout.addWidget(self.first)

        # ----------------------------

        self.previous = QPushButton()

        self.previous.setIcon(
            qta.icon(
                "fa5s.angle-left",
                color=theme_color("text")
            )
        )

        self.previous.clicked.connect(
            self.previous_page
        )

        layout.addWidget(self.previous)

        # ----------------------------

        self.page_label = QLabel(
            "Page 1 / 1"
        )

        layout.addWidget(self.page_label)

        # ----------------------------

        self.next = QPushButton()

        self.next.setIcon(
            qta.icon(
                "fa5s.angle-right",
                color=theme_color("text")
            )
        )

        self.next.clicked.connect(
            self.next_page
        )

        layout.addWidget(self.next)

        # ----------------------------

        self.last = QPushButton()

        self.last.setIcon(
            qta.icon(
                "fa5s.angle-double-right",
                color=theme_color("text")
            )
        )

        self.last.clicked.connect(
            lambda: self.goto_page(
                self.total_pages
            )
        )

        layout.addWidget(self.last)

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
            f"Showing {start} - {end} of {total_records} Orders"
        )

        self.page_label.setText(
            f"Page {self.current_page} / {self.total_pages}"
        )

        self.update_buttons()

    # ----------------------------------------------------

    def update_buttons(self):

        self.first.setEnabled(
            self.current_page > 1
        )

        self.previous.setEnabled(
            self.current_page > 1
        )

        self.next.setEnabled(
            self.current_page < self.total_pages
        )

        self.last.setEnabled(
            self.current_page < self.total_pages
        )

    # ----------------------------------------------------

    def goto_page(self, page):

        if page < 1 or page > self.total_pages:
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