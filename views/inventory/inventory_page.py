from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QMessageBox,
    QStackedWidget,
)

from PySide6.QtCore import Qt

from views.inventory.inventory_header import (
    InventoryHeader,
)

from views.inventory.inventory_stats import (
    InventoryStats,
)

from views.inventory.inventory_filter import (
    InventoryFilter,
)

from views.inventory.inventory_table import (
    InventoryTable,
)

from views.inventory.inventory_pagination import (
    InventoryPagination,
)

from views.inventory.inventory_form import (
    InventoryForm,
)

from views.inventory.stock_transaction_form import (
    StockTransactionDialog,
)

from data.inventory_data import (
    get_inventory_list,
    get_inventory_stats,
    get_inventory_categories,
)

from data.inventory_crud import (
    delete_inventory_item,
)


class InventoryPage(QWidget):

    def __init__(self):

        super().__init__()

        self.current_page = 1
        self.page_size = 10

        self.filters = {
            "search": "",
            "category": "All Categories",
            "stock_status": "All Stock",
        }

        self.build_ui()

        self.refresh_all_data()

    # ==========================================================
    # BUILD UI
    # ==========================================================

    def build_ui(self):

        self.setObjectName(
            "InventoryPage"
        )

        self.setStyleSheet("""
        QWidget {
            background: #111827;
        }

        QScrollArea {
            border: none;
            background: #111827;
        }
        """)

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
        # STACKED WIDGET
        # ======================================================

        self.stack = QStackedWidget()

        # ======================================================
        # PAGE 1 - INVENTORY LIST
        # ======================================================

        self.inventory_list_page = QWidget()

        list_layout = QVBoxLayout(
            self.inventory_list_page
        )

        list_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        list_layout.setSpacing(
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

        scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        # ======================================================
        # CONTAINER
        # ======================================================

        container = QWidget()

        container.setStyleSheet(
            "background:#111827;"
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
            22
        )

        # ======================================================
        # HEADER
        # ======================================================

        self.header = InventoryHeader()

        root.addWidget(
            self.header
        )

        # ======================================================
        # STATS
        # ======================================================

        self.stats = InventoryStats()

        root.addWidget(
            self.stats
        )

        # ======================================================
        # FILTER
        # ======================================================

        self.filter = InventoryFilter()

        root.addWidget(
            self.filter
        )

        # ======================================================
        # TABLE
        # ======================================================

        self.table = InventoryTable()

        root.addWidget(
            self.table,
            1
        )

        # ======================================================
        # PAGINATION
        # ======================================================

        self.pagination = InventoryPagination()

        root.addWidget(
            self.pagination
        )

        # ======================================================
        # SCROLL
        # ======================================================

        scroll.setWidget(
            container
        )

        list_layout.addWidget(
            scroll
        )

        # ======================================================
        # ADD LIST PAGE TO STACK
        # ======================================================

        self.stack.addWidget(
            self.inventory_list_page
        )

        # ======================================================
        # PAGE 2 - INVENTORY FORM
        # ======================================================

        self.form_page = QWidget()

        form_layout = QVBoxLayout(
            self.form_page
        )

        form_layout.setContentsMargins(
            25,
            25,
            25,
            25,
        )

        form_layout.setSpacing(
            0
        )

        self.form = None

        # ======================================================
        # ADD FORM PAGE TO STACK
        # ======================================================

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

        # ------------------------------------------------------
        # HEADER
        # ------------------------------------------------------

        self.header.addItemClicked.connect(
            self.open_add_inventory
        )

        self.header.refreshClicked.connect(
            self.refresh_all_data
        )

        # ------------------------------------------------------
        # FILTER
        # ------------------------------------------------------

        self.filter.filterChanged.connect(
            self.on_filter_changed
        )

        # ------------------------------------------------------
        # PAGINATION
        # ------------------------------------------------------

        self.pagination.pageChanged.connect(
            self.on_page_changed
        )

        self.pagination.pageSizeChanged.connect(
            self.on_page_size_changed
        )

        # ------------------------------------------------------
        # TABLE
        # ------------------------------------------------------

        self.table.editClicked.connect(
            self.open_edit_inventory
        )

        self.table.stockClicked.connect(
            self.stock_inventory
        )

        self.table.deleteClicked.connect(
            self.delete_inventory
        )

        # Optional view signal
        if hasattr(
            self.table,
            "viewClicked"
        ):

            self.table.viewClicked.connect(
                self.view_inventory
            )

    # ==========================================================
    # REFRESH ALL DATA
    # ==========================================================

    def refresh_all_data(self):

        # ======================================================
        # CATEGORIES
        # ======================================================

        categories = (
            get_inventory_categories()
        )

        self.filter.set_categories(
            categories
        )

        # ======================================================
        # STATS + TABLE
        # ======================================================

        self.load_data()

    # ==========================================================
    # LOAD DATA
    # ==========================================================

    def load_data(self):

        try:

            result = get_inventory_list(

                search=self.filters[
                    "search"
                ],

                category=self.filters[
                    "category"
                ],

                stock_status=self.filters[
                    "stock_status"
                ],

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

            self.pagination.set_data(

                current_page=result[
                    "current_page"
                ],

                total_pages=result[
                    "total_pages"
                ],

                total_records=result[
                    "total_records"
                ],

                page_size=result[
                    "page_size"
                ],
            )

            # ==================================================
            # STATS
            # ==================================================

            stats = get_inventory_stats()

            self.stats.set_data(
                stats
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"Unable to load inventory:\n\n{e}",
            )

    # ==========================================================
    # FILTER
    # ==========================================================

    def on_filter_changed(
        self,
        filters,
    ):

        self.filters = filters

        self.current_page = 1

        self.load_data()

    # ==========================================================
    # PAGE CHANGED
    # ==========================================================

    def on_page_changed(
        self,
        page: int,
    ):

        self.current_page = page

        self.load_data()

    # ==========================================================
    # PAGE SIZE CHANGED
    # ==========================================================

    def on_page_size_changed(
        self,
        size: int,
    ):

        self.page_size = size

        self.current_page = 1

        self.load_data()

    # ==========================================================
    # ADD INVENTORY
    # ==========================================================

    def open_add_inventory(self):

        # ------------------------------------------------------
        # REMOVE OLD FORM
        # ------------------------------------------------------

        if self.form is not None:

            self.form.deleteLater()

            self.form = None

        # ------------------------------------------------------
        # CREATE NEW FORM
        # ------------------------------------------------------

        self.form = InventoryForm()

        # ------------------------------------------------------
        # ADD FORM TO FORM PAGE
        # ------------------------------------------------------

        self.form_page.layout().addWidget(
            self.form
        )

        # ------------------------------------------------------
        # FORM BACK
        # ------------------------------------------------------

        if hasattr(
            self.form,
            "backClicked"
        ):

            self.form.backClicked.connect(
                self.show_inventory_list
            )

        # ------------------------------------------------------
        # FORM SAVED
        # ------------------------------------------------------

        if hasattr(
            self.form,
            "saved"
        ):

            self.form.saved.connect(
                self.inventory_saved
            )

        # ------------------------------------------------------
        # PREPARE NEW
        # ------------------------------------------------------

        if hasattr(
            self.form,
            "prepare_new"
        ):

            self.form.prepare_new()

        # ------------------------------------------------------
        # SHOW FORM
        # ------------------------------------------------------

        self.stack.setCurrentWidget(
            self.form_page
        )

    # ==========================================================
    # EDIT INVENTORY
    # ==========================================================

    def open_edit_inventory(
        self,
        item,
    ):

        # ------------------------------------------------------
        # REMOVE OLD FORM
        # ------------------------------------------------------

        if self.form is not None:

            self.form.deleteLater()

            self.form = None

        # ------------------------------------------------------
        # CREATE FORM
        # ------------------------------------------------------

        self.form = InventoryForm()

        # ------------------------------------------------------
        # ADD FORM
        # ------------------------------------------------------

        self.form_page.layout().addWidget(
            self.form
        )

        # ------------------------------------------------------
        # BACK
        # ------------------------------------------------------

        if hasattr(
            self.form,
            "backClicked"
        ):

            self.form.backClicked.connect(
                self.show_inventory_list
            )

        # ------------------------------------------------------
        # SAVED
        # ------------------------------------------------------

        if hasattr(
            self.form,
            "saved"
        ):

            self.form.saved.connect(
                self.inventory_saved
            )

        # ------------------------------------------------------
        # LOAD ITEM
        # ------------------------------------------------------

        if hasattr(
            self.form,
            "load_item"
        ):

            self.form.load_item(
                item
            )

        # ------------------------------------------------------
        # SHOW FORM
        # ------------------------------------------------------

        self.stack.setCurrentWidget(
            self.form_page
        )

    # ==========================================================
    # SHOW INVENTORY LIST
    # ==========================================================

    def show_inventory_list(self):

        self.stack.setCurrentWidget(
            self.inventory_list_page
        )

        self.refresh_all_data()

    # ==========================================================
    # STOCK TRANSACTION
    # ==========================================================

    def stock_inventory(
        self,
        item,
    ):

        dialog = StockTransactionDialog(
            item,
            self,
        )

        dialog.saved.connect(
            self.refresh_all_data
        )

        dialog.exec()

    # ==========================================================
    # VIEW INVENTORY
    # ==========================================================

    def view_inventory(
        self,
        item,
    ):

        QMessageBox.information(
            self,
            "Inventory Item",
            (
                f"Item: "
                f"{item.get('name', '')}\n\n"

                f"Category: "
                f"{item.get('category', '')}\n\n"

                f"SKU: "
                f"{item.get('sku', '')}\n\n"

                f"Quantity: "
                f"{item.get('quantity', 0)}\n\n"

                f"Unit: "
                f"{item.get('unit', '')}\n\n"

                f"Cost Price: "
                f"₹{item.get('cost_price', 0):,.2f}\n\n"

                f"Selling Price: "
                f"₹{item.get('selling_price', 0):,.2f}\n\n"

                f"Stock Status: "
                f"{item.get('stock_status', '')}"
            ),
        )

    # ==========================================================
    # DELETE INVENTORY
    # ==========================================================

    def delete_inventory(
        self,
        item,
    ):

        reply = QMessageBox.question(
            self,
            "Delete Inventory Item",
            (
                "Are you sure you want to deactivate "
                f'"{item["name"]}"?'
            ),
            QMessageBox.Yes |
            QMessageBox.No,
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        try:

            success = delete_inventory_item(
                item["id"]
            )

            if success:

                QMessageBox.information(
                    self,
                    "Deleted",
                    "Inventory item deleted successfully.",
                )

            self.refresh_all_data()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Delete Error",
                str(e),
            )

    # ==========================================================
    # INVENTORY SAVED
    # ==========================================================

    def inventory_saved(
        self,
        *args,
    ):

        self.stack.setCurrentWidget(
            self.inventory_list_page
        )

        self.current_page = 1

        self.refresh_all_data()