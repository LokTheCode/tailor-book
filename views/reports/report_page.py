import csv

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFileDialog,
    QMessageBox,
    QComboBox,
    QDateEdit,
)

from PySide6.QtCore import (
    Qt,
    QDate,
)

from data.report_data import (
    get_date_range,
    get_order_report,
    get_order_summary,
    get_customer_report,
    get_inventory_report,
    get_inventory_report_summary,
)


# ==========================================================
# REPORT STAT CARD
# ==========================================================

class ReportStatCard(QFrame):

    def __init__(
        self,
        title,
        value="0",
        description="",
        parent=None,
    ):

        super().__init__(parent)

        self.setObjectName(
            "StatCard"
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            18,
            16,
            18,
            16,
        )

        layout.setSpacing(
            5
        )

        self.title_label = QLabel(
            title
        )

        self.title_label.setObjectName(
            "StatTitle"
        )

        self.value_label = QLabel(
            value
        )

        self.value_label.setObjectName(
            "StatValue"
        )

        self.description_label = QLabel(
            description
        )

        self.description_label.setObjectName(
            "StatDescription"
        )

        layout.addWidget(
            self.title_label
        )

        layout.addWidget(
            self.value_label
        )

        layout.addWidget(
            self.description_label
        )

    # ======================================================
    # SET VALUE
    # ======================================================

    def set_value(
        self,
        value,
    ):

        self.value_label.setText(
            str(value)
        )


# ==========================================================
# REPORT PAGE
# ==========================================================

