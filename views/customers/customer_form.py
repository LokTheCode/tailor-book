from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

import data.customer_crud as db
from data.customer_crud import CustomerError, CustomerHasOrders

from widgets.customer_form.basic_information import BasicInformation
from widgets.customer_form.form_buttons import FormButtons
from widgets.customer_form.photo_card import PhotoCard


class CustomerForm(QWidget):
    """Add a new customer, or edit / delete an existing one."""

    customerSaved = Signal(dict)
    customerUpdated = Signal(dict)
    customerDeleted = Signal(dict)

    # Back / Cancel: return to the customer list without saving
    backRequested = Signal()

    def __init__(self, customer_id=None):
        super().__init__()

        self.current_customer_id = customer_id
        self.original_record = None

        self.build_ui()

        if customer_id:
            record = db.get_customer_by_id(int(customer_id))
            if record:
                self.load_customer(record)
            else:
                self.show_message(
                    "Not found",
                    f"Customer #{customer_id} no longer exists.",
                    QMessageBox.Warning,
                )
                self.current_customer_id = None

    # ==========================================================
    # UI
    # ==========================================================

    def build_ui(self):

        self.setObjectName("CustomerForm")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.NoFrame)

        self.container = QWidget()

        self.root = QVBoxLayout(self.container)
        self.root.setContentsMargins(20, 20, 20, 20)
        self.root.setSpacing(15)

        # ------------------------------------------------------
        # Header: title left, back button right
        # ------------------------------------------------------

        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)

        self.title_label = QLabel("Add New Customer")
        self.title_label.setObjectName("PageTitle")
        header_layout.addWidget(self.title_label, 0, Qt.AlignVCenter)

        header_layout.addStretch()

        self.back_button = QPushButton("←  Back")
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.clicked.connect(self.backRequested.emit)
        header_layout.addWidget(self.back_button, 0, Qt.AlignRight | Qt.AlignVCenter)

        self.root.addLayout(header_layout)

        # ------------------------------------------------------
        # Photo + details
        # ------------------------------------------------------

        row1 = QHBoxLayout()
        row1.setSpacing(15)

        self.photo_card = PhotoCard()
        self.basic_information = BasicInformation()

        row1.addWidget(self.photo_card, 1)
        row1.addWidget(self.basic_information, 3)

        self.root.addLayout(row1)

        # ------------------------------------------------------
        # Buttons
        # ------------------------------------------------------

        self.form_buttons = FormButtons()
        self.root.addWidget(self.form_buttons)

        self.root.addStretch()

        self.scroll.setWidget(self.container)
        main_layout.addWidget(self.scroll)

        self.form_buttons.saveClicked.connect(self.save_customer)
        self.form_buttons.updateClicked.connect(self.update_customer)
        self.form_buttons.deleteClicked.connect(self.delete_customer)
        self.form_buttons.resetClicked.connect(self.reset_form)
        self.form_buttons.cancelClicked.connect(self.backRequested.emit)

        self.form_buttons.add_mode()

    # ==========================================================
    # MESSAGES
    # ==========================================================

    def show_message(self, title, text, icon=QMessageBox.Information):
        msg = QMessageBox(self)
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec()

    def show_error(self, error):
        self.show_message("Please check", str(error), QMessageBox.Warning)

    # ==========================================================
    # SAVE (new customer)
    # ==========================================================

    def save_customer(self):

        form_data = self.get_customer_data()

        try:
            saved = db.create_customer(form_data)
        except CustomerError as error:
            self.show_error(error)
            return

        self.show_message("Saved", f"Customer {saved['name']} added (ID {saved['id']}).")
        self.customerSaved.emit(saved)

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update_customer(self):

        if not self.current_customer_id:
            return

        form_data = self.get_customer_data()

        try:
            updated = db.update_customer(int(self.current_customer_id), form_data)
        except CustomerError as error:
            self.show_error(error)
            return

        if updated is None:
            self.show_message("Not found", "This customer no longer exists.", QMessageBox.Warning)
            return

        self.show_message("Updated", f"Customer {updated['name']} updated.")
        self.customerUpdated.emit(updated)

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete_customer(self):

        if not self.current_customer_id:
            return

        customer_id = int(self.current_customer_id)
        name = self.basic_information.name.text() or f"#{customer_id}"

        reply = QMessageBox.question(
            self,
            "Delete customer",
            f"Delete {name} and all their measurements?\n\nThis can't be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        try:
            db.delete_customer(customer_id)
        except CustomerHasOrders as error:
            reply = QMessageBox.question(
                self,
                "Customer has orders",
                f"{error}\n\nDeactivate {name} now?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes,
            )
            if reply != QMessageBox.Yes:
                return
            db.set_customer_active(customer_id, False)
            self.show_message("Deactivated", f"{name} has been deactivated.")
            self.customerUpdated.emit({"id": customer_id})
            return

        self.show_message("Deleted", f"{name} has been deleted.")
        self.customerDeleted.emit({"id": customer_id})

    # ==========================================================
    # RESET
    # ==========================================================

    def reset_form(self):
        """Add mode: clear everything. Edit mode: undo unsaved changes."""

        if self.current_customer_id and self.original_record:
            self.load_customer(self.original_record)
            return

        self.current_customer_id = None
        self.title_label.setText("Add New Customer")
        self.photo_card.clear()
        self.basic_information.clear_form()
        self.form_buttons.add_mode()
        self.basic_information.name.setFocus()

    # ==========================================================
    # DATA
    # ==========================================================

    def get_customer_data(self):
        data = {}
        data.update(self.basic_information.get_data())
        data.update(self.photo_card.get_data())
        return data

    def load_customer(self, data):

        self.original_record = dict(data)
        self.current_customer_id = data.get("id")

        self.title_label.setText(f"Edit Customer #{self.current_customer_id}")

        self.basic_information.set_data(data)
        self.photo_card.set_data(data)

        self.form_buttons.edit_mode()
