import csv

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QFileDialog,
    QMessageBox,
    QStackedWidget,
)
from PySide6.QtCore import Qt

from widgets.customer.customer_header import CustomerHeader
from widgets.customer.customer_stats import CustomerStats
from widgets.customer.customer_filter import CustomerFilter
from widgets.customer.customer_table import CustomerTable
from widgets.customer.customer_pagination import CustomerPagination

from views.customers.customer_form import CustomerForm

from data.customer_data import CustomerDataService


class CustomerPage(QWidget):

    def __init__(self):
        super().__init__()

        self.current_page_num = 1
        self.page_size = 10

        self.build_ui()
        self.refresh_all_data()

    # ==========================================================
    # BUILD UI
    # ==========================================================

    def build_ui(self):


        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ======================================================
        # STACKED WIDGET
        # ======================================================

        self.stack = QStackedWidget()

        # ------------------------------------------------------
        # PAGE 1 - CUSTOMER LIST
        # ------------------------------------------------------

        self.customer_list_page = QWidget()

        list_layout = QVBoxLayout(
            self.customer_list_page
        )

        list_layout.setContentsMargins(
            0, 0, 0, 0
        )

        list_layout.setSpacing(0)

        # ------------------------------------------------------
        # SCROLL AREA
        # ------------------------------------------------------

        scroll = QScrollArea()

        scroll.setWidgetResizable(True)

        scroll.setFrameShape(
            QScrollArea.NoFrame
        )

        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        # ------------------------------------------------------
        # CONTAINER
        # ------------------------------------------------------

        container = QWidget()


        root = QVBoxLayout(container)

        root.setContentsMargins(
            25, 25, 25, 25
        )

        root.setSpacing(22)

        # ------------------------------------------------------
        # HEADER
        # ------------------------------------------------------

        self.header = CustomerHeader()

        root.addWidget(
            self.header
        )

        # ------------------------------------------------------
        # STATS
        # ------------------------------------------------------

        self.stats = CustomerStats()

        root.addWidget(
            self.stats
        )

        # ------------------------------------------------------
        # FILTER
        # ------------------------------------------------------

        self.filter = CustomerFilter()

        root.addWidget(
            self.filter
        )

        # ------------------------------------------------------
        # TABLE
        # ------------------------------------------------------

        self.table = CustomerTable()

        root.addWidget(
            self.table,
            1
        )

        # ------------------------------------------------------
        # PAGINATION
        # ------------------------------------------------------

        self.pagination = CustomerPagination()

        root.addWidget(
            self.pagination
        )

        scroll.setWidget(
            container
        )

        list_layout.addWidget(
            scroll
        )

        # ------------------------------------------------------
        # ADD TO STACK
        # ------------------------------------------------------

        self.stack.addWidget(
            self.customer_list_page
        )

        # ======================================================
        # PAGE 2 - CUSTOMER FORM
        # ======================================================

        self.form_page = QWidget()

        form_layout = QVBoxLayout(
            self.form_page
        )

        form_layout.setContentsMargins(
            25, 25, 25, 25
        )

        form_layout.setSpacing(0)

        self.form = None

        self.stack.addWidget(
            self.form_page
        )

        # ======================================================
        # ADD STACK TO MAIN
        # ======================================================

        main_layout.addWidget(
            self.stack
        )

        # ======================================================
        # SIGNAL CONNECTIONS
        # ======================================================

        self.header.addCustomerClicked.connect(
            self.open_add_customer
        )

        self.header.refreshClicked.connect(
            self.refresh_all_data
        )

        self.header.exportClicked.connect(
            self.export_customers
        )

        self.filter.filterClicked.connect(
            self.search_customer
        )

        self.filter.resetClicked.connect(
            self.reset_filter
        )

        self.pagination.pageChanged.connect(
            self.on_page_changed
        )

        self.pagination.pageSizeChanged.connect(
            self.on_page_size_changed
        )

        self.table.editCustomerRequested.connect(
            self.open_edit_customer
        )

        self.table.deleteCustomerRequested.connect(
            self.delete_customer
        )

    # ==========================================================
    # REFRESH
    # ==========================================================

    def refresh_all_data(self):

        stats_data = (
            CustomerDataService.fetch_stats()
        )

        self.stats.set_stats(
            stats_data
        )

        self.load_table_data()

    # ==========================================================
    # LOAD TABLE
    # ==========================================================

    def load_table_data(self):

        name = (
            self.filter.searchName.text()
        )

        mobile = (
            self.filter.mobile.text()
        )

        status = (
            self.filter.status.currentText()
        )

        ctype = (
            self.filter.customerType.currentText()
        )

        result = (
            CustomerDataService.fetch_customers(
                name_query=name,
                mobile_query=mobile,
                status_filter=status,
                type_filter=ctype,
                page=self.current_page_num,
                page_size=self.page_size
            )
        )

        self.table.load_data(
            result.customers
        )

        self.pagination.set_pagination(
            current=result.current_page,
            total=result.total_pages,
            total_records=result.total_count
        )

    # ==========================================================
    # SEARCH
    # ==========================================================

    def search_customer(self):

        self.current_page_num = 1

        self.load_table_data()

    # ==========================================================
    # RESET FILTER
    # ==========================================================

    def reset_filter(self):

        self.filter.searchName.clear()

        self.filter.mobile.clear()

        self.filter.status.setCurrentIndex(
            0
        )

        self.filter.customerType.setCurrentIndex(
            0
        )

        self.current_page_num = 1

        self.load_table_data()

    # ==========================================================
    # PAGINATION
    # ==========================================================

    def on_page_changed(
        self,
        page: int
    ):

        self.current_page_num = page

        self.load_table_data()

    # ==========================================================
    # PAGE SIZE
    # ==========================================================

    def on_page_size_changed(
        self,
        size: int
    ):

        self.page_size = size

        self.current_page_num = 1

        self.load_table_data()

    # ==========================================================
    # ADD CUSTOMER
    # ==========================================================

    def open_add_customer(self):

        # Remove old form
        if self.form is not None:

            self.form.deleteLater()

            self.form = None

        # Create new form
        self.form = CustomerForm()

        # Add form to form page
        self.form_page.layout().addWidget(
            self.form
        )

        # Show form page
        self.stack.setCurrentWidget(
            self.form_page
        )

        # Optional back signal
        if hasattr(
            self.form,
            "backRequested"
        ):
            self.form.backRequested.connect(
                self.show_customer_list
            )

    # ==========================================================
    # EDIT CUSTOMER
    # ==========================================================

    def open_edit_customer(
        self,
        customer_id: int
    ):

        # Remove old form
        if self.form is not None:

            self.form.deleteLater()

            self.form = None

        # Create edit form
        self.form = CustomerForm(
            customer_id=customer_id
        )

        # Add form to same content area
        self.form_page.layout().addWidget(
            self.form
        )

        # Switch to form
        self.stack.setCurrentWidget(
            self.form_page
        )

        # Optional back signal
        if hasattr(
            self.form,
            "backRequested"
        ):
            self.form.backRequested.connect(
                self.show_customer_list
            )

    # ==========================================================
    # SHOW CUSTOMER LIST
    # ==========================================================

    def show_customer_list(self):

        self.stack.setCurrentWidget(
            self.customer_list_page
        )

        self.refresh_all_data()

    # ==========================================================
    # DELETE CUSTOMER
    # ==========================================================

    def delete_customer(
        self,
        customer_id: int
    ):

        reply = QMessageBox.question(
            self,
            "Delete Customer",
            "Are you sure you want to delete this customer?",
            QMessageBox.Yes |
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:

            conn = (
                CustomerDataService
                .get_connection()
            )

            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM customers WHERE id = ?",
                (customer_id,)
            )

            conn.commit()
            conn.close()

            self.refresh_all_data()

    # ==========================================================
    # EXPORT CUSTOMERS
    # ==========================================================

    def export_customers(self):

        file_path, _ = (
            QFileDialog.getSaveFileName(
                self,
                "Export Customers to CSV",
                "customers.csv",
                "CSV Files (*.csv)"
            )
        )

        if not file_path:
            return

        conn = (
            CustomerDataService
            .get_connection()
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                name,
                mobile,
                email,
                gender,
                customer_type,
                is_active,
                created_at
            FROM customers
            """
        )

        rows = cursor.fetchall()

        conn.close()

        with open(
            file_path,
            mode="w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                "ID",
                "Name",
                "Mobile",
                "Email",
                "Gender",
                "Customer Type",
                "Is Active",
                "Created At"
            ])

            writer.writerows(rows)

        QMessageBox.information(
            self,
            "Export Success",
            "Customers exported successfully!"
        )