from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtCore import Qt
import qtawesome as qta

class DeliveryTable(QFrame):
    def __init__(self):
        super().__init__()
        self.item_widgets = []
        self.build_ui()

    def build_ui(self):
        self.setMinimumWidth(330)
        self.setObjectName("Card")

        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(20, 20, 20, 20)
        self.root.setSpacing(15)

        title = QLabel("Today's Deliveries")
        title.setObjectName("CardTitle")
        self.root.addWidget(title)

        self.items_container = QVBoxLayout()
        self.items_container.setSpacing(12)
        self.root.addLayout(self.items_container)
        self.root.addStretch()

    def update_data(self, deliveries_list):
        for w in self.item_widgets:
            self.items_container.removeWidget(w)
            w.deleteLater()
        self.item_widgets.clear()

        for item in deliveries_list:
            card = QWidget()
            card.setObjectName("InnerPanel")
            row = QHBoxLayout(card)
            row.setContentsMargins(12, 12, 12, 12)
            row.setSpacing(12)

            icon = QLabel()
            icon.setPixmap(qta.icon("fa5s.user", color=item.color).pixmap(25, 25))
            icon.setAlignment(Qt.AlignTop)

            info = QVBoxLayout()
            info.setSpacing(3)

            lbl_customer = QLabel(item.customer)
            lbl_customer.setObjectName("ValueText")

            lbl_dress = QLabel(item.dress)
            lbl_dress.setObjectName("FieldLabel")

            time_row = QHBoxLayout()
            time_icon = QLabel()
            time_icon.setPixmap(qta.icon("fa5s.clock", color="#9CA3AF").pixmap(13, 13))
            lbl_time = QLabel(item.time)
            lbl_time.setObjectName("MutedText")

            time_row.addWidget(time_icon)
            time_row.addWidget(lbl_time)
            time_row.addStretch()

            info.addWidget(lbl_customer)
            info.addWidget(lbl_dress)
            info.addLayout(time_row)

            row.addWidget(icon)
            row.addLayout(info)

            self.items_container.addWidget(card)
            self.item_widgets.append(card)