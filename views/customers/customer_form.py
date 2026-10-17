import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

# Imported database helper routines
import data.customer_crud as db

# --- Imported Components ---
from widgets.customer_form.basic_information import BasicInformation
from widgets.customer_form.form_buttons import FormButtons
from widgets.customer_form.photo_card import PhotoCard


class CustomerForm(QWidget):

    customerSaved = Signal(dict)
    customerUpdated = Signal(dict)
    customerDeleted = Signal(dict)

    # BACK BUTTON SIGNAL
    backRequested = Signal()

    def __init__(self, customer_id=None):
        super().__init__()

        self.current_customer_id = customer_id

        self.build_ui()

        # If editing an existing customer
        if customer_id:
            customer_record = db.get_customer_by_id(
                int(customer_id)
            )

            if customer_record:
                self.load_customer(customer_record)

    def build_ui(self):

        self.setObjectName("CustomerForm")


        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            0, 0, 0, 0
        )

        # ======================================================
        # SCROLL AREA
        # ======================================================

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(True)

        self.scroll.setFrameShape(
            QScrollArea.NoFrame
        )

        # ======================================================
        # CONTAINER
        # ======================================================

        self.container = QWidget()

        self.root = QVBoxLayout(
            self.container
        )

        self.root.setContentsMargins(
            20,
            20,
            20,
            20
        )

        self.root.setSpacing(15)

        # ======================================================
        # TOP HEADER
        # ======================================================

        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)

        # ------------------------------------------------------
        # TITLE - LEFT
        # ------------------------------------------------------

        self.title_label = QLabel("Add New Customer")
        self.title_label.setObjectName("PageTitle")

        header_layout.addWidget(
            self.title_label,
            0,
            Qt.AlignVCenter
        )

        # ------------------------------------------------------
        # SPACE
        # ------------------------------------------------------

        header_layout.addStretch()

        # ------------------------------------------------------
        # BACK BUTTON - RIGHT
        # ------------------------------------------------------

        self.back_button = QPushButton("←  Back")

        self.back_button.setCursor(
            Qt.PointingHandCursor
        )

        self.back_button.clicked.connect(
            self.on_back_clicked
        )

        header_layout.addWidget(
            self.back_button,
            0,
            Qt.AlignRight | Qt.AlignVCenter
        )

        self.root.addLayout(
            header_layout
        )

        

        # ======================================================
        # FORM CONTENT
        # ======================================================

        row1 = QHBoxLayout()

        row1.setSpacing(15)

        self.photo_card = PhotoCard()

        self.basic_information = BasicInformation()

        row1.addWidget(
            self.photo_card,
            1
        )

        row1.addWidget(
            self.basic_information,
            3
        )

        self.root.addLayout(
            row1
        )

        # ======================================================
        # FORM BUTTONS
        # ======================================================

        self.form_buttons = FormButtons()

        self.root.addWidget(
            self.form_buttons
        )

        # ======================================================
        # SCROLL
        # ======================================================

        self.scroll.setWidget(
            self.container
        )

        main_layout.addWidget(
            self.scroll
        )

        # ======================================================
        # SIGNALS
        # ======================================================

        self.form_buttons.saveClicked.connect(
            self.save_customer
        )

        self.form_buttons.updateClicked.connect(
            self.update_customer
        )

        self.form_buttons.deleteClicked.connect(
            self.delete_customer
        )

        self.form_buttons.resetClicked.connect(
            self.reset_form
        )

        # Default add mode
        self.form_buttons.add_mode()

    # ==========================================================
    # BACK
    # ==========================================================

    def on_back_clicked(self):

        self.backRequested.emit()

    # ==========================================================
    # MESSAGE
    # ==========================================================

    def show_message(
        self,
        title,
        text,
        icon=QMessageBox.Information
    ):

        msg = QMessageBox(self)

        msg.setIcon(icon)

        msg.setWindowTitle(title)

        msg.setText(text)


        msg.exec()

    # ==========================================================
    # VALIDATE
    # ==========================================================

    def validate_form(self):

        data = (
            self.basic_information
            .get_data()
        )

        if not data.get("name"):

            self.show_message(
                "Error",
                "Customer Name is required.",
                QMessageBox.Warning
            )

            return False

        if (
            not data.get("mobile")
            or len(
                str(
                    data.get("mobile")
                )
            ) != 10
        ):

            self.show_message(
                "Error",
                "Mobile must be 10 digits.",
                QMessageBox.Warning
            )

            return False

        return True

    # ==========================================================
    # SAVE
    # ==========================================================

    def save_customer(self):

        if not self.validate_form():
            return

        form_data = self.get_customer_data()

        saved_customer = db.create_customer(
            form_data
        )

        new_id = saved_customer["id"]

        form_data["id"] = new_id

        self.customerSaved.emit(
            form_data
        )

        self.show_message(
            "Success",
            f"Customer Added Successfully! (ID: {new_id})"
        )

        self.reset_form()

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update_customer(self):

        if not self.current_customer_id:

            self.show_message(
                "Error",
                "No customer selected for update.",
                QMessageBox.Warning
            )

            return

        if not self.validate_form():
            return

        form_data = self.get_customer_data()

        updated_customer = db.update_customer(
            customer_id=int(
                self.current_customer_id
            ),
            data=form_data
        )

        if updated_customer:

            form_data["id"] = (
                self.current_customer_id
            )

            self.customerUpdated.emit(
                form_data
            )

            self.show_message(
                "Success",
                "Customer Details Updated!"
            )

            self.reset_form()

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete_customer(self):

        if self.current_customer_id:

            db.delete_customer(
                int(
                    self.current_customer_id
                )
            )

            self.customerDeleted.emit(
                {
                    "id":
                    self.current_customer_id
                }
            )

            self.show_message(
                "Deleted",
                "Customer Removed!"
            )

            self.reset_form()

    # ==========================================================
    # RESET
    # ==========================================================

    def reset_form(self):

        self.current_customer_id = None

        self.title_label.setText(
            "Add New Customer"
        )

        self.photo_card.clear()

        self.basic_information.clear_form()

        self.form_buttons.add_mode()

    # ==========================================================
    # GET DATA
    # ==========================================================

    def get_customer_data(self):

        data = {
            "id":
            self.current_customer_id
        }

        data.update(
            self.basic_information.get_data()
        )

        data.update(
            self.photo_card.get_data()
        )

        return data

    # ==========================================================
    # LOAD CUSTOMER
    # ==========================================================

    def load_customer(
        self,
        data
    ):

        self.current_customer_id = (
            data.get("id")
        )

        self.title_label.setText(
            f"Edit Customer #{self.current_customer_id}"
        )

        self.basic_information.set_data(
            data
        )

        self.photo_card.set_data(
            data
        )

        self.form_buttons.edit_mode()


