from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QMessageBox,
    QStackedWidget,
    QFrame,
)
from PySide6.QtCore import Qt

from widgets.orders.order_header import OrderHeader
from widgets.orders.order_stats import OrderStats
from widgets.orders.order_filter import OrderFilter
from widgets.orders.order_table import OrderTable
from widgets.orders.order_pagination import OrderPagination

from views.orders.order_form import OrderForm

from data.order_data import (
    get_order_list,
    get_order_stats,
)

from data.order_crud import (
    delete_order,
)


class OrderPage(QWidget):

    def __init__(self):

        super().__init__()

        self.current_page = 1
        self.page_size = 10

        self.build_ui()
        self.connect_events()
        self.load_data()

    # ==========================================================
    # BUILD UI
    # ==========================================================

    def build_ui(self):

        self.setObjectName(
            "OrderPage"
        )

        self.setStyleSheet("""
        
        /* =====================================================
           MAIN PAGE
           ===================================================== */

        QWidget#OrderPage {
            background: #111827;
            color: #F9FAFB;
        }

        /* =====================================================
           SCROLL AREA
           ===================================================== */

        QScrollArea {
            background: #111827;
            border: none;
        }

        QScrollArea QWidget {
            background: #111827;
        }

        /* =====================================================
           FORM PAGE
           ===================================================== */

        QFrame#OrderFormContainer {
            background: #111827;
            border: none;
        }

        """)

        main = QVBoxLayout(self)

        main.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        main.setSpacing(0)

        # ======================================================
        # STACK
        # ======================================================

        self.stack = QStackedWidget()

        self.stack.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        main.addWidget(
            self.stack
        )

        # ======================================================
        # LIST PAGE
        # ======================================================

        self.build_list_page()

        # ======================================================
        # FORM PAGE
        # ======================================================

        self.build_form_page()

        # ======================================================
        # STACK
        # ======================================================

        self.stack.addWidget(
            self.list_page
        )

        self.stack.addWidget(
            self.form_page
        )

        self.stack.setCurrentWidget(
            self.list_page
        )

    # ==========================================================
    # LIST PAGE
    # ==========================================================

    def build_list_page(self):

        self.list_page = QWidget()

        self.list_page.setObjectName(
            "OrderListPage"
        )

        list_layout = QVBoxLayout(
            self.list_page
        )

        list_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        list_layout.setSpacing(0)

        # ======================================================
        # SCROLL
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

        scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        # ======================================================
        # CONTENT
        # ======================================================

        container = QWidget()

        container.setObjectName(
            "OrderListContainer"
        )

        root = QVBoxLayout(
            container
        )

        root.setContentsMargins(
            25,
            25,
            25,
            25,
        )

        root.setSpacing(
            20
        )

        # ======================================================
        # HEADER
        # ======================================================

        self.header = OrderHeader()

        root.addWidget(
            self.header
        )

        # ======================================================
        # STATS
        # ======================================================

        self.stats = OrderStats()

        root.addWidget(
            self.stats
        )

        # ======================================================
        # FILTER
        # ======================================================

        self.filter = OrderFilter()

        root.addWidget(
            self.filter
        )

        # ======================================================
        # TABLE
        # ======================================================

        self.table = OrderTable()

        root.addWidget(
            self.table,
            1
        )

        # ======================================================
        # PAGINATION
        # ======================================================

        self.pagination = OrderPagination()

        root.addWidget(
            self.pagination
        )

        scroll.setWidget(
            container
        )

        list_layout.addWidget(
            scroll
        )

    # ==========================================================
    # FORM PAGE
    # ==========================================================

    def build_form_page(self):

        self.form_page = QWidget()

        self.form_page.setObjectName(
            "OrderFormPage"
        )

        form_layout = QVBoxLayout(
            self.form_page
        )

        form_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        form_layout.setSpacing(
            0
        )

        # ======================================================
        # FORM CONTAINER
        # ======================================================

        form_container = QFrame()

        form_container.setObjectName(
            "OrderFormContainer"
        )

        container_layout = QVBoxLayout(
            form_container
        )

        container_layout.setContentsMargins(
            25,
            25,
            25,
            25,
        )

        container_layout.setSpacing(
            0
        )

        # ======================================================
        # FORM
        # ======================================================

        self.form = OrderForm()

        container_layout.addWidget(
            self.form
        )

        form_layout.addWidget(
            form_container
        )

    # ==========================================================
    # EVENTS
    # ==========================================================

    def connect_events(self):

        # ======================================================
        # HEADER
        # ======================================================

        self.header.addOrderClicked.connect(
            self.open_new_order
        )

        # ======================================================
        # FILTERS
        # ======================================================

        self.filter.searchChanged.connect(
            self.on_filter_changed
        )

        self.filter.statusChanged.connect(
            self.on_filter_changed
        )

        self.filter.paymentChanged.connect(
            self.on_filter_changed
        )

        self.filter.tailorChanged.connect(
            self.on_filter_changed
        )

        self.filter.dateChanged.connect(
            self.on_filter_changed
        )

        self.filter.refreshClicked.connect(
            self.refresh
        )

        # ======================================================
        # PAGINATION
        # ======================================================

        self.pagination.pageChanged.connect(
            self.change_page
        )

        self.pagination.pageSizeChanged.connect(
            self.change_page_size
        )

        # ======================================================
        # TABLE
        # ======================================================

        self.table.viewClicked.connect(
            self.view_order
        )

        self.table.editClicked.connect(
            self.edit_order
        )

        self.table.deleteClicked.connect(
            self.delete_order
        )

        # ======================================================
        # FORM
        # ======================================================

        self.form.backClicked.connect(
            self.back_to_list
        )

        self.form.orderSaved.connect(
            self.order_saved
        )

    # ==========================================================
    # LOAD DATA
    # ==========================================================

    def load_data(self):

        try:

            filters = (
                self.filter.get_filters()
            )

            result = get_order_list(
                search=filters["search"],
                status=filters["status"],
                payment=filters["payment"],
                tailor=filters["tailor"],
                date_value=filters["date"],
                page=self.current_page,
                page_size=self.page_size,
            )

            # ==================================================
            # TABLE
            # ==================================================

            self.table.set_data(
                result["items"]
            )

            # ==================================================
            # PAGINATION
            # ==================================================

            self.pagination.set_pagination(
                current=result[
                    "current_page"
                ],
                total=result[
                    "total_pages"
                ],
                total_records=result[
                    "total_records"
                ],
            )

            # ==================================================
            # STATS
            # ==================================================

            stats = get_order_stats()

            self.stats.set_stats(
                stats
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"Unable to load orders:\n\n{e}",
            )

    # ==========================================================
    # FILTER
    # ==========================================================

    def on_filter_changed(
        self,
        *args,
    ):

        self.current_page = 1

        self.load_data()

    # ==========================================================
    # REFRESH
    # ==========================================================

    def refresh(self):

        self.load_data()

    # ==========================================================
    # PAGINATION
    # ==========================================================

    def change_page(
        self,
        page,
    ):

        self.current_page = page

        self.load_data()

    # ==========================================================
    # PAGE SIZE
    # ==========================================================

    def change_page_size(
        self,
        size,
    ):

        self.page_size = size

        self.current_page = 1

        self.load_data()

    # ==========================================================
    # NEW ORDER
    # ==========================================================

    def open_new_order(self):

        # Reset form
        self.form.prepare_new()

        # Show form page
        self.stack.setCurrentWidget(
            self.form_page
        )

    # ==========================================================
    # EDIT ORDER
    # ==========================================================

    def edit_order(
        self,
        order,
    ):

        self.form.load_order(
            order
        )

        self.stack.setCurrentWidget(
            self.form_page
        )

    # ==========================================================
    # VIEW ORDER
    # ==========================================================

    def view_order(
        self,
        order,
    ):

        QMessageBox.information(
            self,
            "Order Details",
            (
                f"Order: "
                f"{order['order_number']}\n\n"

                f"Customer: "
                f"{order['customer_name']}\n\n"

                f"Status: "
                f"{order['status']}\n\n"

                f"Total: "
                f"₹{order['total_amount']:.2f}\n\n"

                f"Advance: "
                f"₹{order['advance_amount']:.2f}\n\n"

                f"Remaining: "
                f"₹{order['remaining_amount']:.2f}"
            ),
        )

    # ==========================================================
    # DELETE ORDER
    # ==========================================================

    def delete_order(
        self,
        order,
    ):

        answer = QMessageBox.question(
            self,
            "Delete Order",
            (
                f"Are you sure you want to delete "
                f"'{order['order_number']}'?"
            ),
            QMessageBox.Yes
            | QMessageBox.No,
        )

        if answer != QMessageBox.Yes:
            return

        try:

            success = delete_order(
                order["id"]
            )

            if success:

                QMessageBox.information(
                    self,
                    "Deleted",
                    "Order deleted successfully.",
                )

                self.load_data()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"Unable to delete order:\n\n{e}",
            )

    # ==========================================================
    # BACK TO LIST
    # ==========================================================

    def back_to_list(self):

        self.stack.setCurrentWidget(
            self.list_page
        )

        self.current_page = 1

        self.load_data()

    # ==========================================================
    # ORDER SAVED
    # ==========================================================

    def order_saved(
        self,
        order,
    ):

        self.stack.setCurrentWidget(
            self.list_page
        )

        self.current_page = 1

        self.load_data()