from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
)


class OrderActionButtons(QWidget):

    viewClicked = Signal(dict)
    editClicked = Signal(dict)
    deleteClicked = Signal(dict)

    def __init__(self, order, parent=None):
        super().__init__(parent)

        self.setObjectName("TableActions")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.order = order

        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(5)

        # ======================================================
        # VIEW
        # ======================================================

        view_btn = QPushButton("View")
        view_btn.setCursor(Qt.PointingHandCursor)

        view_btn.clicked.connect(
            lambda checked=False, item=order:
                self.viewClicked.emit(item)
        )

        # ======================================================
        # EDIT
        # ======================================================

        edit_btn = QPushButton("Edit")
        edit_btn.setCursor(Qt.PointingHandCursor)

        edit_btn.clicked.connect(
            lambda checked=False, item=order:
                self.editClicked.emit(item)
        )

        # ======================================================
        # DELETE
        # ======================================================

        delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("IconDanger")
        delete_btn.setCursor(Qt.PointingHandCursor)

        delete_btn.clicked.connect(
            lambda checked=False, item=order:
                self.deleteClicked.emit(item)
        )

        layout.addWidget(view_btn)
        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)


class OrderTable(QWidget):

    # ==========================================================
    # SIGNALS
    # ==========================================================

    viewClicked = Signal(dict)
    editClicked = Signal(dict)
    deleteClicked = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.orders = []

        self.build_ui()

    # ==========================================================
    # UI
    # ==========================================================

    def build_ui(self):

        self.setObjectName("Card")
        self.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(0)

        # ======================================================
        # TABLE
        # ======================================================

        self.table = QTableWidget()

        self.table.setColumnCount(10)

        self.table.setHorizontalHeaderLabels([
            "Order",
            "Customer",
            "Garments",
            "Qty",
            "Delivery",
            "Payment",
            "Progress",
            "Status",
            "Tailor",
            "Actions",
        ])

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        self.table.setAlternatingRowColors(True)

        self.table.verticalHeader().setVisible(False)

        # ======================================================
        # HEADER
        # ======================================================

        header = self.table.horizontalHeader()

        header.setStretchLastSection(False)

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            4,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            5,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            6,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            7,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            8,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            9,
            QHeaderView.ResizeToContents
        )

        layout.addWidget(self.table)

    # ==========================================================
    # SET DATA
    # ==========================================================

    def set_data(self, orders):

        self.orders = orders or []

        self.table.setRowCount(0)

        for row_index, order in enumerate(self.orders):

            self.table.insertRow(row_index)

            # --------------------------------------------------
            # ORDER NUMBER
            # --------------------------------------------------

            order_number = order.get(
                "order_number",
                "—"
            )

            self.set_item(
                row_index,
                0,
                order_number
            )

            # --------------------------------------------------
            # CUSTOMER
            # --------------------------------------------------

            customer_name = order.get(
                "customer_name",
                "—"
            )

            mobile = order.get(
                "mobile",
                ""
            )

            customer_text = customer_name

            if mobile:
                customer_text += f"\n{mobile}"

            self.set_item(
                row_index,
                1,
                customer_text
            )

            # --------------------------------------------------
            # GARMENTS
            # --------------------------------------------------

            garments = order.get(
                "garments",
                "—"
            )

            self.set_item(
                row_index,
                2,
                str(garments)
            )

            # --------------------------------------------------
            # QUANTITY
            # --------------------------------------------------

            quantity = order.get(
                "quantity",
                0
            )

            self.set_item(
                row_index,
                3,
                str(quantity)
            )

            # --------------------------------------------------
            # DELIVERY
            # --------------------------------------------------

            delivery_date = order.get(
                "delivery_date",
                "—"
            )

            self.set_item(
                row_index,
                4,
                delivery_date
            )

            # --------------------------------------------------
            # PAYMENT
            # --------------------------------------------------

            payment_status = order.get(
                "payment_status",
                "Pending"
            )

            payment_item = self.create_status_item(
                payment_status,
                "payment"
            )

            self.table.setItem(
                row_index,
                5,
                payment_item
            )

            # --------------------------------------------------
            # PROGRESS
            # --------------------------------------------------

            progress = order.get(
                "progress",
                0
            )

            progress_text = f"{progress}%"

            self.set_item(
                row_index,
                6,
                progress_text
            )

            # --------------------------------------------------
            # STATUS
            # --------------------------------------------------

            status = order.get(
                "status",
                "pending"
            )

            status_text = str(status).replace(
                "_",
                " "
            ).title()

            status_item = self.create_status_item(
                status_text,
                "status"
            )

            self.table.setItem(
                row_index,
                7,
                status_item
            )

            # --------------------------------------------------
            # TAILOR
            # --------------------------------------------------

            tailor_name = order.get(
                "tailor_name",
                "—"
            )

            self.set_item(
                row_index,
                8,
                tailor_name
            )

            # --------------------------------------------------
            # ACTIONS
            # --------------------------------------------------

            actions = OrderActionButtons(
                order
            )

            actions.viewClicked.connect(
                self.viewClicked.emit
            )

            actions.editClicked.connect(
                self.editClicked.emit
            )

            actions.deleteClicked.connect(
                self.deleteClicked.emit
            )

            self.table.setCellWidget(
                row_index,
                9,
                actions
            )

            self.table.setRowHeight(
                row_index,
                58
            )

        # ======================================================
        # EMPTY STATE
        # ======================================================

        if not self.orders:

            self.table.insertRow(0)

            empty_item = QTableWidgetItem(
                "No orders found"
            )

            empty_item.setTextAlignment(
                Qt.AlignCenter
            )

            self.table.setItem(
                0,
                0,
                empty_item
            )

            self.table.setSpan(
                0,
                0,
                1,
                10
            )

            self.table.setRowHeight(
                0,
                80
            )

    # ==========================================================
    # SET ITEM
    # ==========================================================

    def set_item(
        self,
        row,
        column,
        value
    ):

        item = QTableWidgetItem(
            str(value)
        )

        item.setTextAlignment(
            Qt.AlignVCenter | Qt.AlignLeft
        )

        self.table.setItem(
            row,
            column,
            item
        )

    # ==========================================================
    # STATUS ITEM
    # ==========================================================

    def create_status_item(
        self,
        text,
        status_type
    ):

        item = QTableWidgetItem(
            str(text)
        )

        item.setTextAlignment(
            Qt.AlignCenter
        )

        item.setData(
            Qt.UserRole,
            status_type
        )

        return item

    # ==========================================================
    # CLEAR
    # ==========================================================

    def clear(self):

        self.orders = []

        self.table.setRowCount(0)

    # ==========================================================
    # GET SELECTED ORDER
    # ==========================================================

    def get_selected_order(self):

        row = self.table.currentRow()

        if row < 0:
            return None

        if row >= len(self.orders):
            return None

        return self.orders[row]