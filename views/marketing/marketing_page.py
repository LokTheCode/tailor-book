from PySide6.QtCore import QThread, Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QProgressBar,
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

from data.customer_crud import CUSTOMER_TYPES
from services import notification_service as notify
from services import settings_service


class SendWorker(QThread):
    """Sends marketing messages one by one without freezing the window."""

    progress = Signal(int, int, int)  # done, sent, failed
    finishedSending = Signal(int, int, bool)  # sent, failed, cancelled

    def __init__(self, customers, channel, campaign, params, subject, body):
        super().__init__()
        self.customers = customers
        self.channel = channel
        self.campaign = campaign
        self.params = params
        self.subject = subject
        self.body = body
        self.cancelled = False

    def run(self):
        sent = failed = 0
        for index, customer in enumerate(self.customers, start=1):
            if self.cancelled:
                break
            ok, _detail = notify.send_marketing_one(
                customer, self.channel,
                campaign=self.campaign, params=self.params,
                subject=self.subject, body=self.body,
            )
            sent += ok
            failed += not ok
            self.progress.emit(index, sent, failed)
        self.finishedSending.emit(sent, failed, self.cancelled)


class MarketingPage(QWidget):
    """Send WhatsApp (AiSensy) or email campaigns to chosen customers."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.audience_list = []
        self.build_ui()
        self.update_channel()
        self.refresh_audience()
        self.refresh_logs()

    # ======================================================
    # UI
    # ======================================================

    def build_ui(self):

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        outer.addWidget(scroll)

        content = QWidget()
        scroll.setWidget(content)

        root = QVBoxLayout(content)
        root.setContentsMargins(30, 25, 30, 25)
        root.setSpacing(20)

        # ---------------- Header ----------------
        title = QLabel("Marketing")
        title.setObjectName("PageTitle")
        subtitle = QLabel("Send offers and updates to your customers on WhatsApp (AiSensy) or email.")
        subtitle.setObjectName("PageSubtitle")
        root.addWidget(title)
        root.addWidget(subtitle)

        self.setup_hint = QLabel()
        self.setup_hint.setObjectName("InfoBox")
        self.setup_hint.setWordWrap(True)
        root.addWidget(self.setup_hint)

        # ---------------- Compose card ----------------
        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 22, 24, 22)
        card_layout.setSpacing(14)

        card_title = QLabel("New message")
        card_title.setObjectName("CardTitle")
        card_layout.addWidget(card_title)

        form = QFormLayout()
        form.setSpacing(12)

        self.channel = QComboBox()
        self.channel.addItem("WhatsApp (AiSensy)", "whatsapp")
        self.channel.addItem("Email", "email")
        self.channel.currentIndexChanged.connect(self.update_channel)
        form.addRow(self._label("Send by"), self.channel)

        audience_row = QHBoxLayout()
        self.audience_kind = QComboBox()
        self.audience_kind.addItems(notify.AUDIENCES)
        self.audience_kind.currentIndexChanged.connect(self.audience_kind_changed)
        self.customer_type = QComboBox()
        self.customer_type.addItems(CUSTOMER_TYPES)
        self.customer_type.currentIndexChanged.connect(self.refresh_audience)
        self.days = QSpinBox()
        self.days.setRange(1, 3650)
        self.days.setValue(30)
        self.days.setSuffix(" days")
        self.days.valueChanged.connect(self.refresh_audience)
        audience_row.addWidget(self.audience_kind, 2)
        audience_row.addWidget(self.customer_type, 1)
        audience_row.addWidget(self.days, 1)
        form.addRow(self._label("Send to"), audience_row)

        self.audience_count = QLabel()
        self.audience_count.setObjectName("MutedText")
        form.addRow("", self.audience_count)

        card_layout.addLayout(form)

        # Channel-specific fields
        self.fields_stack = QStackedWidget()

        wa_box = QWidget()
        wa_form = QFormLayout(wa_box)
        wa_form.setContentsMargins(0, 0, 0, 0)
        wa_form.setSpacing(12)
        self.campaign = QLineEdit()
        self.campaign.setPlaceholderText("Name of a Live API campaign in AiSensy, e.g. diwali_offer")
        self.params = QLineEdit()
        self.params.setPlaceholderText("Values for {{1}}, {{2}}... e.g. {customer_name}, 20%")
        wa_form.addRow(self._label("AiSensy campaign"), self.campaign)
        wa_form.addRow(self._label("Template values"), self.params)
        self.fields_stack.addWidget(wa_box)

        email_box = QWidget()
        email_form = QFormLayout(email_box)
        email_form.setContentsMargins(0, 0, 0, 0)
        email_form.setSpacing(12)
        self.subject = QLineEdit()
        self.subject.setPlaceholderText("e.g. Festive offer at {shop_name}")
        self.body = QTextEdit()
        self.body.setPlaceholderText("Dear {customer_name},\n\n...")
        self.body.setFixedHeight(140)
        email_form.addRow(self._label("Subject"), self.subject)
        email_form.addRow(self._label("Message"), self.body)
        self.fields_stack.addWidget(email_box)

        card_layout.addWidget(self.fields_stack)

        hint = QLabel(
            "You can use: " + ", ".join("{" + p + "}" for p in
                                       ["customer_name", "mobile", "shop_name", "shop_phone"])
        )
        hint.setObjectName("MutedText")
        hint.setWordWrap(True)
        card_layout.addWidget(hint)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        card_layout.addWidget(self.progress)

        buttons = QHBoxLayout()
        self.status_label = QLabel()
        self.status_label.setObjectName("MutedText")
        buttons.addWidget(self.status_label, 1)

        self.cancel_button = QPushButton("Stop")
        self.cancel_button.setVisible(False)
        self.cancel_button.clicked.connect(self.cancel_sending)
        buttons.addWidget(self.cancel_button)

        self.send_button = QPushButton(" Send")
        self.send_button.setObjectName("Primary")
        self.send_button.setIcon(qta.icon("fa5s.paper-plane", color="white"))
        self.send_button.clicked.connect(self.send)
        buttons.addWidget(self.send_button)
        card_layout.addLayout(buttons)

        root.addWidget(card)

        # ---------------- History card ----------------
        history = QFrame()
        history.setObjectName("Card")
        history_layout = QVBoxLayout(history)
        history_layout.setContentsMargins(16, 16, 16, 16)
        history_layout.setSpacing(10)

        history_header = QHBoxLayout()
        history_title = QLabel("Message history")
        history_title.setObjectName("CardTitle")
        history_header.addWidget(history_title)
        history_header.addStretch()
        refresh = QPushButton(" Refresh")
        refresh.setIcon(qta.icon("fa5s.sync-alt", color="white"))
        refresh.clicked.connect(self.refresh_logs)
        history_header.addWidget(refresh)
        history_layout.addLayout(history_header)

        hint = QLabel("Order notifications, marketing and test messages. Hover a row to see the full reply.")
        hint.setObjectName("MutedText")
        history_layout.addWidget(hint)

        self.logs = QTableWidget(0, 6)
        self.logs.setHorizontalHeaderLabels(["Time", "Customer", "Type", "Channel", "To", "Status"])
        self.logs.verticalHeader().setVisible(False)
        self.logs.setEditTriggers(QTableWidget.NoEditTriggers)
        self.logs.setSelectionBehavior(QTableWidget.SelectRows)
        self.logs.setAlternatingRowColors(True)
        self.logs.setMinimumHeight(320)
        self.logs.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        history_layout.addWidget(self.logs)

        root.addWidget(history)

    def _label(self, text):
        label = QLabel(text)
        label.setObjectName("FieldLabel")
        return label

    # ======================================================
    # STATE
    # ======================================================

    def current_channel(self):
        return self.channel.currentData()

    def update_channel(self, *_):
        channel = self.current_channel()
        self.fields_stack.setCurrentIndex(0 if channel == "whatsapp" else 1)

        if channel == "whatsapp" and not settings_service.get_bool("wa_enabled"):
            self.setup_hint.setText("WhatsApp is turned off. Set up AiSensy in Settings > WhatsApp first.")
            self.setup_hint.setVisible(True)
        elif channel == "email" and not settings_service.get_bool("email_enabled"):
            self.setup_hint.setText("Email is turned off. Set up your email account in Settings > Email first.")
            self.setup_hint.setVisible(True)
        else:
            self.setup_hint.setVisible(False)

        self.refresh_audience()

    def audience_kind_changed(self, *_):
        kind = self.audience_kind.currentText()
        self.customer_type.setVisible(kind == "Customer type")
        self.days.setVisible("N days" in kind)
        self.refresh_audience()

    def refresh_audience(self, *_):
        if not hasattr(self, "audience_count"):
            return
        self.audience_list = notify.audience(
            self.audience_kind.currentText(),
            customer_type=self.customer_type.currentText(),
            days=self.days.value(),
            channel=self.current_channel(),
        )
        need = "an email address" if self.current_channel() == "email" else "a mobile number"
        count = len(self.audience_list)
        self.audience_count.setText(f"{count} customer{'s' if count != 1 else ''} with {need}")
        self.send_button.setText(f" Send to {count}")
        self.send_button.setEnabled(count > 0 and self.worker is None)

    def refresh_logs(self):
        rows = notify.recent_logs()
        self.logs.setRowCount(len(rows))
        for r, log in enumerate(rows):
            values = [
                log["time"].strftime("%d %b %Y %I:%M %p") if log["time"] else "-",
                log["customer"],
                log["event"],
                "WhatsApp" if log["channel"] == "whatsapp" else "Email",
                log["recipient"],
                "Sent" if log["status"] == "sent" else "Failed",
            ]
            for c, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setToolTip(log["detail"] or value)
                if c == 5:
                    item.setForeground(QColor("#10B981" if log["status"] == "sent" else "#F87171"))
                self.logs.setItem(r, c, item)

    # ======================================================
    # SEND
    # ======================================================

    def send(self):
        channel = self.current_channel()

        if channel == "whatsapp":
            if not settings_service.get_bool("wa_enabled"):
                QMessageBox.warning(self, "WhatsApp is off", "Turn on WhatsApp in Settings > WhatsApp first.")
                return
            if not self.campaign.text().strip():
                QMessageBox.warning(self, "Campaign needed", "Enter the AiSensy campaign name.")
                return
        else:
            if not settings_service.get_bool("email_enabled"):
                QMessageBox.warning(self, "Email is off", "Turn on email in Settings > Email first.")
                return
            if not self.subject.text().strip() or not self.body.toPlainText().strip():
                QMessageBox.warning(self, "Message needed", "Enter a subject and a message.")
                return

        count = len(self.audience_list)
        reply = QMessageBox.question(
            self, "Send message",
            f"Send this {'WhatsApp' if channel == 'whatsapp' else 'email'} to {count} customers?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        self.worker = SendWorker(
            list(self.audience_list), channel,
            self.campaign.text(), self.params.text(),
            self.subject.text(), self.body.toPlainText(),
        )
        self.worker.progress.connect(self.on_progress)
        self.worker.finishedSending.connect(self.on_finished)

        self.progress.setRange(0, count)
        self.progress.setValue(0)
        self.progress.setVisible(True)
        self.cancel_button.setVisible(True)
        self.send_button.setEnabled(False)
        self.status_label.setText("Sending...")

        self.worker.start()

    def cancel_sending(self):
        if self.worker:
            self.worker.cancelled = True
            self.status_label.setText("Stopping after the current message...")

    def on_progress(self, done, sent, failed):
        self.progress.setValue(done)
        self.status_label.setText(f"Sent {sent}, failed {failed} of {self.progress.maximum()}")

    def on_finished(self, sent, failed, cancelled):
        self.worker.wait()
        self.worker = None
        self.progress.setVisible(False)
        self.cancel_button.setVisible(False)
        self.refresh_audience()
        self.refresh_logs()

        text = f"Sent {sent}, failed {failed}."
        if cancelled:
            text = "Stopped. " + text
        if failed:
            text += "\n\nSee Message history for the reasons (hover a Failed row)."
        self.status_label.setText(text.split("\n")[0])
        QMessageBox.information(self, "Done", text)

    # Shortcut hooks (see DashboardWindow)
    def shortcut_refresh(self):
        self.refresh_audience()
        self.refresh_logs()
