from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QFrame,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import qtawesome as qta
from data.customer_data import CustomerStatsData

class CustomerStatCard(QFrame):

    def __init__(self, title, value, icon, subtitle, icon_color="#3B82F6"):
        super().__init__()
        self.title_text = title
        self.value_text = value
        self.icon_name = icon
        self.subtitle_text = subtitle
        self.icon_color = icon_color
        self.build_ui()

    def build_ui(self):
        self.setObjectName("StatCard")
        self.setMinimumHeight(135)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        top = QHBoxLayout()
        icon = QLabel()
        icon.setPixmap(qta.icon(self.icon_name, color=self.icon_color).pixmap(24, 24))
        top.addWidget(icon)
        top.addStretch()
        layout.addLayout(top)

        self.lbl_value = QLabel(self.value_text)
        self.lbl_value.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.lbl_value.setStyleSheet("color:white;")
        layout.addWidget(self.lbl_value)

        self.lbl_title = QLabel(self.title_text)
        self.lbl_title.setStyleSheet("color:#D1D5DB; font-size:14px; font-weight:600;")
        layout.addWidget(self.lbl_title)

        self.lbl_subtitle = QLabel(self.subtitle_text)
        self.lbl_subtitle.setStyleSheet("color:#9CA3AF; font-size:12px;")
        layout.addWidget(self.lbl_subtitle)

    def set_data(self, value: str, subtitle: str):
        self.lbl_value.setText(value)
        self.lbl_subtitle.setText(subtitle)


class CustomerStats(QWidget):

    def __init__(self):
        super().__init__()
        self.build_ui()

    def build_ui(self):
        self.setStyleSheet("""
        QFrame#StatCard{
            background:#1F2937;
            border-radius:16px;
            border:2px solid transparent;
        }
        QLabel{
            background: transparent;
        }
        QFrame#StatCard:hover{
            border:2px solid qlineargradient(
                x1:0,y1:0, x2:1,y2:0,
                stop:0 #3B82F6, stop:1 #8B5CF6
            );
            background:#263244;
        }
        """)

        grid = QGridLayout(self)
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(20)
        grid.setContentsMargins(0, 0, 0, 0)

        self.card_total = CustomerStatCard("Total Customers", "0", "fa5s.users", "+0 this month", "#3B82F6")
        self.card_active = CustomerStatCard("Active Customers", "0", "fa5s.user-check", "0% Active", "#10B981")
        self.card_inactive = CustomerStatCard("Inactive", "0", "fa5s.user-times", "Needs follow-up", "#EF4444")
        self.card_vip = CustomerStatCard("VIP Customers", "0", "fa5s.crown", "Premium Members", "#F59E0B")

        grid.addWidget(self.card_total, 0, 0)
        grid.addWidget(self.card_active, 0, 1)
        grid.addWidget(self.card_inactive, 0, 2)
        grid.addWidget(self.card_vip, 0, 3)

    def set_stats(self, stats: CustomerStatsData):
        self.card_total.set_data(f"{stats.total_customers:,}", f"+{stats.new_this_month} this month")
        self.card_active.set_data(f"{stats.active_customers:,}", f"{stats.active_percentage}% Active")
        self.card_inactive.set_data(f"{stats.inactive_customers:,}", "Needs follow-up")
        self.card_vip.set_data(f"{stats.vip_customers:,}", "Premium Members")