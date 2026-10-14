from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea
from PySide6.QtCore import Qt, QTimer

from data.dashboard_data import DashboardDataService, DashboardData
from widgets.dashboard.stats_section import StatSection
from widgets.dashboard.recent_order_table import RecentOrderTable
from widgets.dashboard.delivery_table import DeliveryTable
from widgets.dashboard.quick_action import QuickAction
from widgets.dashboard.revenue_chart import RevenueChart
from widgets.dashboard.order_status_chart import OrderStatusChart


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.build_ui()
        self.setup_timer()
        self.refresh_dashboard()

    def build_ui(self):
        self.setObjectName("DashboardPage")
        self.setStyleSheet("""
        QWidget#DashboardPage { background:#111827; border:none; }
        QScrollArea#DashboardScroll { background:#111827; border:none; }
        QScrollArea#DashboardScroll > QWidget { background:#111827; border:none; }
        QLabel#Welcome { color:white; font-size:30px; font-weight:700; }
        QLabel#Subtitle { color:#9CA3AF; font-size:14px; }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setObjectName("DashboardScroll")
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFrameShape(QScrollArea.NoFrame)
        main_layout.addWidget(scroll)

        content = QWidget()
        content.setObjectName("DashboardContent")
        scroll.setWidget(content)
        content.setStyleSheet("QWidget#DashboardContent { background:#111827; border:none; }")

        root = QVBoxLayout(content)
        root.setContentsMargins(30, 25, 30, 25)
        root.setSpacing(25)

        title = QLabel("Welcome Back, Admin 👋")
        title.setObjectName("Welcome")

        subtitle = QLabel("Here's what's happening in your tailoring shop today.")
        subtitle.setObjectName("Subtitle")
        root.addWidget(title)
        root.addWidget(subtitle)

        # Dashboard Sub-components
        statsChart = QHBoxLayout()
        statsChart.setSpacing(20)
        self.stat_section = StatSection()
        self.order_status_chart = OrderStatusChart()
        statsChart.addWidget(self.stat_section, 2)
        statsChart.addWidget(self.order_status_chart, 1)
        root.addLayout(statsChart)

        charts = QHBoxLayout()
        charts.setSpacing(20)
        self.revenue_chart = RevenueChart()
        self.deliveries = DeliveryTable()
        charts.addWidget(self.revenue_chart, 2)
        charts.addWidget(self.deliveries, 1)
        root.addLayout(charts)

        tables = QHBoxLayout()
        tables.setSpacing(20)
        self.recent_orders = RecentOrderTable()
        tables.addWidget(self.recent_orders)
        root.addLayout(tables)

        # self.quick_actions = QuickAction()
        # # Bind QuickAction events if needed
        # root.addWidget(self.quick_actions)
        # root.addStretch()

    def setup_timer(self):
        # Auto-refresh dashboard data every 30 seconds
        self.refresh_timer = QTimer(self)
        self.refresh_timer.setInterval(30000)
        self.refresh_timer.timeout.connect(self.refresh_dashboard)
        self.refresh_timer.start()

    def refresh_dashboard(self):

        data: DashboardData = DashboardDataService.fetch_latest()

        # Update all UI parts asynchronously
        self.stat_section.update_data(data.stats)
        self.recent_orders.update_data(data.recent_orders)
        self.deliveries.update_data(data.deliveries)
        
        # Determine current total revenue display text dynamically
        rev_total_str = data.stats[2][1] if len(data.stats) > 2 else "₹ 0"
        self.revenue_chart.update_data(data.revenue_series, total_text=rev_total_str)
        
        self.order_status_chart.update_data(data.order_status)