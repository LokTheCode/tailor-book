from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

class RecentOrderTable(QFrame):
    def __init__(self):
        super().__init__()
        self.build_ui()

    def build_ui(self):
        self.setMinimumHeight(360)
        self.setStyleSheet("""
        QFrame { background:#1B2333; border-radius:18px; }
        QLabel { color:white; font-size:18px; font-weight:bold; }
        QTableWidget {
            background:transparent; color:white; border:none;
            gridline-color:#2D3748; font-size:13px;
            selection-background-color:#374151; alternate-background-color:#20293D;
        }
        QHeaderView::section {
            background:#111827; color:white; border:none; padding:10px; font-weight:bold;
        }
        """)
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(15)

        title = QLabel("Recent Orders")
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