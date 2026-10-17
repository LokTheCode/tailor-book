from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QMessageBox,
    QStackedWidget,
)

from PySide6.QtCore import Qt


from widgets.measurement_list.measurement_header import (
    MeasurementHeader,
)

from widgets.measurement_list.measurement_stats import (
    MeasurementStats,
)

from widgets.measurement_list.measurement_filter import (
    MeasurementFilter,
)

from widgets.measurement_list.measurement_table import (
    MeasurementTable,
)

from widgets.measurement_list.measurement_pagination import (
    MeasurementPagination,
)

from views.measurements.measurement_form import (
    MeasurementForm,
)

from data.measurement_data import (
    get_measurement_list,
    get_measurement_stats,
)

from services import settings_service
from data.measurement_crud import (
    delete_measurement,
)


class MeasurementPage(QWidget):

    def __init__(self):

        super().__init__()

        self.current_page = 1

        self.page_size = settings_service.get_int("rows_per_page", 10)

        self.build_ui()

        self.connect_events()

        self.load_data()

    # ======================================================
    # BUILD UI
    # ======================================================

    def build_ui(self):

        self.setObjectName(
            "MeasurementPage"
        )


        main = QVBoxLayout(self)

        main.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        # ==================================================
        # STACK
        # ==================================================

        self.stack = QStackedWidget()

        main.addWidget(
            self.stack
        )

        # ==================================================
        # LIST PAGE
        # ==================================================

        self.list_page = QWidget()

        list_layout = QVBoxLayout(
            self.list_page
        )

        list_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        # ==================================================
        # SCROLL
        # ==================================================

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        container = QWidget()

        root = QVBoxLayout(container)
        
        root.setContentsMargins(
            25, 25, 25, 25
        )
        
        root.setSpacing(22)

        # ==================================================
        # HEADER
        # ==================================================

        self.header = (
            MeasurementHeader()
        )

        root.addWidget(
            self.header
        )

        # ==================================================
        # STATS
        # ==================================================

        self.stats = (
            MeasurementStats()
        )

        root.addWidget(
            self.stats
        )

        # ==================================================
        # FILTER
        # ==================================================

        self.filter = (
            MeasurementFilter()
        )

        root.addWidget(
            self.filter
        )

        # ==================================================
        # TABLE
        # ==================================================

        self.table = (
            MeasurementTable()
        )

        root.addWidget(
            self.table
        )

        # ==================================================
        # PAGINATION
        # ==================================================

        self.pagination = (
            MeasurementPagination()
        )

        # Rows per page from Settings > General
        self.pagination.page_size.blockSignals(True)
        self.pagination.page_size.setCurrentText(str(self.page_size))
        self.pagination.page_size.blockSignals(False)

        root.addWidget(
            self.pagination
        )

        root.addStretch()

        scroll.setWidget(
            container
        )

        list_layout.addWidget(
            scroll
        )

        # ==================================================
        # FORM PAGE
        # ==================================================

        self.form_page = QWidget()

        form_layout = QVBoxLayout(
            self.form_page
        )

        form_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.form = (
            MeasurementForm()
        )

        form_layout.addWidget(
            self.form
        )

        # ==================================================
        # STACK PAGES
        # ==================================================

        self.stack.addWidget(
            self.list_page
        )

        self.stack.addWidget(
            self.form_page
        )

        self.stack.setCurrentWidget(
            self.list_page
        )

    # ======================================================
    # EVENTS
    # ======================================================

    def connect_events(self):

        # -----------------------------------------------
        # ADD
        # -----------------------------------------------

        self.header.addMeasurementClicked.connect(
            self.open_measurement_form
        )

        # -----------------------------------------------
        # FILTER
        # -----------------------------------------------

        self.filter.searchChanged.connect(
            self.on_filter_changed
        )

        self.filter.garmentChanged.connect(
            self.on_filter_changed
        )

        self.filter.dateChanged.connect(
            self.on_filter_changed
        )

        self.filter.refreshClicked.connect(
            self.refresh
        )

        # -----------------------------------------------
        # PAGINATION
        # -----------------------------------------------

        self.pagination.pageChanged.connect(
            self.change_page
        )

        self.pagination.pageSizeChanged.connect(
            self.change_page_size
        )

        # -----------------------------------------------
        # TABLE
        # -----------------------------------------------

        self.table.editClicked.connect(
            self.edit_measurement
        )

        self.table.deleteClicked.connect(
            self.delete_measurement
        )

        # -----------------------------------------------
        # FORM
        # -----------------------------------------------

        # Form: Back, Save, Update and Delete all return to the list
        self.form.backRequested.connect(
            self.show_list
        )

        self.form.measurementSaved.connect(
            self.measurement_saved
        )

        self.form.measurementDeleted.connect(
            self.show_list
        )

    # ======================================================
    # LOAD DATA
    # ======================================================

    def load_data(self):

        try:

            filters = (
                self.filter.get_filters()
            )

            result = get_measurement_list(

                search=filters["search"],

                garment=filters["garment"],

                date_value=filters["date"],

                page=self.current_page,

                page_size=self.page_size,
            )

            self.table.set_data(
                result["items"]
            )

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

            stats = (
                get_measurement_stats()
            )

            self.stats.set_stats(
                stats
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"Unable to load measurements:\n\n{e}",
            )

    # ======================================================
    # FILTER
    # ======================================================

    def on_filter_changed(self, *args):

        self.current_page = 1

        self.load_data()

    # ======================================================
    # REFRESH
    # ======================================================

    def refresh(self):

        self.load_data()

    # ======================================================
    # PAGE
    # ======================================================

    def change_page(self, page):

        self.current_page = page

        self.load_data()

    # ======================================================
    # PAGE SIZE
    # ======================================================

    def change_page_size(self, size):

        self.page_size = size

        self.current_page = 1

        self.load_data()

    # ======================================================
    # OPEN FORM
    # ======================================================

    def open_measurement_form(self):

        self.form.open_new()

        self.stack.setCurrentWidget(
            self.form_page
        )

    def edit_measurement(
        self,
        measurement,
    ):

        self.form.load_measurement(
            measurement
        )

        self.stack.setCurrentWidget(
            self.form_page
        )

    def show_list(self, *_):

        self.stack.setCurrentWidget(
            self.list_page
        )

        self.load_data()

    def delete_measurement(
        self,
        measurement,
    ):

        result = QMessageBox.question(

            self,

            "Delete Measurement",

            (
                "Are you sure you want to delete "
                f"'{measurement['measurement_name']}' "
                "measurement?"
            ),

            QMessageBox.Yes
            | QMessageBox.No,
        )

        if result != QMessageBox.Yes:
            return

        try:

            success = delete_measurement(
                measurement["id"]
            )

            if success:

                QMessageBox.information(
                    self,
                    "Deleted",
                    "Measurement deleted successfully.",
                )

                self.load_data()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"Unable to delete measurement:\n\n{e}",
            )

    # ======================================================
    # SAVED
    # ======================================================

    def measurement_saved(
        self,
        measurement,
    ):

        self.stack.setCurrentWidget(
            self.list_page
        )

        self.current_page = 1

        self.load_data()