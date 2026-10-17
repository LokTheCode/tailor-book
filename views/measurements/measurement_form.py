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
    MeasurementError,
)
from services import settings_service

from widgets.measurement.measurement_fields import (
    MEASUREMENT_FIELDS,
)

from widgets.measurement.dynamic_measurement_section import (
    DynamicMeasurementSection,
)


def unit_label():
    """'inches' or 'cm', from Settings > Measurements."""
    return "cm" if settings_service.get("measurement_unit") == "cm" else "inches"


class MeasurementForm(QWidget):

    measurementSaved = Signal(dict)
    measurementDeleted = Signal()

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

        self.garment_combo.addItems(
            settings_service.get_list("garment_types")
        )

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
                f"Upper Body ({unit_label()})",
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
                f"Lower Body ({unit_label()})",
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
            self.clear_measurement_fields
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
    # CUSTOMERS
    # ======================================================

    def load_customers(self, select_id=None):
        """Fill the customer list (active customers only).

        Called every time the form opens, so customers added since the
        app started are listed too.
        """

        if select_id is None and self.current_customer:
            select_id = self.current_customer.get("id")

        self.customers = get_all_customers()

        self.customer_combo.blockSignals(True)
        self.customer_combo.clear()

        self.customer_combo.addItem("Select a customer...", None)

        for customer in self.customers:
            self.customer_combo.addItem(
                f"{customer.get('name', 'Unknown')} - {customer.get('mobile', '')}",
                customer,
            )

        self.customer_combo.setCurrentIndex(0)
        self.customer_combo.blockSignals(False)

        self.current_customer = None
        self.customer_info.setText("No customer selected")
        self.previous_list.clear()

        if select_id:
            self.select_customer(select_id)

    def select_customer(self, customer_id, customer_fallback=None):
        """Select a customer in the list (adds them if inactive)."""

        for index in range(1, self.customer_combo.count()):
            data = self.customer_combo.itemData(index)
            if data and data.get("id") == customer_id:
                self.customer_combo.setCurrentIndex(index)
                return

        # Inactive customers aren't listed, but their old measurements
        # can still be opened and edited
        if customer_fallback:
            self.customer_combo.addItem(
                f"{customer_fallback.get('name', '')} - {customer_fallback.get('mobile', '')} (inactive)",
                customer_fallback,
            )
            self.customer_combo.setCurrentIndex(self.customer_combo.count() - 1)

    def customer_changed(self, index):

        customer = self.customer_combo.itemData(index) if index >= 0 else None

        self.current_customer = customer

        if not customer:
            self.customer_info.setText("No customer selected")
            self.previous_list.clear()
            return

        self.customer_info.setText(
            f"""
            <b style="font-size:15px;">{customer.get('name', '')}</b><br>
            <span style="color:#94A3B8;">
            Customer ID: {customer.get('id', '')}<br>
            Mobile: {customer.get('mobile', '')}<br>
            Email: {customer.get('email', '') or '-'}
            </span>
            """
        )

        self.load_previous_measurements()

        if not self._loading:
            self.clear_measurement_fields()

    # ======================================================
    # PREVIOUS MEASUREMENTS
    # ======================================================

    def load_previous_measurements(self, refresh_only=False):

        self.previous_list.clear()

        if not self.current_customer:
            return

        for measurement in get_measurements_by_customer(self.current_customer.get("id")):

            text = measurement.get("measurement_name") or "Measurement"
            if measurement.get("garment"):
                text = f"{text}  •  {measurement['garment']}"
            if measurement.get("updated_at"):
                text = f"{text}  •  {measurement['updated_at'].strftime('%d %b %Y')}"

            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, measurement)
            self.previous_list.addItem(item)

    def load_previous_measurement(self, item):
        """Click an old measurement to edit it."""

        measurement = item.data(Qt.UserRole)
        if measurement:
            self.fill_fields(measurement)

    # ======================================================
    # OPEN FOR NEW / EDIT (called by the measurement page)
    # ======================================================

    def open_new(self):
        """Blank form, with a fresh customer list."""

        self.load_customers(select_id=None)
        self.clear_measurement_fields()
        self.customer_combo.setFocus()

    def load_measurement(self, measurement):
        """Open an existing measurement for editing."""

        self._loading = True
        try:
            self.load_customers(select_id=None)
            self.select_customer(
                measurement.get("customer_id"),
                customer_fallback={
                    "id": measurement.get("customer_id"),
                    "name": measurement.get("customer_name", ""),
                    "mobile": measurement.get("mobile", ""),
                },
            )
        finally:
            self._loading = False

        self.fill_fields(measurement)

    def fill_fields(self, measurement):

        self.current_measurement = measurement

        self.measurement_name.setText(measurement.get("measurement_name", ""))

        garment = measurement.get("garment") or ""
        if garment:
            index = self.garment_combo.findText(garment)
            if index < 0:
                self.garment_combo.addItem(garment)
                index = self.garment_combo.count() - 1
            self.garment_combo.blockSignals(True)
            self.garment_combo.setCurrentIndex(index)
            self.garment_combo.blockSignals(False)

        self.upper_section.set_data(measurement.get("upper_measurements", {}))
        self.lower_section.set_data(measurement.get("lower_measurements", {}))
        self.extra_section.set_data(measurement.get("extra_measurements", {}))
        self.notes.setPlainText(measurement.get("notes", ""))

        self.set_edit_mode()

    # ======================================================
    # GARMENT
    # ======================================================

    def garment_changed(self, garment):

        # Suggest a name only while it's empty or still a suggestion
        current = self.measurement_name.text().strip()
        if not current or current.endswith(" Regular Fit"):
            self.measurement_name.setText(f"{garment} Regular Fit")

    # ======================================================
    # FORM DATA
    # ======================================================

    def get_form_data(self):

        return {
            "customer_id": (self.current_customer or {}).get("id"),
            "measurement_name": self.measurement_name.text().strip(),
            "garment": self.garment_combo.currentText(),
            "upper_measurements": self.upper_section.get_data(),
            "lower_measurements": self.lower_section.get_data(),
            "extra_measurements": self.extra_section.get_data(),
            "notes": self.notes.toPlainText().strip(),
        }

    # ======================================================
    # SAVE (new)
    # ======================================================

    def save_measurement(self):

        try:
            measurement = create_measurement(self.get_form_data())
        except MeasurementError as error:
            QMessageBox.warning(self, "Please check", str(error))
            return
        except Exception as error:
            QMessageBox.critical(self, "Error", f"Unable to save measurement:\n\n{error}")
            return

        QMessageBox.information(self, "Saved", "Measurement saved.")
        self.measurementSaved.emit(measurement)

    # ======================================================
    # UPDATE
    # ======================================================

    def update_current_measurement(self):

        if not self.current_measurement:
            QMessageBox.warning(self, "Update", "Select a measurement first.")
            return

        try:
            measurement = update_measurement(self.current_measurement["id"], self.get_form_data())
        except MeasurementError as error:
            QMessageBox.warning(self, "Please check", str(error))
            return
        except Exception as error:
            QMessageBox.critical(self, "Error", f"Unable to update measurement:\n\n{error}")
            return

        if not measurement:
            QMessageBox.warning(self, "Update", "This measurement no longer exists.")
            return

        QMessageBox.information(self, "Updated", "Measurement updated.")
        self.measurementSaved.emit(measurement)

    # ======================================================
    # DELETE
    # ======================================================

    def delete_current_measurement(self):

        if not self.current_measurement:
            QMessageBox.warning(self, "Delete", "Select a measurement first.")
            return

        name = self.current_measurement.get("measurement_name", "this measurement")

        result = QMessageBox.question(
            self,
            "Delete Measurement",
            f"Delete '{name}'? This can't be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if result != QMessageBox.Yes:
            return

        try:
            delete_measurement(self.current_measurement["id"])
        except Exception as error:
            QMessageBox.critical(self, "Error", f"Unable to delete measurement:\n\n{error}")
            return

        QMessageBox.information(self, "Deleted", "Measurement deleted.")
        self.measurementDeleted.emit()

    # ======================================================
    # CLEAR
    # ======================================================

    def clear_measurement_fields(self, keep_customer=True):

        self.current_measurement = None

        self.measurement_name.clear()
        self.upper_section.clear()
        self.lower_section.clear()
        self.extra_section.clear()
        self.notes.clear()

        if self.garment_combo.count():
            self.garment_combo.blockSignals(True)
            self.garment_combo.setCurrentIndex(0)
            self.garment_combo.blockSignals(False)
            self.measurement_name.setText(f"{self.garment_combo.currentText()} Regular Fit")

        self.title_label.setText("Add New Measurement")
        self.subtitle_label.setText("Create and manage customer measurements")

        self.save_button.setText("Save Measurement")
        self.save_button.setEnabled(True)
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    def clear_form(self):
        """Kept for older callers: same as opening a new form."""
        self.open_new()

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
            "Update this measurement, or Save as New to keep both versions"
        )

        # Save stays enabled: it saves the values as a new measurement
        self.save_button.setText("Save as New")
        self.save_button.setEnabled(True)
        self.update_button.setEnabled(True)
        self.delete_button.setEnabled(True)