class ReportPage(QWidget):

    def __init__(
        self,
        parent=None,
    ):

        super().__init__(parent)

        self.orders = []

        self.report_customers = []

        self.inventory_transactions = []

        self.build_ui()

        self.load_report()

    # ==========================================================
    # UI
    # ==========================================================

    def build_ui(self):

        self.setObjectName(
            "ReportPage"
        )


        main_layout = QVBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        main_layout.setSpacing(
            0
        )

        # ======================================================
        # SCROLL AREA
        # ======================================================

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setFrameShape(
            QScrollArea.NoFrame
        )

        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        container = QWidget()

        root = QVBoxLayout(
            container
        )

        root.setContentsMargins(
            25,
            25,
            25,
            30,
        )

        root.setSpacing(
            20
        )

        # ======================================================
        # HEADER
        # ======================================================

        header = QFrame()

        header.setObjectName(
            "Card"
        )

        header_layout = QVBoxLayout(
            header
        )

        header_layout.setContentsMargins(
            20,
            18,
            20,
            18,
        )

        header_layout.setSpacing(
            14
        )

        # ------------------------------------------------------
        # TITLE ROW
        # ------------------------------------------------------

        title_row = QHBoxLayout()

        title_box = QVBoxLayout()

        title_box.setSpacing(
            3
        )

        title = QLabel(
            "Reports"
        )

        title.setObjectName(
            "PageTitle"
        )

        subtitle = QLabel(
            "Business performance, orders, customers and inventory overview"
        )

        subtitle.setObjectName(
            "PageSubtitle"
        )

        title_box.addWidget(
            title
        )

        title_box.addWidget(
            subtitle
        )

        title_row.addLayout(
            title_box
        )

        title_row.addStretch()

        header_layout.addLayout(
            title_row
        )

        # ------------------------------------------------------
        # FILTER ROW
        # ------------------------------------------------------

        filter_row = QHBoxLayout()

        filter_row.setSpacing(
            10
        )

        # ======================================================
        # REPORT TYPE
        # ======================================================

        report_type_box = QVBoxLayout()

        report_type_box.setSpacing(
            4
        )

        report_type_label = QLabel(
            "Report Type"
        )

        report_type_label.setObjectName(
            "FieldLabel"
        )

        self.report_type = QComboBox()

        self.report_type.addItems([
            "Overall Report",
            "Order Report",
            "Customer Report",
            "Inventory Report",
        ])

        self.report_type.setMinimumWidth(
            160
        )

        self.report_type.currentTextChanged.connect(
            self.on_report_type_changed
        )

        report_type_box.addWidget(
            report_type_label
        )

        report_type_box.addWidget(
            self.report_type
        )

        filter_row.addLayout(
            report_type_box
        )

        # ======================================================
        # DATE RANGE
        # ======================================================

        date_range_box = QVBoxLayout()

        date_range_box.setSpacing(
            4
        )

        date_range_label = QLabel(
            "Date Range"
        )

        date_range_label.setObjectName(
            "FieldLabel"
        )

        self.date_range = QComboBox()

        self.date_range.addItems([
            "Today",
            "This Week",
            "This Month",
            "This Year",
            "Custom Date",
        ])

        self.date_range.setCurrentText(
            "This Month"
        )

        self.date_range.setMinimumWidth(
            150
        )

        self.date_range.currentTextChanged.connect(
            self.on_date_range_changed
        )

        date_range_box.addWidget(
            date_range_label
        )

        date_range_box.addWidget(
            self.date_range
        )

        filter_row.addLayout(
            date_range_box
        )

        # ======================================================
        # START DATE
        # ======================================================

        self.start_date_box = QVBoxLayout()

        self.start_date_box.setSpacing(
            4
        )

        start_label = QLabel(
            "From"
        )

        start_label.setObjectName(
            "FieldLabel"
        )

        self.start_date_edit = QDateEdit()

        self.start_date_edit.setCalendarPopup(
            True
        )

        self.start_date_edit.setDisplayFormat(
            "dd/MM/yyyy"
        )

        self.start_date_edit.setDate(
            QDate.currentDate()
        )

        self.start_date_edit.setMinimumWidth(
            125
        )

        self.start_date_edit.dateChanged.connect(
            self.on_custom_date_changed
        )

        self.start_date_box.addWidget(
            start_label
        )

        self.start_date_box.addWidget(
            self.start_date_edit
        )

        filter_row.addLayout(
            self.start_date_box
        )

        # ======================================================
        # END DATE
        # ======================================================

        self.end_date_box = QVBoxLayout()

        self.end_date_box.setSpacing(
            4
        )

        end_label = QLabel(
            "To"
        )

        end_label.setObjectName(
            "FieldLabel"
        )

        self.end_date_edit = QDateEdit()

        self.end_date_edit.setCalendarPopup(
            True
        )

        self.end_date_edit.setDisplayFormat(
            "dd/MM/yyyy"
        )

        self.end_date_edit.setDate(
            QDate.currentDate()
        )

        self.end_date_edit.setMinimumWidth(
            125
        )

        self.end_date_edit.dateChanged.connect(
            self.on_custom_date_changed
        )

        self.end_date_box.addWidget(
            end_label
        )

        self.end_date_box.addWidget(
            self.end_date_edit
        )

        filter_row.addLayout(
            self.end_date_box
        )

        # Start/end hidden initially
        self.start_date_box_widget = QWidget()

        # We cannot hide a layout directly, therefore
        # the actual widgets are hidden below.
        self.start_date_edit.setVisible(
            False
        )

        start_label.setVisible(
            False
        )

        self.end_date_edit.setVisible(
            False
        )

        end_label.setVisible(
            False
        )

        filter_row.addStretch()

        # ======================================================
        # REFRESH
        # ======================================================

        refresh_button = QPushButton(
            "↻  Refresh"
        )

        refresh_button.setCursor(
            Qt.PointingHandCursor
        )

        refresh_button.clicked.connect(
            self.load_report
        )

        filter_row.addWidget(
            refresh_button
        )

        # ======================================================
        # DOWNLOAD
        # ======================================================

        download_button = QPushButton(
            "↓  Download CSV"
        )

        download_button.setObjectName(
            "Primary"
        )

        download_button.setCursor(
            Qt.PointingHandCursor
        )

        download_button.clicked.connect(
            self.export_report
        )

        filter_row.addWidget(
            download_button
        )

        header_layout.addLayout(
            filter_row
        )

        root.addWidget(
            header
        )

        # ======================================================
        # DATE RANGE LABEL
        # ======================================================

        self.selected_range_label = QLabel()

        self.selected_range_label.setObjectName("MutedText")


        root.addWidget(
            self.selected_range_label
        )

        # ======================================================
        # STATISTICS
        # ======================================================

        stats_layout = QHBoxLayout()

        stats_layout.setSpacing(
            12
        )

        self.total_orders = ReportStatCard(
            "Total Orders",
            "0",
            "Orders in selected period",
        )

        self.revenue = ReportStatCard(
            "Revenue",
            "₹0.00",
            "Total order value",
        )

        self.delivered = ReportStatCard(
            "Delivered",
            "0",
            "Completed deliveries",
        )

        self.pending = ReportStatCard(
            "Pending",
            "0",
            "Orders still in progress",
        )

        self.customers = ReportStatCard(
            "Customers",
            "0",
            "Active customers with orders",
        )

        self.inventory_value = ReportStatCard(
            "Inventory Value",
            "₹0.00",
            "Current inventory cost",
        )

        stats_layout.addWidget(
            self.total_orders,
            1
        )

        stats_layout.addWidget(
            self.revenue,
            1
        )

        stats_layout.addWidget(
            self.delivered,
            1
        )

        stats_layout.addWidget(
            self.pending,
            1
        )

        stats_layout.addWidget(
            self.customers,
            1
        )

        stats_layout.addWidget(
            self.inventory_value,
            1
        )

        root.addLayout(
            stats_layout
        )

        # ======================================================
        # ORDER STATUS
        # ======================================================

        self.status_card = self.create_report_card(
            "Order Status Summary",
            "Current distribution of orders by status",
        )

        status_layout = (
            self.status_card.layout()
        )

        self.status_table = QTableWidget()

        self.status_table.setColumnCount(
            2
        )

        self.status_table.setHorizontalHeaderLabels([
            "Status",
            "Orders",
        ])

        self.prepare_table(
            self.status_table
        )

        status_layout.addWidget(
            self.status_table
        )

        root.addWidget(
            self.status_card
        )

        # ======================================================
        # TOP CUSTOMERS
        # ======================================================

        self.customers_card = self.create_report_card(
            "Top Customers",
            "Customers ranked by order value in selected period",
        )

        customers_layout = (
            self.customers_card.layout()
        )

        self.customer_table = QTableWidget()

        self.customer_table.setColumnCount(
            4
        )

        self.customer_table.setHorizontalHeaderLabels([
            "Customer",
            "Orders",
            "Revenue",
            "Last Order",
        ])

        self.prepare_table(
            self.customer_table
        )

        customers_layout.addWidget(
            self.customer_table
        )

        root.addWidget(
            self.customers_card
        )

        # ======================================================
        # ORDERS
        # ======================================================

        self.orders_card = self.create_report_card(
            "Order Summary",
            "Highest-value orders in selected period",
        )

        orders_layout = (
            self.orders_card.layout()
        )

        self.order_table = QTableWidget()

        self.order_table.setColumnCount(
            5
        )

        self.order_table.setHorizontalHeaderLabels([
            "Order",
            "Customer",
            "Status",
            "Total",
            "Delivery Date",
        ])

        self.prepare_table(
            self.order_table
        )

        orders_layout.addWidget(
            self.order_table
        )

        root.addWidget(
            self.orders_card
        )

        # ======================================================
        # INVENTORY TRANSACTIONS
        # ======================================================

        self.inventory_card = self.create_report_card(
            "Inventory Transactions",
            "Stock movements in selected period",
        )

        inventory_layout = (
            self.inventory_card.layout()
        )

        self.inventory_table = QTableWidget()

        self.inventory_table.setColumnCount(
            6
        )

        self.inventory_table.setHorizontalHeaderLabels([
            "Item",
            "SKU",
            "Type",
            "Quantity",
            "Reference",
            "Date",
        ])

        self.prepare_table(
            self.inventory_table
        )

        inventory_layout.addWidget(
            self.inventory_table
        )

        root.addWidget(
            self.inventory_card
        )

        # ======================================================
        # SET SCROLL
        # ======================================================

        scroll.setWidget(
            container
        )

        main_layout.addWidget(
            scroll
        )

    # ==========================================================
    # CREATE REPORT CARD
    # ==========================================================

    def create_report_card(
        self,
        title,
        subtitle,
    ):

        card = QFrame()

        card.setObjectName(
            "Card"
        )

        layout = QVBoxLayout(
            card
        )

        layout.setContentsMargins(
            18,
            18,
            18,
            18,
        )

        layout.setSpacing(
            10
        )

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "CardTitle"
        )

        subtitle_label = QLabel(
            subtitle
        )

        subtitle_label.setObjectName(
            "CardSubtitle"
        )

        layout.addWidget(
            title_label
        )

        layout.addWidget(
            subtitle_label
        )

        return card

    # ==========================================================
    # PREPARE TABLE
    # ==========================================================

    def prepare_table(
        self,
        table,
    ):

        table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        table.setAlternatingRowColors(
            True
        )

        table.verticalHeader().setVisible(
            False
        )

        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        table.setMinimumHeight(
            180
        )

    # ==========================================================
    # GET SELECTED DATE RANGE
    # ==========================================================

    def get_selected_date_range(
        self,
    ):

        selected = (
            self.date_range.currentText()
        )

        mapping = {
            "Today": "today",
            "This Week": "week",
            "This Month": "month",
            "This Year": "year",
            "Custom Date": "custom",
        }

        period = mapping.get(
            selected,
            "month",
        )

        if period == "custom":

            start_date = (
                self.start_date_edit
                .date()
                .toPython()
            )

            end_date = (
                self.end_date_edit
                .date()
                .toPython()
            )

            return (
                period,
                start_date,
                end_date,
            )

        return (
            period,
            None,
            None,
        )

    # ==========================================================
    # DATE RANGE CHANGED
    # ==========================================================

    def on_date_range_changed(
        self,
        value,
    ):

        is_custom = (
            value == "Custom Date"
        )

        # Show/hide date widgets
        self.start_date_edit.setVisible(
            is_custom
        )

        self.end_date_edit.setVisible(
            is_custom
        )

        # Find labels in the parent layouts
        for i in range(
            self.start_date_box.count()
        ):

            widget = (
                self.start_date_box
                .itemAt(i)
                .widget()
            )

            if widget:
                widget.setVisible(
                    is_custom
                )

        for i in range(
            self.end_date_box.count()
        ):

            widget = (
                self.end_date_box
                .itemAt(i)
                .widget()
            )

            if widget:
                widget.setVisible(
                    is_custom
                )

        if not is_custom:

            self.load_report()

    # ==========================================================
    # CUSTOM DATE CHANGED
    # ==========================================================

    def on_custom_date_changed(
        self,
        _date,
    ):

        if (
            self.date_range.currentText()
            == "Custom Date"
        ):

            self.load_report()

    # ==========================================================
    # LOAD REPORT
    # ==========================================================

    def load_report(
        self,
    ):

        try:

            (
                period,
                start_date,
                end_date,
            ) = self.get_selected_date_range()

            # ==================================================
            # NORMALIZE DATE RANGE
            # ==================================================

            range_start, range_end = (
                get_date_range(
                    period,
                    start_date,
                    end_date,
                )
            )

            # ==================================================
            # UPDATE RANGE LABEL
            # ==================================================

            self.selected_range_label.setText(
                (
                    "Showing data from "
                    f"{range_start.strftime('%d/%m/%Y')}"
                    " to "
                    f"{range_end.strftime('%d/%m/%Y')}"
                )
            )

            # ==================================================
            # ORDER DATA
            # ==================================================

            order_data = get_order_report(
                period,
                start_date,
                end_date,
            )

            self.orders = (
                order_data.get(
                    "items",
                    [],
                )
                or []
            )

            # ==================================================
            # ORDER SUMMARY
            # ==================================================

            order_summary = (
                get_order_summary(
                    period,
                    start_date,
                    end_date,
                )
            )

            self.apply_order_stats(
                order_summary
            )

            # ==================================================
            # CUSTOMER DATA
            # ==================================================

            customer_data = (
                get_customer_report(
                    period,
                    start_date,
                    end_date,
                )
            )

            self.report_customers = (
                customer_data.get(
                    "items",
                    [],
                )
                or []
            )

            self.customers.set_value(
                len(
                    self.report_customers
                )
            )

            # ==================================================
            # INVENTORY DATA
            # ==================================================

            inventory_data = (
                get_inventory_report(
                    period,
                    start_date,
                    end_date,
                )
            )

            self.inventory_transactions = (
                inventory_data.get(
                    "items",
                    [],
                )
                or []
            )

            inventory_summary = (
                get_inventory_report_summary(
                    period,
                    start_date,
                    end_date,
                )
            )

            self.inventory_value.set_value(
                (
                    f"₹"
                    f"{inventory_summary.get('inventory_value', 0):,.2f}"
                )
            )

            # ==================================================
            # BUILD TABLES
            # ==================================================

            self.build_status_report()

            self.build_customer_report()

            self.build_order_report()

            self.build_inventory_report()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Report Error",
                (
                    "Unable to generate report:\n\n"
                    f"{e}"
                ),
            )

    # ==========================================================
    # APPLY ORDER STATS
    # ==========================================================

    def apply_order_stats(
        self,
        stats,
    ):

        if not stats:
            return

        total_orders = (
            stats.get(
                "total_orders",
                0,
            )
        )

        revenue = (
            stats.get(
                "revenue",
                0,
            )
        )

        delivered = (
            stats.get(
                "delivered",
                0,
            )
        )

        pending = (
            stats.get(
                "pending",
                0,
            )
        )

        self.total_orders.set_value(
            total_orders
        )

        self.revenue.set_value(
            f"₹{self.to_float(revenue):,.2f}"
        )

        self.delivered.set_value(
            delivered
        )

        self.pending.set_value(
            pending
        )

    # ==========================================================
    # STATUS REPORT
    # ==========================================================

    def build_status_report(
        self,
    ):

        status_map = {}

        for order in self.orders:

            status = (
                str(
                    order.get(
                        "status",
                        "Unknown",
                    )
                    or "Unknown"
                )
                .strip()
                .title()
            )

            status_map[status] = (
                status_map.get(
                    status,
                    0,
                )
                + 1
            )

        self.status_table.setRowCount(
            0
        )

        sorted_statuses = sorted(
            status_map.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        for row, (
            status,
            count,
        ) in enumerate(
            sorted_statuses
        ):

            self.status_table.insertRow(
                row
            )

            self.status_table.setItem(
                row,
                0,
                QTableWidgetItem(
                    status
                ),
            )

            self.status_table.setItem(
                row,
                1,
                QTableWidgetItem(
                    str(count)
                ),
            )

    # ==========================================================
    # CUSTOMER REPORT
    # ==========================================================

    def build_customer_report(
        self,
    ):

        self.customer_table.setRowCount(
            0
        )

        for row, customer in enumerate(
            self.report_customers[:10]
        ):

            self.customer_table.insertRow(
                row
            )

            self.customer_table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(
                        customer.get(
                            "customer_name",
                            "",
                        )
                    )
                ),
            )

            self.customer_table.setItem(
                row,
                1,
                QTableWidgetItem(
                    str(
                        customer.get(
                            "orders",
                            0,
                        )
                    )
                ),
            )

            revenue = self.to_float(
                customer.get(
                    "revenue",
                    0,
                )
            )

            self.customer_table.setItem(
                row,
                2,
                QTableWidgetItem(
                    f"₹{revenue:,.2f}"
                ),
            )

            self.customer_table.setItem(
                row,
                3,
                QTableWidgetItem(
                    str(
                        customer.get(
                            "last_order",
                            "",
                        )
                    )
                ),
            )

    # ==========================================================
    # ORDER REPORT
    # ==========================================================

    def build_order_report(
        self,
    ):

        sorted_orders = sorted(
            self.orders,
            key=lambda x: (
                self.to_float(
                    x.get(
                        "total_amount",
                        0,
                    )
                )
            ),
            reverse=True,
        )[:15]

        self.order_table.setRowCount(
            0
        )

        for row, order in enumerate(
            sorted_orders
        ):

            self.order_table.insertRow(
                row
            )

            self.order_table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(
                        order.get(
                            "order_number",
                            "",
                        )
                    )
                ),
            )

            self.order_table.setItem(
                row,
                1,
                QTableWidgetItem(
                    str(
                        order.get(
                            "customer_name",
                            "",
                        )
                    )
                ),
            )

            self.order_table.setItem(
                row,
                2,
                QTableWidgetItem(
                    str(
                        order.get(
                            "status",
                            "",
                        )
                    )
                ),
            )

            amount = self.to_float(
                order.get(
                    "total_amount",
                    0,
                )
            )

            self.order_table.setItem(
                row,
                3,
                QTableWidgetItem(
                    f"₹{amount:,.2f}"
                ),
            )

            self.order_table.setItem(
                row,
                4,
                QTableWidgetItem(
                    str(
                        order.get(
                            "delivery_date",
                            "",
                        )
                    )
                ),
            )

    # ==========================================================
    # INVENTORY REPORT
    # ==========================================================

    def build_inventory_report(
        self,
    ):

        self.inventory_table.setRowCount(
            0
        )

        for row, transaction in enumerate(
            self.inventory_transactions[:100]
        ):

            self.inventory_table.insertRow(
                row
            )

            self.inventory_table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(
                        transaction.get(
                            "item_name",
                            "",
                        )
                    )
                ),
            )

            self.inventory_table.setItem(
                row,
                1,
                QTableWidgetItem(
                    str(
                        transaction.get(
                            "sku",
                            "",
                        )
                    )
                ),
            )

            self.inventory_table.setItem(
                row,
                2,
                QTableWidgetItem(
                    str(
                        transaction.get(
                            "transaction_type",
                            "",
                        )
                    )
                ),
            )

            quantity = self.to_float(
                transaction.get(
                    "quantity",
                    0,
                )
            )

            self.inventory_table.setItem(
                row,
                3,
                QTableWidgetItem(
                    f"{quantity:g} "
                    f"{transaction.get('unit', '')}"
                )
            )

            reference = (
                transaction.get(
                    "reference_type",
                    "",
                )
                or ""
            )

            reference_id = (
                transaction.get(
                    "reference_id",
                    "",
                )
                or ""
            )

            if reference_id:

                reference = (
                    f"{reference} "
                    f"#{reference_id}"
                )

            self.inventory_table.setItem(
                row,
                4,
                QTableWidgetItem(
                    reference
                )
            )

            self.inventory_table.setItem(
                row,
                5,
                QTableWidgetItem(
                    str(
                        transaction.get(
                            "created_at",
                            "",
                        )
                    )
                ),
            )

    # ==========================================================
    # REPORT TYPE CHANGED
    # ==========================================================

    def on_report_type_changed(
        self,
        report_type,
    ):

        show_orders = (
            report_type
            in (
                "Overall Report",
                "Order Report",
            )
        )

        show_customers = (
            report_type
            in (
                "Overall Report",
                "Customer Report",
            )
        )

        show_inventory = (
            report_type
            in (
                "Overall Report",
                "Inventory Report",
            )
        )

        self.status_card.setVisible(
            show_orders
        )

        self.orders_card.setVisible(
            show_orders
        )

        self.customers_card.setVisible(
            show_customers
        )

        self.inventory_card.setVisible(
            show_inventory
        )

        # ======================================================
        # STAT CARDS
        # ======================================================

        self.total_orders.setVisible(
            show_orders
        )

        self.revenue.setVisible(
            show_orders
        )

        self.delivered.setVisible(
            show_orders
        )

        self.pending.setVisible(
            show_orders
        )

        self.customers.setVisible(
            show_customers
        )

        self.inventory_value.setVisible(
            show_inventory
        )

    # ==========================================================
    # EXPORT REPORT
    # ==========================================================

    def export_report(
        self,
    ):

        file_path, _ = (
            QFileDialog.getSaveFileName(
                self,
                "Download Report",
                "tailor_report.csv",
                "CSV Files (*.csv)",
            )
        )

        if not file_path:
            return

        try:

            (
                period,
                start_date,
                end_date,
            ) = self.get_selected_date_range()

            range_start, range_end = (
                get_date_range(
                    period,
                    start_date,
                    end_date,
                )
            )

            report_type = (
                self.report_type.currentText()
            )

            # ==================================================
            # ORDER
            # ==================================================

            if report_type == "Order Report":

                data = get_order_report(
                    period,
                    start_date,
                    end_date,
                )

                self.export_order_csv(
                    file_path,
                    data.get(
                        "items",
                        [],
                    ),
                    range_start,
                    range_end,
                )

            # ==================================================
            # CUSTOMER
            # ==================================================

            elif report_type == "Customer Report":

                data = get_customer_report(
                    period,
                    start_date,
                    end_date,
                )

                self.export_customer_csv(
                    file_path,
                    data.get(
                        "items",
                        [],
                    ),
                    range_start,
                    range_end,
                )

            # ==================================================
            # INVENTORY
            # ==================================================

            elif report_type == "Inventory Report":

                data = get_inventory_report(
                    period,
                    start_date,
                    end_date,
                )

                self.export_inventory_csv(
                    file_path,
                    data.get(
                        "items",
                        [],
                    ),
                    range_start,
                    range_end,
                )

            # ==================================================
            # OVERALL
            # ==================================================

            else:

                order_data = (
                    get_order_report(
                        period,
                        start_date,
                        end_date,
                    )
                )

                customer_data = (
                    get_customer_report(
                        period,
                        start_date,
                        end_date,
                    )
                )

                inventory_data = (
                    get_inventory_report(
                        period,
                        start_date,
                        end_date,
                    )
                )

                self.export_overall_csv(
                    file_path,
                    order_data.get(
                        "items",
                        [],
                    ),
                    customer_data.get(
                        "items",
                        [],
                    ),
                    inventory_data.get(
                        "items",
                        [],
                    ),
                    range_start,
                    range_end,
                )

            # ==================================================
            # SUCCESS
            # ==================================================

            QMessageBox.information(
                self,
                "Download Successful",
                (
                    "Report downloaded successfully.\n\n"
                    f"Report: {report_type}\n"
                    f"Period: "
                    f"{range_start.strftime('%d/%m/%Y')}"
                    " - "
                    f"{range_end.strftime('%d/%m/%Y')}"
                ),
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Download Error",
                str(e),
            )

    # ==========================================================
    # EXPORT ORDER CSV
    # ==========================================================

    def export_order_csv(
        self,
        file_path,
        orders,
        start_date,
        end_date,
    ):

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8-sig",
        ) as file:

            writer = csv.writer(
                file
            )

            writer.writerow([
                "Order Number",
                "Customer",
                "Mobile",
                "Order Date",
                "Delivery Date",
                "Status",
                "Subtotal",
                "Discount",
                "Tax",
                "Total Amount",
                "Advance Amount",
                "Remaining Amount",
                "Description",
            ])

            for order in orders:

                writer.writerow([
                    order.get(
                        "order_number",
                        "",
                    ),

                    order.get(
                        "customer_name",
                        "",
                    ),

                    order.get(
                        "customer_mobile",
                        "",
                    ),

                    order.get(
                        "order_date",
                        "",
                    ),

                    order.get(
                        "delivery_date",
                        "",
                    ),

                    order.get(
                        "status",
                        "",
                    ),

                    order.get(
                        "subtotal",
                        0,
                    ),

                    order.get(
                        "discount",
                        0,
                    ),

                    order.get(
                        "tax",
                        0,
                    ),

                    order.get(
                        "total_amount",
                        0,
                    ),

                    order.get(
                        "advance_amount",
                        0,
                    ),

                    order.get(
                        "remaining_amount",
                        0,
                    ),

                    order.get(
                        "description",
                        "",
                    ),
                ])

    # ==========================================================
    # EXPORT CUSTOMER CSV
    # ==========================================================

    def export_customer_csv(
        self,
        file_path,
        customers,
        start_date,
        end_date,
    ):

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8-sig",
        ) as file:

            writer = csv.writer(
                file
            )

            writer.writerow([
                "Customer ID",
                "Customer Name",
                "Mobile",
                "Email",
                "Customer Type",
                "Reference",
                "Orders",
                "Revenue",
                "Last Order",
            ])

            for customer in customers:

                writer.writerow([
                    customer.get(
                        "customer_id",
                        "",
                    ),

                    customer.get(
                        "customer_name",
                        "",
                    ),

                    customer.get(
                        "mobile",
                        "",
                    ),

                    customer.get(
                        "email",
                        "",
                    ),

                    customer.get(
                        "customer_type",
                        "",
                    ),

                    customer.get(
                        "reference",
                        "",
                    ),

                    customer.get(
                        "orders",
                        0,
                    ),

                    customer.get(
                        "revenue",
                        0,
                    ),

                    customer.get(
                        "last_order",
                        "",
                    ),
                ])

    # ==========================================================
    # EXPORT INVENTORY CSV
    # ==========================================================

    def export_inventory_csv(
        self,
        file_path,
        transactions,
        start_date,
        end_date,
    ):

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8-sig",
        ) as file:

            writer = csv.writer(
                file
            )

            writer.writerow([
                "Transaction ID",
                "Item",
                "SKU",
                "Category",
                "Transaction Type",
                "Quantity",
                "Unit",
                "Reference Type",
                "Reference ID",
                "Notes",
                "Date",
            ])

            for transaction in transactions:

                writer.writerow([
                    transaction.get(
                        "transaction_id",
                        "",
                    ),

                    transaction.get(
                        "item_name",
                        "",
                    ),

                    transaction.get(
                        "sku",
                        "",
                    ),

                    transaction.get(
                        "category",
                        "",
                    ),

                    transaction.get(
                        "transaction_type",
                        "",
                    ),

                    transaction.get(
                        "quantity",
                        0,
                    ),

                    transaction.get(
                        "unit",
                        "",
                    ),

                    transaction.get(
                        "reference_type",
                        "",
                    ),

                    transaction.get(
                        "reference_id",
                        "",
                    ),

                    transaction.get(
                        "notes",
                        "",
                    ),

                    transaction.get(
                        "created_at",
                        "",
                    ),
                ])

    # ==========================================================
    # EXPORT OVERALL CSV
    # ==========================================================

    def export_overall_csv(
        self,
        file_path,
        orders,
        customers,
        inventory,
        start_date,
        end_date,
    ):

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8-sig",
        ) as file:

            writer = csv.writer(
                file
            )

            # ==================================================
            # HEADER
            # ==================================================

            writer.writerow([
                "TAILOR SHOP REPORT"
            ])

            writer.writerow([
                "From",
                start_date.strftime(
                    "%d/%m/%Y"
                ),
                "To",
                end_date.strftime(
                    "%d/%m/%Y"
                ),
            ])

            writer.writerow([])

            # ==================================================
            # ORDERS
            # ==================================================

            writer.writerow([
                "ORDERS"
            ])

            writer.writerow([
                "Order Number",
                "Customer",
                "Mobile",
                "Order Date",
                "Delivery Date",
                "Status",
                "Subtotal",
                "Discount",
                "Tax",
                "Total",
                "Advance",
                "Remaining",
            ])

            for order in orders:

                writer.writerow([
                    order.get(
                        "order_number",
                        "",
                    ),

                    order.get(
                        "customer_name",
                        "",
                    ),

                    order.get(
                        "customer_mobile",
                        "",
                    ),

                    order.get(
                        "order_date",
                        "",
                    ),

                    order.get(
                        "delivery_date",
                        "",
                    ),

                    order.get(
                        "status",
                        "",
                    ),

                    order.get(
                        "subtotal",
                        0,
                    ),

                    order.get(
                        "discount",
                        0,
                    ),

                    order.get(
                        "tax",
                        0,
                    ),

                    order.get(
                        "total_amount",
                        0,
                    ),

                    order.get(
                        "advance_amount",
                        0,
                    ),

                    order.get(
                        "remaining_amount",
                        0,
                    ),
                ])

            writer.writerow([])

            # ==================================================
            # CUSTOMERS
            # ==================================================

            writer.writerow([
                "CUSTOMERS"
            ])

            writer.writerow([
                "Customer",
                "Mobile",
                "Email",
                "Type",
                "Orders",
                "Revenue",
                "Last Order",
            ])

            for customer in customers:

                writer.writerow([
                    customer.get(
                        "customer_name",
                        "",
                    ),

                    customer.get(
                        "mobile",
                        "",
                    ),

                    customer.get(
                        "email",
                        "",
                    ),

                    customer.get(
                        "customer_type",
                        "",
                    ),

                    customer.get(
                        "orders",
                        0,
                    ),

                    customer.get(
                        "revenue",
                        0,
                    ),

                    customer.get(
                        "last_order",
                        "",
                    ),
                ])

            writer.writerow([])

            # ==================================================
            # INVENTORY
            # ==================================================

            writer.writerow([
                "INVENTORY TRANSACTIONS"
            ])

            writer.writerow([
                "Item",
                "SKU",
                "Category",
                "Transaction",
                "Quantity",
                "Unit",
                "Reference",
                "Date",
            ])

            for item in inventory:

                writer.writerow([
                    item.get(
                        "item_name",
                        "",
                    ),

                    item.get(
                        "sku",
                        "",
                    ),

                    item.get(
                        "category",
                        "",
                    ),

                    item.get(
                        "transaction_type",
                        "",
                    ),

                    item.get(
                        "quantity",
                        0,
                    ),

                    item.get(
                        "unit",
                        "",
                    ),

                    item.get(
                        "reference_type",
                        "",
                    ),

                    item.get(
                        "created_at",
                        "",
                    ),
                ])

    # ==========================================================
    # NUMBER HELPER
    # ==========================================================

    @staticmethod
    def to_float(
        value,
    ):

        try:

            return float(
                value or 0
            )

        except (
            TypeError,
            ValueError,
        ):

            return 0.0