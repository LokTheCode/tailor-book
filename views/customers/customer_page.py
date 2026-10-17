import csv
import sqlite3
from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QFileDialog,
    QMessageBox,
    QStackedWidget,
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices

from widgets.customer.customer_header import CustomerHeader
from widgets.customer.customer_stats import CustomerStats
from widgets.customer.customer_filter import CustomerFilter
from widgets.customer.customer_table import CustomerTable
from widgets.customer.customer_pagination import CustomerPagination

from views.customers.customer_form import CustomerForm

from data.customer_data import CustomerDataService
import data.customer_crud as db
from services import settings_service
from utils import excel_export
from utils.excel_export import Column, Sheet
from data.customer_crud import CustomerHasOrders


class CustomerPage(QWidget):

    def __init__(self):
        super().__init__()

        self.current_page_num = 1
        self.page_size = settings_service.get_int("rows_per_page", 10)

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

        # Rows per page from Settings > General
        self.pagination.page_size.blockSignals(True)
        self.pagination.page_size.setCurrentText(str(self.page_size))
        self.pagination.page_size.blockSignals(False)

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

        self.connect_form()

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

        self.connect_form()

    # ==========================================================
    # FORM SIGNALS
    # ==========================================================

    def connect_form(self):
        """Back, Cancel, Save, Update and Delete all return to the list."""

        self.form.backRequested.connect(self.show_customer_list)
        self.form.customerSaved.connect(self.show_customer_list)
        self.form.customerUpdated.connect(self.show_customer_list)
        self.form.customerDeleted.connect(self.show_customer_list)

    # ==========================================================
    # SHOW CUSTOMER LIST
    # ==========================================================

    def show_customer_list(self, *_):

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

        customer = db.get_customer_by_id(customer_id)
        if customer is None:
            self.refresh_all_data()
            return

        name = customer["name"]

        reply = QMessageBox.question(
            self,
            "Delete Customer",
            f"Delete {name} and all their measurements?\n\nThis can't be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        try:
            db.delete_customer(customer_id)

        except CustomerHasOrders as error:

            # Customers with orders are deactivated instead, so their
            # order history keeps pointing at a real customer
            reply = QMessageBox.question(
                self,
                "Customer has orders",
                f"{error}\n\nDeactivate {name} now?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )

            if reply == QMessageBox.Yes:
                db.set_customer_active(customer_id, False)

        self.refresh_all_data()

    # ==========================================================
    # EXPORT CUSTOMERS
    # ==========================================================

    def export_customers(self):

        excel = excel_export.is_available()
        stamp = datetime.now().strftime("%Y-%m-%d")

        file_path, chosen = QFileDialog.getSaveFileName(
            self,
            "Export Customers",
            f"customers_{stamp}.{'xlsx' if excel else 'csv'}",
            "Excel Workbook (*.xlsx);;CSV (*.csv)" if excel else "CSV (*.csv)",
        )

        if not file_path:
            return

        conn = CustomerDataService.get_connection()
        conn.row_factory = sqlite3.Row
        rows = [
            dict(row) for row in conn.execute(
                """
                SELECT
                    c.id, c.name, c.mobile, c.alternate_mobile, c.email, c.gender,
                    c.customer_type, c.reference, c.address,
                    CASE WHEN c.is_active = 1 THEN 'Active' ELSE 'Inactive' END AS status,
                    substr(c.created_at, 1, 10) AS created,
                    (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id) AS orders,
                    (SELECT COALESCE(SUM(o.total_amount), 0) FROM orders o
                      WHERE o.customer_id = c.id AND LOWER(o.status) != 'cancelled') AS spent,
                    (SELECT COALESCE(SUM(o.remaining_amount), 0) FROM orders o
                      WHERE o.customer_id = c.id AND LOWER(o.status) != 'cancelled') AS pending
                FROM customers c
                ORDER BY c.id
                """
            )
        ]
        conn.close()

        columns = [
            Column("ID", "id", "int", width=7),
            Column("Name", "name"),
            Column("Mobile", "mobile"),
            Column("Alt. Mobile", "alternate_mobile"),
            Column("Email", "email"),
            Column("Gender", "gender"),
            Column("Type", "customer_type"),
            Column("Reference", "reference"),
            Column("Address", "address", width=34),
            Column("Status", "status", "status"),
            Column("Joined", "created"),
            Column("Orders", "orders", "int", total=True),
            Column("Total Spent", "spent", "money", total=True),
            Column("Pending", "pending", "money", total=True),
        ]

        try:
            if file_path.lower().endswith(".csv") or "CSV" in chosen:
                # utf-8-sig so Excel shows ₹ and Hindi names correctly
                with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
                    writer = csv.writer(f)
                    writer.writerow([c.header for c in columns])
                    for row in rows:
                        writer.writerow([row.get(c.key, "") for c in columns])
            else:
                if not file_path.lower().endswith(".xlsx"):
                    file_path += ".xlsx"
                active = sum(1 for r in rows if r["status"] == "Active")
                excel_export.export(
                    file_path,
                    "Customer List",
                    [Sheet("Customers", "Customer List", columns, rows, summary=[
                        ("Total customers", len(rows), "int"),
                        ("Active", active, "int"),
                        ("Inactive", len(rows) - active, "int"),
                    ])],
                )

        except OSError as error:
            QMessageBox.warning(
                self,
                "Export Failed",
                f"Couldn't write the file. If it's open in Excel, close it and try again.\n\n{error}"
            )
            return

        reply = QMessageBox.question(
            self,
            "Export Success",
            f"Exported {len(rows)} customers to:\n{file_path}\n\nOpen it now?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )
        if reply == QMessageBox.Yes:
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))