from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
    QHBoxLayout,
    QWidget
)
from PySide6.QtCore import Qt, Signal
import qtawesome as qta
from typing import List
from data.customer_data import CustomerRowData

class CustomerTable(QFrame):
    editCustomerRequested = Signal(int)
    deleteCustomerRequested = Signal(int)

    def __init__(self):
        super().__init__()
        self.build_ui()

    def build_ui(self):
        self.setObjectName("CustomerTable")
        self.setStyleSheet("""
        QFrame#CustomerTable{
            background:#1F2937;
            border:1px solid #374151;
            border-radius:15px;
        }
        QTableWidget{
            background:transparent;
            color:white;
            border:none;
            gridline-color:#374151;
            alternate-background-color:#111827;
            selection-background-color:#3B82F6;
        }
        QHeaderView::section{
            background:#111827;
            color:white;
            border:none;
            padding:12px;
            font-weight:bold;
        }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Name", "Mobile", "Orders", "Pending", "Last Visit", "Status", "Measurements", "Action"
        ])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().hide()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        layout.addWidget(self.table)

    def load_data(self, customers: List[CustomerRowData]):
        self.table.setRowCount(len(customers))
        
        for row, c in enumerate(customers):
            # ID
            item_id = QTableWidgetItem(str(c.id))
            item_id.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, item_id)

            # Name
            item_name = QTableWidgetItem(c.name)
            item_name.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row, 1, item_name)

            # Mobile
            item_mobile = QTableWidgetItem(c.mobile)
            item_mobile.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, item_mobile)

            # Orders Count
            item_orders = QTableWidgetItem(str(c.orders_count))
            item_orders.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, item_orders)

            # Pending Amount
            item_pending = QTableWidgetItem(f"₹{c.pending_amount:,.2f}")
            item_pending.setTextAlignment(Qt.AlignCenter)
            if c.pending_amount > 0:
                item_pending.setForeground(Qt.GlobalColor.red)
            self.table.setItem(row, 4, item_pending)

            # Last Visit
            item_visit = QTableWidgetItem(c.last_visit)
            item_visit.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 5, item_visit)

            # Status
            item_status = QTableWidgetItem(c.status)
            item_status.setTextAlignment(Qt.AlignCenter)
            if c.status.lower() == "active":
                item_status.setForeground(Qt.GlobalColor.green)
            else:
                item_status.setForeground(Qt.GlobalColor.gray)
            self.table.setItem(row, 6, item_status)

            # Measurements
            item_m = QTableWidgetItem("Yes" if c.has_measurements else "No")
            item_m.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 7, item_m)

            # Action Buttons Widget (Edit / Delete)
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(4, 2, 4, 2)
            action_layout.setSpacing(6)
            action_layout.setAlignment(Qt.AlignCenter)

            edit_btn = QPushButton()
            edit_btn.setIcon(qta.icon("fa5s.edit", color="#3B82F6"))
            edit_btn.setToolTip("Edit Customer")
            edit_btn.setCursor(Qt.PointingHandCursor)
            edit_btn.setStyleSheet("background: transparent; border: none;")
            edit_btn.clicked.connect(lambda _, cid=c.id: self.editCustomerRequested.emit(cid))

            del_btn = QPushButton()
            del_btn.setIcon(qta.icon("fa5s.trash-alt", color="#EF4444"))
            del_btn.setToolTip("Delete Customer")
            del_btn.setCursor(Qt.PointingHandCursor)
            del_btn.setStyleSheet("background: transparent; border: none;")
            del_btn.clicked.connect(lambda _, cid=c.id: self.deleteCustomerRequested.emit(cid))

            action_layout.addWidget(edit_btn)
            action_layout.addWidget(del_btn)

            self.table.setCellWidget(row, 8, action_widget)