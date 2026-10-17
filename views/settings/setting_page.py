"""Settings: every section saves to the settings table (services/settings_service)."""

import shutil
import sys
import time
from pathlib import Path

from PySide6.QtCore import QUrl, Qt, Signal
from PySide6.QtGui import QDesktopServices, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

import qtawesome as qta

from config import APP_NAME, APP_VERSION
from database.database import DB_PATH
from services import backup_service, notification_service, settings_service
from utils.shortcuts import SHORTCUTS
from utils.theme import ACCENTS, FONT_SCALES, apply_theme

DATA_DIR = Path(DB_PATH).parent
LOGO_DIR = DATA_DIR / "branding"

SECTIONS = [
    ("General", "fa5s.sliders-h"),
    ("Shop Details", "fa5s.store"),
    ("Invoice", "fa5s.file-invoice"),
    ("WhatsApp", "fa5b.whatsapp"),
    ("Email", "fa5s.envelope"),
    ("Notifications", "fa5s.bell"),
    ("Backup", "fa5s.database"),
    ("Measurements", "fa5s.ruler"),
    ("Appearance", "fa5s.palette"),
    ("Shortcuts", "fa5s.keyboard"),
    ("About", "fa5s.info-circle"),
]


class SettingPage(QWidget):

    settingsSaved = Signal()

    def __init__(self):
        super().__init__()

        # setting key -> widget, filled while building the sections
        self.bindings = {}
        self.logo_path = ""

        self.build_ui()
        self.load()

    # ======================================================
    # LAYOUT
    # ======================================================

    def build_ui(self):

        root = QHBoxLayout(self)
        root.setContentsMargins(25, 25, 25, 25)
        root.setSpacing(20)

        # ---------------- Left menu ----------------
        left = QFrame()
        left.setObjectName("Card")
        left.setFixedWidth(230)

        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(14, 16, 14, 16)
        left_layout.setSpacing(10)

        title = QLabel("Settings")
        title.setObjectName("CardTitle")
        left_layout.addWidget(title)

        self.menu = QListWidget()
        for name, icon in SECTIONS:
            self.menu.addItem(name)
            self.menu.item(self.menu.count() - 1).setIcon(qta.icon(icon, color="#D1D5DB"))
        left_layout.addWidget(self.menu)
        root.addWidget(left)

        # ---------------- Right side ----------------
        right = QVBoxLayout()
        right.setSpacing(14)

        self.stack = QStackedWidget()
        builders = {
            "General": self.build_general,
            "Shop Details": self.build_shop,
            "Invoice": self.build_invoice,
            "WhatsApp": self.build_whatsapp,
            "Email": self.build_email,
            "Notifications": self.build_notifications,
            "Backup": self.build_backup,
            "Measurements": self.build_measurements,
            "Appearance": self.build_appearance,
            "Shortcuts": self.build_shortcuts,
            "About": self.build_about,
        }
        for name, _icon in SECTIONS:
            self.stack.addWidget(self._scroll(builders[name]()))

        self.menu.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.menu.setCurrentRow(0)

        right.addWidget(self.stack, 1)

        bottom = QHBoxLayout()
        self.saved_label = QLabel()
        self.saved_label.setObjectName("MutedText")
        bottom.addWidget(self.saved_label, 1)

        reload_button = QPushButton(" Undo changes")
        reload_button.setIcon(qta.icon("fa5s.undo-alt", color="white"))
        reload_button.clicked.connect(self.load)
        bottom.addWidget(reload_button)

        save = QPushButton(" Save Settings")
        save.setObjectName("Primary")
        save.setIcon(qta.icon("fa5s.save", color="white"))
        save.clicked.connect(self.save)
        bottom.addWidget(save)

        right.addLayout(bottom)
        root.addLayout(right, 1)

    def _scroll(self, widget):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setWidget(widget)
        return scroll

    # ---------------- small builders ----------------

    def _section(self, title, subtitle):
        """A page with a heading; returns (page widget, its layout)."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 8, 0)
        layout.setSpacing(16)

        heading = QLabel(title)
        heading.setObjectName("PageTitle")
        layout.addWidget(heading)

        if subtitle:
            sub = QLabel(subtitle)
            sub.setObjectName("PageSubtitle")
            sub.setWordWrap(True)
            layout.addWidget(sub)

        return page, layout

    def _card(self, layout, title=None):
        """A card with a form layout inside; returns the form."""
        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 20, 24, 20)
        card_layout.setSpacing(14)
        if title:
            label = QLabel(title)
            label.setObjectName("CardTitle")
            card_layout.addWidget(label)
        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        card_layout.addLayout(form)
        layout.addWidget(card)
        return form

    def _label(self, text):
        label = QLabel(text)
        label.setObjectName("FieldLabel")
        return label

    def _hint(self, text):
        label = QLabel(text)
        label.setObjectName("MutedText")
        label.setWordWrap(True)
        label.setTextFormat(Qt.RichText)
        label.setOpenExternalLinks(True)
        return label

    def _bind(self, form, key, widget, label):
        self.bindings[key] = widget
        form.addRow(self._label(label), widget)
        return widget

    def _line(self, form, key, label, placeholder="", password=False):
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        if password:
            field.setEchoMode(QLineEdit.Password)
            show = field.addAction(qta.icon("fa5s.eye", color="#9CA3AF"), QLineEdit.TrailingPosition)
            show.triggered.connect(
                lambda: field.setEchoMode(
                    QLineEdit.Normal if field.echoMode() == QLineEdit.Password else QLineEdit.Password
                )
            )
        return self._bind(form, key, field, label)

    def _text(self, form, key, label, height=90):
        field = QTextEdit()
        field.setFixedHeight(height)
        return self._bind(form, key, field, label)

    def _check(self, form, key, text):
        box = QCheckBox(text)
        self.bindings[key] = box
        form.addRow("", box)
        return box

    def _combo(self, form, key, label, options):
        """options: list of text, or list of (label, value)."""
        combo = QComboBox()
        for option in options:
            if isinstance(option, tuple):
                combo.addItem(option[0], option[1])
            else:
                combo.addItem(option, option)
        return self._bind(form, key, combo, label)

    def _spin(self, form, key, label, low, high, suffix=""):
        spin = QSpinBox()
        spin.setRange(low, high)
        spin.setSuffix(suffix)
        return self._bind(form, key, spin, label)

    # ======================================================
    # SECTIONS
    # ======================================================

    def build_general(self):
        page, layout = self._section("General", "Basic preferences for the whole app.")
        form = self._card(layout)
        self._line(form, "currency_symbol", "Currency symbol", "₹")
        self._combo(form, "rows_per_page", "Rows per page", ["10", "25", "50", "100"])
        form.addRow("", self._hint("Rows per page applies to Customers and Measurements the next time the app starts."))
        layout.addStretch()
        return page

    def build_shop(self):
        page, layout = self._section(
            "Shop Details",
            "Used in WhatsApp/email messages ({shop_name}, {shop_phone}, {shop_address}) and on invoices.",
        )
        form = self._card(layout)
        self._line(form, "shop_name", "Shop name", "Dev Tailors")
        self._line(form, "shop_owner", "Owner name")
        self._line(form, "shop_phone", "Phone", "9876543210")
        self._line(form, "shop_email", "Email", "shop@example.com")
        self._text(form, "shop_address", "Address")
        self._line(form, "shop_gstin", "GSTIN", "Optional")

        logo_row = QHBoxLayout()
        self.logo_preview = QLabel("No logo")
        self.logo_preview.setObjectName("InfoBox")
        self.logo_preview.setFixedSize(120, 120)
        self.logo_preview.setAlignment(Qt.AlignCenter)
        logo_row.addWidget(self.logo_preview)

        buttons = QVBoxLayout()
        upload = QPushButton(" Choose Logo")
        upload.setIcon(qta.icon("fa5s.upload", color="white"))
        upload.clicked.connect(self.choose_logo)
        remove = QPushButton(" Remove")
        remove.setIcon(qta.icon("fa5s.trash", color="white"))
        remove.clicked.connect(lambda: self.set_logo(""))
        buttons.addWidget(upload)
        buttons.addWidget(remove)
        buttons.addStretch()
        logo_row.addLayout(buttons)
        logo_row.addStretch()
        form.addRow(self._label("Logo"), logo_row)

        layout.addStretch()
        return page

    def build_invoice(self):
        page, layout = self._section("Invoice", "Numbering, tax and the text printed on invoices.")
        form = self._card(layout, "Numbering & tax")
        self._line(form, "order_prefix", "Order number prefix", "ORD-")
        self._line(form, "invoice_prefix", "Invoice number prefix", "INV-")
        gst = QDoubleSpinBox()
        gst.setRange(0, 100)
        gst.setDecimals(2)
        gst.setSuffix(" %")
        self._bind(form, "default_gst_percent", gst, "Default GST")
        form.addRow("", self._hint("The order prefix is used for new orders, e.g. ORD-0012. "
                                   "Default GST is filled in for each new garment in an order."))

        form = self._card(layout, "Printed invoice")
        self._combo(form, "invoice_paper", "Paper size", ["A4", "Thermal 80mm"])
        self._check(form, "invoice_show_logo", "Show the shop logo")
        self._text(form, "invoice_terms", "Terms & conditions")
        self._line(form, "invoice_footer", "Footer line", "Thank you for your business!")
        layout.addStretch()
        return page

    def build_whatsapp(self):
        page, layout = self._section(
            "WhatsApp (AiSensy)",
            "Send WhatsApp messages to customers through your AiSensy account.",
        )

        steps = QLabel(
            "<b>How to set up</b><br>"
            "1. In <a href='https://app.aisensy.com' style='color:#60A5FA'>AiSensy</a>, create a WhatsApp "
            "template, e.g. <i>Hi {{1}}, your order {{2}} is ready. Balance: {{3}}</i>, and wait for approval.<br>"
            "2. Go to <b>Campaigns → Launch → API Campaign</b>, choose the template and set the campaign "
            "<b>Live</b>.<br>"
            "3. Copy your <b>API key</b> (Manage → API Key) and paste it below.<br>"
            "4. For each message, enter the campaign name and the values for {{1}}, {{2}}… in order, "
            "separated by commas."
        )
        steps.setObjectName("InfoBox")
        steps.setWordWrap(True)
        steps.setOpenExternalLinks(True)
        layout.addWidget(steps)

        form = self._card(layout, "Account")
        self._check(form, "wa_enabled", "Turn on WhatsApp messages")
        self._line(form, "wa_api_key", "AiSensy API key", "Paste your API key", password=True)
        self._line(form, "wa_api_url", "API URL")
        self._line(form, "wa_country_code", "Country code", "+91")
        form.addRow("", self._hint("Leave the API URL as it is unless AiSensy gives you a different one."))

        for event, label in notification_service.EVENTS.items():
            form = self._card(layout, f"Message: {label}")
            self._line(form, f"wa_campaign_{event}", "Campaign name", "e.g. order_ready")
            self._line(form, f"wa_params_{event}", "Template values", "{customer_name}, {order_number}")

        layout.addWidget(self._placeholder_help())

        form = self._card(layout, "Send a test")
        test_row = QHBoxLayout()
        self.wa_test_mobile = QLineEdit()
        self.wa_test_mobile.setPlaceholderText("Your mobile number")
        self.wa_test_event = QComboBox()
        for event, label in notification_service.EVENTS.items():
            self.wa_test_event.addItem(label, event)
        test = QPushButton(" Send Test")
        test.setIcon(qta.icon("fa5b.whatsapp", color="white"))
        test.clicked.connect(self.test_whatsapp)
        test_row.addWidget(self.wa_test_mobile, 2)
        test_row.addWidget(self.wa_test_event, 1)
        test_row.addWidget(test)
        form.addRow(self._label("Send to"), test_row)
        form.addRow("", self._hint("Saves your settings first, then sends that message with sample values."))

        layout.addStretch()
        return page

    def build_email(self):
        page, layout = self._section("Email", "Send emails to customers from your own email account.")

        form = self._card(layout, "Email account (SMTP)")
        self._check(form, "email_enabled", "Turn on email messages")
        self._line(form, "smtp_host", "SMTP server", "smtp.gmail.com")
        self._spin(form, "smtp_port", "Port", 1, 65535)
        self._combo(form, "smtp_security", "Security", ["STARTTLS", "SSL", "None"])
        self._line(form, "smtp_username", "Login (email)", "you@gmail.com")
        self._line(form, "smtp_password", "Password", "App password", password=True)
        self._line(form, "email_from_name", "Sender name", "Shop name if empty")
        self._line(form, "email_from_address", "Sender email", "Login email if empty")
        form.addRow("", self._hint(
            "Gmail: server smtp.gmail.com, port 587, STARTTLS. Turn on 2-Step Verification and create an "
            "<a href='https://myaccount.google.com/apppasswords' style='color:#60A5FA'>App Password</a> "
            "to use here (your normal password won't work)."
        ))

        for event, label in notification_service.EVENTS.items():
            form = self._card(layout, f"Email: {label}")
            self._line(form, f"email_subject_{event}", "Subject")
            self._text(form, f"email_body_{event}", "Message", height=120)

        layout.addWidget(self._placeholder_help())

        form = self._card(layout, "Send a test")
        row = QHBoxLayout()
        self.email_test_to = QLineEdit()
        self.email_test_to.setPlaceholderText("Your email address")
        test = QPushButton(" Send Test Email")
        test.setIcon(qta.icon("fa5s.paper-plane", color="white"))
        test.clicked.connect(self.test_email)
        row.addWidget(self.email_test_to, 1)
        row.addWidget(test)
        form.addRow(self._label("Send to"), row)

        layout.addStretch()
        return page

    def _placeholder_help(self):
        text = ", ".join("{" + p + "}" for p in notification_service.PLACEHOLDERS)
        hint = QLabel(f"<b>Values you can use:</b> {text}")
        hint.setObjectName("InfoBox")
        hint.setWordWrap(True)
        return hint

    def build_notifications(self):
        page, layout = self._section(
            "Notifications",
            "Choose which order updates are sent to customers automatically.",
        )

        card = QFrame()
        card.setObjectName("Card")
        grid = QGridLayout(card)
        grid.setContentsMargins(24, 20, 24, 20)
        grid.setHorizontalSpacing(30)
        grid.setVerticalSpacing(14)

        grid.addWidget(self._label("When"), 0, 0)
        grid.addWidget(self._label("WhatsApp"), 0, 1)
        grid.addWidget(self._label("Email"), 0, 2)

        for row, (event, label) in enumerate(notification_service.EVENTS.items(), start=1):
            grid.addWidget(QLabel(label), row, 0)
            for column, channel in ((1, "wa"), (2, "email")):
                box = QCheckBox()
                self.bindings[f"notify_{event}_{channel}"] = box
                grid.addWidget(box, row, column)

        grid.setColumnStretch(3, 1)
        layout.addWidget(card)

        layout.addWidget(self._hint(
            "Messages are only sent if WhatsApp / Email is turned on in its own section. "
            "Emails go only to customers with an email address. "
            "'Order ready' and 'Order delivered' are sent when an order's status changes to Ready or Delivered. "
            "Every message is listed in Marketing → Message history."
        ))
        layout.addStretch()
        return page

    def build_backup(self):
        page, layout = self._section(
            "Backup",
            "Keep a copy of all customers, orders, measurements, photos and settings.",
        )

        form = self._card(layout, "Backup settings")
        folder_row = QHBoxLayout()
        folder = QLineEdit()
        folder.setPlaceholderText(str(Path.home() / "Documents" / "TailorBackups"))
        self.bindings["backup_folder"] = folder
        browse = QPushButton("Browse")
        browse.clicked.connect(self.choose_backup_folder)
        folder_row.addWidget(folder, 1)
        folder_row.addWidget(browse)
        form.addRow(self._label("Backup folder"), folder_row)
        self._check(form, "backup_on_exit", "Back up automatically when the app closes")
        self._spin(form, "backup_keep", "Keep automatic backups", 1, 100, " latest")
        form.addRow("", self._hint("Tip: choose a folder in Google Drive, OneDrive or a USB drive "
                                   "so you have a copy if this PC fails."))

        form = self._card(layout, "Backup & restore")
        self.last_backup_label = QLabel()
        form.addRow(self._label("Last backup"), self.last_backup_label)

        buttons = QHBoxLayout()
        backup = QPushButton(" Back Up Now")
        backup.setObjectName("Primary")
        backup.setIcon(qta.icon("fa5s.download", color="white"))
        backup.clicked.connect(self.backup_now)
        restore = QPushButton(" Restore from Backup...")
        restore.setIcon(qta.icon("fa5s.upload", color="white"))
        restore.clicked.connect(self.restore_backup)
        open_folder = QPushButton(" Open Backup Folder")
        open_folder.setIcon(qta.icon("fa5s.folder-open", color="white"))
        open_folder.clicked.connect(lambda: self.open_folder(backup_service.backup_folder()))
        buttons.addWidget(backup)
        buttons.addWidget(restore)
        buttons.addWidget(open_folder)
        buttons.addStretch()
        form.addRow("", buttons)

        layout.addStretch()
        return page

    def build_measurements(self):
        page, layout = self._section("Measurements", "Units and garment types for measurement forms.")
        form = self._card(layout)
        self._combo(form, "measurement_unit", "Unit", [("Inches", "inch"), ("Centimetres", "cm")])
        self._line(form, "garment_types", "Garment types", "Shirt, Pant, Suit")
        form.addRow("", self._hint(
            "Separate garment types with commas. Changes show in the measurement form and filter "
            "the next time the app starts."
        ))
        layout.addStretch()
        return page

    def build_appearance(self):
        page, layout = self._section("Appearance", "Colours and text size. Applied as soon as you save.")
        form = self._card(layout)
        self._combo(form, "accent_color", "Accent colour", list(ACCENTS))
        self._combo(form, "font_size", "Text size", list(FONT_SCALES))
        layout.addStretch()
        return page

    def build_shortcuts(self):
        page, layout = self._section("Keyboard Shortcuts", "Work faster without the mouse. Press F1 anywhere to see these.")

        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(12, 12, 12, 12)

        table = QTableWidget(len(SHORTCUTS), 2)
        table.setHorizontalHeaderLabels(["Keys", "What it does"])
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionMode(QTableWidget.NoSelection)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        for row, (keys, description) in enumerate(SHORTCUTS):
            table.setItem(row, 0, QTableWidgetItem(keys))
            table.setItem(row, 1, QTableWidgetItem(description))
        table.setMinimumHeight(40 * (len(SHORTCUTS) + 1))
        card_layout.addWidget(table)

        layout.addWidget(card)
        layout.addStretch()
        return page

    def build_about(self):
        page, layout = self._section("About", "")
        form = self._card(layout, APP_NAME)
        form.addRow(self._label("Version"), QLabel(APP_VERSION))
        form.addRow(self._label("Python"), QLabel(sys.version.split()[0]))

        data_row = QHBoxLayout()
        data_label = QLabel(str(DATA_DIR))
        data_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        data_label.setWordWrap(True)
        open_data = QPushButton("Open")
        open_data.clicked.connect(lambda: self.open_folder(DATA_DIR))
        data_row.addWidget(data_label, 1)
        data_row.addWidget(open_data)
        form.addRow(self._label("Data folder"), data_row)
        form.addRow("", self._hint("Your database (tailor.db), customer photos and logo are stored here."))

        layout.addStretch()
        return page

    # ======================================================
    # LOAD / SAVE
    # ======================================================

    def load(self):
        values = settings_service.get_all()

        for key, widget in self.bindings.items():
            value = values.get(key, "")
            if isinstance(widget, QCheckBox):
                widget.setChecked(str(value).strip().lower() in ("1", "true", "yes", "on"))
            elif isinstance(widget, QComboBox):
                index = widget.findData(value)
                if index < 0:
                    index = widget.findText(value)
                widget.setCurrentIndex(max(0, index))
            elif isinstance(widget, QDoubleSpinBox):
                try:
                    widget.setValue(float(value or 0))
                except ValueError:
                    widget.setValue(0)
            elif isinstance(widget, QSpinBox):
                try:
                    widget.setValue(int(value or 0))
                except ValueError:
                    widget.setValue(widget.minimum())
            elif isinstance(widget, QTextEdit):
                widget.setPlainText(value)
            else:
                widget.setText(value)

        self.set_logo(values.get("shop_logo", ""), store=False)
        self.last_backup_label.setText(values.get("last_backup_at") or "Never")
        self.saved_label.setText("")

    def collect(self):
        values = {}
        for key, widget in self.bindings.items():
            if isinstance(widget, QCheckBox):
                values[key] = widget.isChecked()
            elif isinstance(widget, QComboBox):
                values[key] = widget.currentData() if widget.currentData() is not None else widget.currentText()
            elif isinstance(widget, QDoubleSpinBox):
                values[key] = f"{widget.value():g}"
            elif isinstance(widget, QSpinBox):
                values[key] = str(widget.value())
            elif isinstance(widget, QTextEdit):
                values[key] = widget.toPlainText().strip()
            else:
                values[key] = widget.text().strip()
        values["shop_logo"] = self.logo_path
        return values

    def validate(self, values):
        if values["wa_enabled"] and not values["wa_api_key"]:
            return "WhatsApp is turned on but the AiSensy API key is empty."
        if values["email_enabled"] and not (values["smtp_host"] and values["smtp_username"]):
            return "Email is turned on but the SMTP server or login is empty."
        if not values["shop_name"]:
            return "Shop name can't be empty."
        if not [g for g in values["garment_types"].split(",") if g.strip()]:
            return "Add at least one garment type."
        return None

    def save(self, silent=False):
        values = self.collect()

        problem = self.validate(values)
        if problem:
            QMessageBox.warning(self, "Please check", problem)
            return False

        appearance_before = (settings_service.get("accent_color"), settings_service.get("font_size"))

        settings_service.set_many(values)

        if (values["accent_color"], values["font_size"]) != appearance_before:
            apply_theme(QApplication.instance())

        self.saved_label.setText(f"Saved at {time.strftime('%I:%M %p')}")
        self.settingsSaved.emit()

        if not silent:
            QMessageBox.information(self, "Settings", "Settings saved.")
        return True

    # ======================================================
    # LOGO
    # ======================================================

    def choose_logo(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose Logo", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if path:
            self.set_logo(path, store=True)

    def set_logo(self, path, store=False):
        """Show a logo; when store=True copy it into the app's branding folder."""
        if path and store:
            LOGO_DIR.mkdir(parents=True, exist_ok=True)
            source = Path(path)
            target = LOGO_DIR / f"logo_{int(time.time())}{source.suffix.lower()}"
            shutil.copy2(source, target)
            path = str(target)

        self.logo_path = path if path and Path(path).is_file() else ""

        if self.logo_path:
            pixmap = QPixmap(self.logo_path).scaled(110, 110, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_preview.setPixmap(pixmap)
        else:
            self.logo_preview.clear()
            self.logo_preview.setText("No logo")

    # ======================================================
    # TESTS
    # ======================================================

    def _busy(self, func, *args):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            return func(*args)
        finally:
            QApplication.restoreOverrideCursor()

    def test_whatsapp(self):
        mobile = self.wa_test_mobile.text().strip()
        if len("".join(c for c in mobile if c.isdigit())) < 10:
            QMessageBox.warning(self, "Test", "Enter your mobile number (10 digits).")
            return
        if not self.save(silent=True):
            return
        ok, detail = self._busy(notification_service.test_whatsapp, mobile, self.wa_test_event.currentData())
        if ok:
            QMessageBox.information(self, "WhatsApp test", f"AiSensy accepted the message.\n\n{detail}")
        else:
            QMessageBox.warning(self, "WhatsApp test failed", detail)

    def test_email(self):
        to = self.email_test_to.text().strip()
        if "@" not in to:
            QMessageBox.warning(self, "Test", "Enter the email address to send the test to.")
            return
        if not self.save(silent=True):
            return
        ok, detail = self._busy(notification_service.test_email, to)
        if ok:
            QMessageBox.information(self, "Email test", f"Test email sent to {to}.")
        else:
            QMessageBox.warning(self, "Email test failed", detail)

    # ======================================================
    # BACKUP
    # ======================================================

    def choose_backup_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Choose Backup Folder")
        if folder:
            self.bindings["backup_folder"].setText(folder)

    def backup_now(self):
        if not self.save(silent=True):
            return
        try:
            path = self._busy(backup_service.backup_now)
        except Exception as error:
            QMessageBox.critical(self, "Backup failed", str(error))
            return
        self.last_backup_label.setText(settings_service.get("last_backup_at"))
        QMessageBox.information(self, "Backup", f"Backup saved:\n{path}")

    def restore_backup(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Choose Backup", str(backup_service.backup_folder()), "Backup (*.zip)"
        )
        if not path:
            return

        reply = QMessageBox.warning(
            self,
            "Restore backup",
            "This replaces ALL current data with the backup.\n\n"
            "A safety backup of the current data is made first. The app will close when done; "
            "open it again to continue.\n\nRestore now?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        try:
            safety = self._busy(backup_service.restore, path)
        except backup_service.BackupError as error:
            QMessageBox.warning(self, "Restore failed", str(error))
            return
        except Exception as error:
            QMessageBox.critical(self, "Restore failed", str(error))
            return

        QMessageBox.information(
            self,
            "Restored",
            f"Backup restored. The app will now close; please open it again.\n\n"
            f"Your previous data was saved to:\n{safety}",
        )
        QApplication.instance().setProperty("skipExitBackup", True)
        QApplication.quit()

    def open_folder(self, folder):
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))
