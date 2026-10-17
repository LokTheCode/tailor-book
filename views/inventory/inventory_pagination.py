from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
)


class InventoryPagination(QFrame):

    pageChanged = Signal(int)
    pageSizeChanged = Signal(int)

    def __init__(self, parent=None):

        super().__init__(parent)

        self.current_page = 1
        self.total_pages = 1

        self.setObjectName("Pagination")

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            10, 8, 10, 8
        )

        self.info = QLabel(
            "Showing 0 items"
        )

        layout.addWidget(
            self.info
        )

        layout.addStretch()

        self.page_size = QComboBox()

        self.page_size.addItems([
            "10",
            "25",
            "50",
        ])

        self.page_size.currentTextChanged.connect(
            self.change_page_size
        )

        layout.addWidget(
            QLabel("Per page")
        )

        layout.addWidget(
            self.page_size
        )

        self.previous = QPushButton(
            "‹"
        )

        self.previous.clicked.connect(
            self.previous_page
        )

        self.next = QPushButton(
            "›"
        )

        self.next.clicked.connect(
            self.next_page
        )

        self.page_label = QLabel(
            "Page 1 / 1"
        )

        layout.addWidget(
            self.previous
        )

        layout.addWidget(
            self.page_label
        )

        layout.addWidget(
            self.next
        )

    def set_data(
        self,
        current_page,
        total_pages,
        total_records,
        page_size
    ):

        self.current_page = current_page
        self.total_pages = max(
            1,
            total_pages
        )

        self.info.setText(
            f"{total_records} items"
        )

        self.page_label.setText(
            f"Page {current_page} / "
            f"{self.total_pages}"
        )

        self.previous.setEnabled(
            current_page > 1
        )

        self.next.setEnabled(
            current_page < self.total_pages
        )

        index = self.page_size.findText(
            str(page_size)
        )

        if index >= 0:

            self.page_size.blockSignals(
                True
            )

            self.page_size.setCurrentIndex(
                index
            )

            self.page_size.blockSignals(
                False
            )

    def previous_page(self):

        if self.current_page > 1:

            self.pageChanged.emit(
                self.current_page - 1
            )

    def next_page(self):

        if self.current_page < self.total_pages:

            self.pageChanged.emit(
                self.current_page + 1
            )

    def change_page_size(self):

        self.pageSizeChanged.emit(
            int(
                self.page_size.currentText()
            )
        )