from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

class RecentOrderTable(QFrame):
    def __init__(self):
        super().__init__()
        self.build_ui()

    def build_ui(self):
        self.setMinimumHeight(360)
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(15)

        self.setObjectName("Card")

        title = QLabel("Recent Orders")
        title.setObjectName("CardTitle")
        root.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Order", "Customer", "Dress", "Delivery", "Status", "Amount"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().hide()
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setShowGrid(False)
        self.table.setMinimumHeight(270)
        root.addWidget(self.table)

    def update_data(self, orders_data):
        self.table.setRowCount(len(orders_data))
        status_colors = {
            "Ready": "#22C55E",
            "Pending": "#EF4444",
            "Cutting": "#3B82F6",
            "Stitching": "#F59E0B"
        }

        for row, values in enumerate(orders_data):
            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)

                if col == 4:
                    color = status_colors.get(value, "#8B5CF6")
                    item.setForeground(QColor(color))
                    item.setFont(QFont("Segoe UI", 10, QFont.Bold))

                self.table.setItem(row, col, item)