# views/dashboard/dashboard_window.py

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QWidget,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QStackedWidget
)

from services.user_service import PAGES, can_open
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
from views.users.user_page import UserPage
from views.users.change_password_dialog import ChangePasswordDialog


class DashboardWindow(QMainWindow):

    # Emitted when the user confirms logout; AppManager shows the login screen
    logoutRequested = Signal()

    def __init__(self, user):
        super().__init__()

        # Logged-in user dict from UserService (id, name, email, role, permissions)
        self.user = user

        self.setWindowTitle("Dev Tailor ERP")
        self.resize(1500, 900)
        self.setMinimumSize(1400, 850)

        self.pages = {}

        self.build_ui()

    # ----------------------------------------------------

    def page_factories(self):
        """Page key -> function that builds that page."""
        return {
            "dashboard": DashboardPage,
            "customers": CustomerPage,
            "measurements": MeasurementPage,
            "orders": OrderPage,
            "inventory": InventoryPage,
            "reports": ReportPage,
            "users": lambda: UserPage(self.user),
            "settings": SettingPage,
        }

    def build_ui(self):

        # ----------------------------------------------------
        # Central Widget
        # ----------------------------------------------------

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Only the pages this user is allowed to open
        allowed = [key for key in PAGES if can_open(self.user, key)]

        # ----------------------------------------------------
        # Sidebar
        # ----------------------------------------------------

        self.sidebar = Sidebar(allowed_pages=allowed)
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
        self.topbar.set_user(self.user)
        right_layout.addWidget(self.topbar)

        # ----------------------------------------------------
        # Stacked Pages (built only for allowed pages)
        # ----------------------------------------------------

        self.stack = QStackedWidget()

        factories = self.page_factories()
        for key in allowed:
            page = factories[key]()
            self.pages[key] = page
            self.stack.addWidget(page)

        if not self.pages:
            empty = QLabel("Your account has no pages assigned.\nAsk your administrator for access.")
            empty.setObjectName("PageSubtitle")
            empty.setWordWrap(True)
            self.stack.addWidget(empty)

        right_layout.addWidget(self.stack)
        root.addWidget(right)

        # ----------------------------------------------------
        # Signals
        # ----------------------------------------------------

        self.sidebar.pageClicked.connect(self.show_page)
        self.sidebar.logoutClicked.connect(self.logout)
        self.topbar.logoutClicked.connect(self.logout)
        self.topbar.changePasswordClicked.connect(self.change_password)

        if allowed:
            self.show_page(allowed[0])

    # ----------------------------------------------------

    def show_page(self, key):

        page = self.pages.get(key)
        if page is None:
            return

        self.stack.setCurrentWidget(page)
        self.sidebar.set_active(key)

    # ----------------------------------------------------

    def change_password(self):
        ChangePasswordDialog(self.user, parent=self).exec()

    def logout(self):

        reply = QMessageBox.question(
            self,
            "Logout",
            "Are you sure you want to log out?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            self.logoutRequested.emit()