# ==============================================================
# MAIN WINDOW
# ==============================================================

class MainWindow(QWidget):

    def __init__(self):

        super().__init__()

        db.init_db()

        self.setWindowTitle(
            "Customer Management System"
        )

        self.resize(
            1200,
            700
        )

        layout = QHBoxLayout(
            self
        )

        # ======================================================
        # LEFT - FORM
        # ======================================================

        self.form = CustomerForm()

        layout.addWidget(
            self.form,
            2
        )

        # ======================================================
        # RIGHT - TABLE
        # ======================================================

        self.table = QTableWidget()

        self.table.setColumnCount(
            4
        )

        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Name",
                "Mobile",
                "Type"
            ]
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )


        layout.addWidget(
            self.table,
            2
        )

        # ======================================================
        # SIGNALS
        # ======================================================

        self.form.customerSaved.connect(
            self.add_customer_to_table
        )

        self.form.customerUpdated.connect(
            self.update_customer_in_table
        )

        self.form.customerDeleted.connect(
            self.delete_customer_from_table
        )

        self.table.cellClicked.connect(
            self.on_table_row_click
        )

        # ======================================================
        # LOAD DATA
        # ======================================================

        self.load_table_data()

    # ==========================================================
    # TABLE DATA
    # ==========================================================

    def load_table_data(self):

        self.table.setRowCount(0)

        records = db.get_all_customers()

        for record in records:

            row = self.table.rowCount()

            self.table.insertRow(
                row
            )

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(record["id"])
                )
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    record["name"]
                )
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    record["mobile"]
                )
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    record.get(
                        "customer_type",
                        ""
                    )
                )
            )

    # ==========================================================
    # ADD TABLE ROW
    # ==========================================================

    def add_customer_to_table(
        self,
        data
    ):

        row = self.table.rowCount()

        self.table.insertRow(
            row
        )

        self.table.setItem(
            row,
            0,
            QTableWidgetItem(
                str(data.get("id"))
            )
        )

        self.table.setItem(
            row,
            1,
            QTableWidgetItem(
                data.get(
                    "name",
                    ""
                )
            )
        )

        self.table.setItem(
            row,
            2,
            QTableWidgetItem(
                data.get(
                    "mobile",
                    ""
                )
            )
        )

        self.table.setItem(
            row,
            3,
            QTableWidgetItem(
                data.get(
                    "customer_type",
                    ""
                )
            )
        )

    # ==========================================================
    # UPDATE TABLE ROW
    # ==========================================================

    def update_customer_in_table(
        self,
        data
    ):

        target_id = str(
            data.get("id")
        )

        for row in range(
            self.table.rowCount()
        ):

            if (
                self.table
                .item(row, 0)
                .text()
                == target_id
            ):

                self.table.setItem(
                    row,
                    1,
                    QTableWidgetItem(
                        data.get(
                            "name",
                            ""
                        )
                    )
                )

                self.table.setItem(
                    row,
                    2,
                    QTableWidgetItem(
                        data.get(
                            "mobile",
                            ""
                        )
                    )
                )

                self.table.setItem(
                    row,
                    3,
                    QTableWidgetItem(
                        data.get(
                            "customer_type",
                            ""
                        )
                    )
                )

                break

    # ==========================================================
    # DELETE TABLE ROW
    # ==========================================================

    def delete_customer_from_table(
        self,
        data
    ):

        target_id = str(
            data.get("id")
        )

        for row in range(
            self.table.rowCount()
        ):

            if (
                self.table
                .item(row, 0)
                .text()
                == target_id
            ):

                self.table.removeRow(
                    row
                )

                break

    # ==========================================================
    # TABLE CLICK
    # ==========================================================

    def on_table_row_click(
        self,
        row,
        column
    ):

        cust_id = int(
            self.table
            .item(row, 0)
            .text()
        )

        customer_record = (
            db.get_customer_by_id(
                cust_id
            )
        )

        if customer_record:

            self.form.load_customer(
                customer_record
            )


# ==============================================================
# RUN
# ==============================================================

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    window = MainWindow()

    window.show()

    sys.exit(
        app.exec()
    )