# views/dashboard/dashboard_window.py

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget
)

from widgets.sidebar import Sidebar
from widgets.topbar import TopBar

# Pages
from views.dashboard.dashboard_page import DashboardPage
from views.customers.customer_page import CustomerPage
from views.measurements.measurement_page import MeasurementPage
from views.orders.order_page import OrderPage
from views.inventory.inventory_page import InventoryPage
from views.reports.report_page import ReportPage
from views.settings.setting_page import SettingPage


class DashboardWindow(QMainWindow):

    def __init__(self, user=None):
        super().__init__()

        self.user = user

        self.setWindowTitle("Dev Tailor ERP")
        self.resize(1500, 900)
        self.setMinimumSize(1400, 850)

        self.build_ui()

    def build_ui(self):

        # ----------------------------------------------------
        # Central Widget
        # ----------------------------------------------------

        central = QWidget()

        self.setCentralWidget(central)

        central.setStyleSheet("""
        QWidget{
            background-color:#111827;
            color:white;
        }
        """)

        root = QHBoxLayout(central)

        root.setContentsMargins(0, 0, 0, 0)

        root.setSpacing(0)

        # ----------------------------------------------------
        # Sidebar
        # ----------------------------------------------------

        self.sidebar = Sidebar()

        root.addWidget(self.sidebar)

        # ----------------------------------------------------
        # Right Area
        # ----------------------------------------------------

        right = QWidget()

        right_layout = QVBoxLayout(right)

        right_layout.setContentsMargins(0, 0, 0, 0)

        right_layout.setSpacing(0)

        # ----------------------------------------------------
        # Top Bar
        # ----------------------------------------------------

        self.topbar = TopBar()

        right_layout.addWidget(self.topbar)

        # ----------------------------------------------------
        # Stacked Pages
        # ----------------------------------------------------

        self.stack = QStackedWidget()

        self.dashboard_page = DashboardPage()

        self.customer_page = CustomerPage()

        self.measurement_page = MeasurementPage()

        self.order_page = OrderPage()

        self.inventory_page = InventoryPage()

        self.report_page = ReportPage()

        self.setting_page = SettingPage()

        self.stack.addWidget(self.dashboard_page)

        self.stack.addWidget(self.customer_page)

        self.stack.addWidget(self.measurement_page)

        self.stack.addWidget(self.order_page)

        self.stack.addWidget(self.inventory_page)

        self.stack.addWidget(self.report_page)

        self.stack.addWidget(self.setting_page)

        right_layout.addWidget(self.stack)

        root.addWidget(right)

        # ----------------------------------------------------
        # Sidebar Signals
        # ----------------------------------------------------

        self.sidebar.dashboardClicked.connect(
            lambda: self.change_page(0, "Dashboard")
        )

        self.sidebar.customerClicked.connect(
            lambda: self.change_page(1, "Customers")
        )

        self.sidebar.measurementClicked.connect(
            lambda: self.change_page(2, "Measurements")
        )

        self.sidebar.orderClicked.connect(
            lambda: self.change_page(3, "Orders")
        )

        self.sidebar.inventoryClicked.connect(
            lambda: self.stack.setCurrentWidget(self.inventory_page)
        )

        self.sidebar.reportClicked.connect(
            lambda: self.change_page(5, "Reports")
        )

        self.sidebar.settingClicked.connect(
            lambda: self.change_page(6, "Settings")
        )

    # ----------------------------------------------------

    def change_page(self, index, title):

        self.stack.setCurrentIndex(index)

        # self.topbar.setTitle(title)