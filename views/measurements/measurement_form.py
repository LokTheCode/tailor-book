from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QComboBox,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QScrollArea,
    QFrame,
    QSizePolicy,
)

from data.customer_crud import (
    get_all_customers,
)

from data.measurement_crud import (
    create_measurement,
    get_measurements_by_customer,
    update_measurement,
    delete_measurement,
)

from widgets.measurement.measurement_fields import (
    MEASUREMENT_FIELDS,
)

from widgets.measurement.dynamic_measurement_section import (
    DynamicMeasurementSection,
)


class MeasurementForm(QWidget):

    measurementSaved = Signal(dict)

    # Back to measurement list
    backRequested = Signal()

    def __init__(self, parent=None):

        super().__init__(parent)

        self.current_customer = None
        self.current_measurement = None

        self.customers = []

        self.setup_ui()
        self.load_customers()

    # ======================================================
    # MAIN UI
    # ======================================================

    def setup_ui(self):

        self.setObjectName(
            "MeasurementForm"
        )

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        main_layout.setSpacing(0)

        # ==================================================
        # HEADER AREA
        # ==================================================

        header_card = QFrame()

        header_card.setObjectName(
            "PageHeader"
        )

        header_layout = QHBoxLayout(
            header_card
        )

        header_layout.setContentsMargins(
            24,
            20,
            24,
            20,
        )

        header_layout.setSpacing(14)

        # --------------------------------------------------
        # TITLE
        # --------------------------------------------------

        title_box = QVBoxLayout()

        title_box.setSpacing(3)

        self.title_label = QLabel(
            "Add New Measurement"
        )

        self.title_label.setObjectName(
            "PageTitle"
        )

        self.subtitle_label = QLabel(
            "Create and manage customer measurements"
        )

        self.subtitle_label.setObjectName(
            "PageSubtitle"
        )

        title_box.addWidget(
            self.title_label
        )

        title_box.addWidget(
            self.subtitle_label
        )

        header_layout.addLayout(
            title_box
        )

        # --------------------------------------------------
        # PUSH BACK BUTTON TO RIGHT
        # --------------------------------------------------

        header_layout.addStretch()

        # --------------------------------------------------
        # BACK BUTTON
        # --------------------------------------------------

        self.back_button = QPushButton(
            "←  Back"
        )

        self.back_button.setCursor(
            Qt.PointingHandCursor
        )

        self.back_button.setMinimumHeight(
            40
        )

        self.back_button.clicked.connect(
            self.on_back_clicked
        )

        header_layout.addWidget(
            self.back_button
        )

        main_layout.addWidget(
            header_card
        )

        # ==================================================
        # MAIN SCROLL
        # ==================================================

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setFrameShape(
            QFrame.NoFrame
        )

        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        content = QWidget()

        content.setObjectName(
            "MeasurementContent"
        )

        content_layout = QVBoxLayout(
            content
        )

        content_layout.setContentsMargins(
            24,
            20,
            24,
            30,
        )

        content_layout.setSpacing(
            18
        )

        # ==================================================
        # CUSTOMER + PREVIOUS MEASUREMENTS
        # ==================================================

        top_layout = QHBoxLayout()

        top_layout.setSpacing(
            18
        )

        # ==================================================
        # CUSTOMER CARD
        # ==================================================

        customer_card = QFrame()

        customer_card.setObjectName(
            "Card"
        )

        customer_card.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        )

        customer_layout = QVBoxLayout(
            customer_card
        )

        customer_layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        customer_layout.setSpacing(
            12
        )

        # Card title
        customer_title = QLabel(
            "Customer"
        )

        customer_title.setObjectName(
            "CardTitle"
        )

        customer_layout.addWidget(
            customer_title
        )

        # Card subtitle
        customer_subtitle = QLabel(
            "Select the customer for this measurement"
        )

        customer_subtitle.setObjectName(
            "CardSubtitle"
        )

        customer_layout.addWidget(
            customer_subtitle
        )

        # Customer combo
        self.customer_combo = QComboBox()

        self.customer_combo.setEditable(
            True
        )

        self.customer_combo.setPlaceholderText(
            "Search customer..."
        )

        self.customer_combo.setMinimumHeight(
            42
        )

        self.customer_combo.currentIndexChanged.connect(
            self.customer_changed
        )

        customer_layout.addWidget(
            self.customer_combo
        )

        # Customer info
        self.customer_info = QLabel(
            "No customer selected"
        )

        self.customer_info.setObjectName(
            "InfoBox"
        )

        self.customer_info.setWordWrap(
            True
        )

        customer_layout.addWidget(
            self.customer_info
        )

        top_layout.addWidget(
            customer_card,
            2
        )

        # ==================================================
        # PREVIOUS MEASUREMENTS CARD
        # ==================================================

        previous_card = QFrame()

        previous_card.setObjectName(
            "Card"
        )

        previous_layout = QVBoxLayout(
            previous_card
        )

        previous_layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        previous_layout.setSpacing(
            12
        )

        previous_title = QLabel(
            "Previous Measurements"
        )

        previous_title.setObjectName(
            "CardTitle"
        )

        previous_layout.addWidget(
            previous_title
        )

        previous_subtitle = QLabel(
            "Select an existing measurement to edit"
        )

        previous_subtitle.setObjectName(
            "CardSubtitle"
        )

        previous_layout.addWidget(
            previous_subtitle
        )

        self.previous_list = QListWidget()

        self.previous_list.setMinimumHeight(
            145
        )

        self.previous_list.itemClicked.connect(
            self.load_previous_measurement
        )

        previous_layout.addWidget(
            self.previous_list,
            1
        )

        top_layout.addWidget(
            previous_card,
            1
        )

        content_layout.addLayout(
            top_layout
        )

        # ==================================================
        # MEASUREMENT INFORMATION
        # ==================================================

        info_card = QFrame()

        info_card.setObjectName(
            "Card"
        )

        info_layout = QVBoxLayout(
            info_card
        )

        info_layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        info_layout.setSpacing(
            16
        )

        info_title = QLabel(
            "Measurement Information"
        )

        info_title.setObjectName(
            "CardTitle"
        )

        info_layout.addWidget(
            info_title
        )

        info_subtitle = QLabel(
            "Give this measurement a name and select the garment type"
        )

        info_subtitle.setObjectName(
            "CardSubtitle"
        )

        info_layout.addWidget(
            info_subtitle
        )

        # --------------------------------------------------
        # GRID
        # --------------------------------------------------

        info_grid = QGridLayout()

        info_grid.setHorizontalSpacing(
            18
        )

        info_grid.setVerticalSpacing(
            8
        )

        # --------------------------------------------------
        # MEASUREMENT NAME
        # --------------------------------------------------

        name_label = QLabel(
            "Measurement Name"
        )

        name_label.setObjectName(
            "FieldLabel"
        )

        self.measurement_name = QLineEdit()

        self.measurement_name.setPlaceholderText(
            "Example: Shirt Regular Fit"
        )

        self.measurement_name.setMinimumHeight(
            42
        )

        info_grid.addWidget(
            name_label,
            0,
            0
        )

        info_grid.addWidget(
            self.measurement_name,
            1,
            0
        )

        # --------------------------------------------------
        # GARMENT
        # --------------------------------------------------

        garment_label = QLabel(
            "Garment"
        )

        garment_label.setObjectName(
            "FieldLabel"
        )

        self.garment_combo = QComboBox()

        self.garment_combo.addItems([
            "Shirt",
            "Pant",
            "Suit",
            "Blazer",
            "Kurta",
            "Sherwani",
        ])

        self.garment_combo.setMinimumHeight(
            42
        )

        self.garment_combo.currentTextChanged.connect(
            self.garment_changed
        )

        info_grid.addWidget(
            garment_label,
            0,
            1
        )

        info_grid.addWidget(
            self.garment_combo,
            1,
            1
        )

        # Equal columns
        info_grid.setColumnStretch(
            0,
            1
        )

        info_grid.setColumnStretch(
            1,
            1
        )

        info_layout.addLayout(
            info_grid
        )

        content_layout.addWidget(
            info_card
        )

        # ==================================================
        # UPPER BODY
        # ==================================================

        self.upper_section = (
            DynamicMeasurementSection(
                "Upper Body",
                MEASUREMENT_FIELDS["upper"],
            )
        )

        content_layout.addWidget(
            self.upper_section
        )

        # ==================================================
        # LOWER BODY
        # ==================================================

        self.lower_section = (
            DynamicMeasurementSection(
                "Lower Body",
                MEASUREMENT_FIELDS["lower"],
            )
        )

        content_layout.addWidget(
            self.lower_section
        )

        # ==================================================
        # EXTRA MEASUREMENTS
        # ==================================================

        self.extra_section = (
            DynamicMeasurementSection(
                "Extra Measurements",
                MEASUREMENT_FIELDS["extra"],
            )
        )

        content_layout.addWidget(
            self.extra_section
        )

        # ==================================================
        # NOTES
        # ==================================================

        notes_card = QFrame()

        notes_card.setObjectName(
            "Card"
        )

        notes_layout = QVBoxLayout(
            notes_card
        )

        notes_layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        notes_layout.setSpacing(
            12
        )

        notes_title = QLabel(
            "Notes & Instructions"
        )

        notes_title.setObjectName(
            "CardTitle"
        )

        notes_layout.addWidget(
            notes_title
        )

        notes_subtitle = QLabel(
            "Add stitching instructions or special fitting requirements"
        )

        notes_subtitle.setObjectName(
            "CardSubtitle"
        )

        notes_layout.addWidget(
            notes_subtitle
        )

        self.notes = QTextEdit()

        self.notes.setPlaceholderText(
            "Enter stitching instructions, "
            "special fitting instructions, etc."
        )

        self.notes.setMinimumHeight(
            120
        )

        notes_layout.addWidget(
            self.notes
        )

        content_layout.addWidget(
            notes_card
        )

        # ==================================================
        # ACTION BAR
        # ==================================================

        button_card = QFrame()

        button_card.setObjectName(
            "Card"
        )

        button_layout = QHBoxLayout(
            button_card
        )

        button_layout.setContentsMargins(
            20,
            16,
            20,
            16,
        )

        button_layout.setSpacing(
            10
        )

        # --------------------------------------------------
        # CLEAR
        # --------------------------------------------------

        self.clear_button = QPushButton(
            "Clear"
        )

        self.clear_button.setMinimumHeight(
            42
        )

        self.clear_button.clicked.connect(
            self.clear_form
        )

        button_layout.addWidget(
            self.clear_button
        )

        button_layout.addStretch()

        # --------------------------------------------------
        # DELETE
        # --------------------------------------------------

        self.delete_button = QPushButton(
            "Delete"
        )

        self.delete_button.setObjectName(
            "Danger"
        )

        self.delete_button.setMinimumHeight(
            42
        )

        self.delete_button.clicked.connect(
            self.delete_current_measurement
        )

        button_layout.addWidget(
            self.delete_button
        )

        # --------------------------------------------------
        # UPDATE
        # --------------------------------------------------

        self.update_button = QPushButton(
            "Update"
        )

        self.update_button.setMinimumHeight(
            42
        )

        self.update_button.clicked.connect(
            self.update_current_measurement
        )

        button_layout.addWidget(
            self.update_button
        )

        # --------------------------------------------------
        # SAVE
        # --------------------------------------------------

        self.save_button = QPushButton(
            "Save Measurement"
        )

        self.save_button.setObjectName(
            "Primary"
        )

        self.save_button.setMinimumHeight(
            42
        )

        self.save_button.clicked.connect(
            self.save_measurement
        )

        button_layout.addWidget(
            self.save_button
        )

        content_layout.addWidget(
            button_card
        )

        content_layout.addStretch()

        # ==================================================
        # SET SCROLL CONTENT
        # ==================================================

        scroll.setWidget(
            content
        )

        main_layout.addWidget(
            scroll,
            1
        )

        # Initial button state
        self.update_button.setEnabled(
            False
        )

        self.delete_button.setEnabled(
            False
        )

    # ======================================================
    # BACK
    # ======================================================

    def on_back_clicked(self):
    
        self.backRequested.emit()

    # ======================================================
    # CUSTOMER
    # ======================================================

    def load_customers(self):

        self.customers = get_all_customers()

        self.customer_combo.blockSignals(
            True
        )

        self.customer_combo.clear()

        for customer in self.customers:

            name = customer.get(
                "name",
                "Unknown",
            )

            mobile = customer.get(
                "mobile",
                "",
            )

            self.customer_combo.addItem(
                f"{name} - {mobile}",
                customer,
            )

        self.customer_combo.blockSignals(
            False
        )

    # ======================================================
    # CUSTOMER CHANGED
    # ======================================================

    def customer_changed(
        self,
        index,
    ):

        if index < 0:
            return

        customer = (
            self.customer_combo.itemData(
                index
            )
        )

        if not customer:
            return

        self.current_customer = customer

        name = customer.get(
            "name",
            "",
        )

        mobile = customer.get(
            "mobile",
            "",
        )

        email = customer.get(
            "email",
            "",
        )

        customer_id = customer.get(
            "id",
            "",
        )

        self.customer_info.setText(
            f"""
            <b style="font-size:15px;">{name}</b><br>
            <span style="color:#94A3B8;">
            Customer ID: {customer_id}<br>
            Mobile: {mobile}<br>
            Email: {email}
            </span>
            """
        )

        self.load_previous_measurements(
            refresh_only=True
        )

        self.clear_measurement_fields(
            keep_customer=True
        )

    # ======================================================
    # PREVIOUS MEASUREMENTS
    # ======================================================

    def load_previous_measurements(
        self,
        refresh_only=False,
    ):

        self.previous_list.clear()

        if not self.current_customer:
            return

        customer_id = (
            self.current_customer.get(
                "id"
            )
        )

        measurements = (
            get_measurements_by_customer(
                customer_id
            )
        )

        for measurement in measurements:

            measurement_name = (
                measurement.get(
                    "measurement_name",
                    "Measurement",
                )
            )

            garment = (
                measurement.get(
                    "garment",
                    "",
                )
            )

            display_name = measurement_name

            if garment:
                display_name = (
                    f"{measurement_name}  •  {garment}"
                )

            item = QListWidgetItem(
                display_name
            )

            item.setData(
                Qt.UserRole,
                measurement
            )

            self.previous_list.addItem(
                item
            )

    # ======================================================
    # LOAD PREVIOUS
    # ======================================================

    def load_previous_measurement(
        self,
        item,
    ):

        measurement = item.data(
            Qt.UserRole
        )

        if not measurement:
            return

        self.current_measurement = (
            measurement
        )

        self.measurement_name.setText(
            measurement.get(
                "measurement_name",
                "",
            )
        )

        garment = measurement.get(
            "garment",
            "",
        )

        if garment:

            garment_index = (
                self.garment_combo.findText(
                    garment
                )
            )

            if garment_index >= 0:

                self.garment_combo.setCurrentIndex(
                    garment_index
                )

        self.upper_section.set_data(
            measurement.get(
                "upper_measurements",
                {},
            )
        )

        self.lower_section.set_data(
            measurement.get(
                "lower_measurements",
                {},
            )
        )

        self.extra_section.set_data(
            measurement.get(
                "extra_measurements",
                {},
            )
        )

        self.notes.setPlainText(
            measurement.get(
                "notes",
                "",
            )
        )

        self.title_label.setText(
            f"Edit Measurement #{measurement.get('id')}"
        )

        self.subtitle_label.setText(
            "Update the selected customer measurement"
        )

        self.update_button.setEnabled(
            True
        )

        self.delete_button.setEnabled(
            True
        )

        self.save_button.setEnabled(
            False
        )

    # ======================================================
    # GARMENT
    # ======================================================

    def garment_changed(
        self,
        garment,
    ):

        if not self.measurement_name.text().strip():

            self.measurement_name.setText(
                f"{garment} Regular Fit"
            )

    # ======================================================
    # GET FORM DATA
    # ======================================================

    def get_form_data(self):

        if not self.current_customer:

            raise ValueError(
                "Please select a customer."
            )

        measurement_name = (
            self.measurement_name.text().strip()
        )

        if not measurement_name:

            raise ValueError(
                "Please enter measurement name."
            )

        return {

            "customer_id":
                self.current_customer["id"],

            "measurement_name":
                measurement_name,

            "upper_measurements":
                self.upper_section.get_data(),

            "lower_measurements":
                self.lower_section.get_data(),

            "extra_measurements":
                self.extra_section.get_data(),

            "notes":
                self.notes.toPlainText().strip(),
        }

    # ======================================================
    # SAVE
    # ======================================================

    def save_measurement(self):

        try:

            data = self.get_form_data()

            measurement = create_measurement(
                data
            )

            self.current_measurement = (
                measurement
            )

            QMessageBox.information(
                self,
                "Success",
                "Measurement saved successfully.",
            )

            self.load_previous_measurements()

            self.measurementSaved.emit(
                measurement
            )

            self.set_edit_mode()

        except ValueError as e:

            QMessageBox.warning(
                self,
                "Validation",
                str(e),
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"Unable to save measurement:\n\n{e}",
            )

    # ======================================================
    # UPDATE
    # ======================================================

    def update_current_measurement(
        self,
    ):

        if not self.current_measurement:

            QMessageBox.warning(
                self,
                "Update",
                "Please select a measurement first.",
            )

            return

        try:

            data = self.get_form_data()

            measurement = update_measurement(
                self.current_measurement["id"],
                data,
            )

            if not measurement:

                QMessageBox.warning(
                    self,
                    "Update",
                    "Measurement not found.",
                )

                return

            self.current_measurement = (
                measurement
            )

            QMessageBox.information(
                self,
                "Success",
                "Measurement updated successfully.",
            )

            self.load_previous_measurements()

            self.measurementSaved.emit(
                measurement
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"Unable to update measurement:\n\n{e}",
            )

    # ======================================================
    # DELETE
    # ======================================================

    def delete_current_measurement(
        self,
    ):

        if not self.current_measurement:

            QMessageBox.warning(
                self,
                "Delete",
                "Please select a measurement first.",
            )

            return

        result = QMessageBox.question(
            self,
            "Delete Measurement",
            "Are you sure you want to delete this measurement?",
            QMessageBox.Yes
            | QMessageBox.No,
        )

        if result != QMessageBox.Yes:
            return

        try:

            success = delete_measurement(
                self.current_measurement["id"]
            )

            if success:

                QMessageBox.information(
                    self,
                    "Deleted",
                    "Measurement deleted successfully.",
                )

                self.clear_measurement_fields()

                self.load_previous_measurements()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"Unable to delete measurement:\n\n{e}",
            )

    # ======================================================
    # CLEAR MEASUREMENT FIELDS
    # ======================================================

    def clear_measurement_fields(
        self,
        keep_customer=True,
    ):

        self.current_measurement = None

        self.measurement_name.clear()

        self.upper_section.clear()

        self.lower_section.clear()

        self.extra_section.clear()

        self.notes.clear()

        self.title_label.setText(
            "Add New Measurement"
        )

        self.subtitle_label.setText(
            "Create and manage customer measurements"
        )

        self.save_button.setEnabled(
            True
        )

        self.update_button.setEnabled(
            False
        )

        self.delete_button.setEnabled(
            False
        )

    # ======================================================
    # CLEAR FORM
    # ======================================================

    def clear_form(self):

        self.clear_measurement_fields()

        self.previous_list.clear()

        if self.current_customer:

            self.load_previous_measurements()

    # ======================================================
    # EDIT MODE
    # ======================================================

    def set_edit_mode(self):

        self.title_label.setText(
            f"Edit Measurement #{self.current_measurement.get('id')}"
            if self.current_measurement
            else "Edit Measurement"
        )

        self.subtitle_label.setText(
            "Update the selected customer measurement"
        )

        self.save_button.setEnabled(
            True
        )

        self.update_button.setEnabled(
            True
        )

        self.delete_button.setEnabled(
            True
        )

