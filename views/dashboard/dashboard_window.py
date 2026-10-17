# views/dashboard/dashboard_window.py

from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtGui import QKeySequence, QShortcut
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
from views.marketing.marketing_page import MarketingPage
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
            "marketing": MarketingPage,
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

        self.allowed = allowed
        self.setup_shortcuts()
        self.setup_daily_backup()

    # ----------------------------------------------------
    # DAILY BACKUP (Settings > Backup)
    # ----------------------------------------------------

    def setup_daily_backup(self):
        # First check shortly after opening, then every 30 minutes
        QTimer.singleShot(60 * 1000, self.run_daily_backup)
        self.backup_timer = QTimer(self)
        self.backup_timer.timeout.connect(self.run_daily_backup)
        self.backup_timer.start(30 * 60 * 1000)

    def run_daily_backup(self):
        """Back up in the background so the app never freezes."""
        import threading
        from services import backup_service

        def work():
            try:
                backup_service.daily_backup_if_due()
            except Exception as error:
                print(f"Daily backup failed: {error}")

        threading.Thread(target=work, daemon=True).start()

    # ----------------------------------------------------
    # KEYBOARD SHORTCUTS (listed in utils/shortcuts.py)
    # ----------------------------------------------------

    # For each page: method names to try for New / Refresh, and the
    # attribute path of its search box
    PAGE_ACTIONS = {
        "customers": ("open_add_customer", "refresh_all_data", "filter.searchName"),
        "measurements": ("open_measurement_form", "load_data", "filter.search"),
        "orders": ("open_new_order", "refresh", "filter.search"),
        "inventory": ("open_add_inventory", "refresh_all_data", "filter.search"),
        "users": ("add_user", "refresh", None),
        "dashboard": (None, "refresh_dashboard", None),
        "reports": (None, "load_report", None),
        "marketing": (None, "shortcut_refresh", None),
        "settings": (None, "load", None),
    }

    def setup_shortcuts(self):

        def add(keys, handler):
            shortcut = QShortcut(QKeySequence(keys), self)
            shortcut.setContext(Qt.ApplicationShortcut)
            shortcut.activated.connect(handler)

        for number, key in enumerate(self.allowed[:9], start=1):
            add(f"Ctrl+{number}", lambda page=key: self.show_page(page))

        add("Ctrl+N", lambda: self.page_action(0))
        add("F5", lambda: self.page_action(1))
        add("Ctrl+F", self.focus_search)
        add("Ctrl+B", self.quick_backup)
        add("Ctrl+Shift+P", self.change_password)
        add("Ctrl+Shift+L", self.logout)
        add("F1", self.show_shortcuts)

    def current_key(self):
        page = self.stack.currentWidget()
        for key, widget in self.pages.items():
            if widget is page:
                return key
        return None

    def page_action(self, index):
        key = self.current_key()
        name = self.PAGE_ACTIONS.get(key, (None, None, None))[index]
        method = getattr(self.pages.get(key), name, None) if name else None
        if callable(method):
            method()

    def focus_search(self):
        key = self.current_key()
        path = self.PAGE_ACTIONS.get(key, (None, None, None))[2]
        target = self.pages.get(key)
        for part in (path or "").split("."):
            target = getattr(target, part, None) if part else None
        if target is not None and hasattr(target, "setFocus"):
            target.setFocus()
            if hasattr(target, "selectAll"):
                target.selectAll()

    def quick_backup(self):
        from services import backup_service
        try:
            path = backup_service.backup_now()
        except Exception as error:
            QMessageBox.critical(self, "Backup failed", str(error))
            return
        QMessageBox.information(self, "Backup", f"Backup saved:\n{path}")

    def show_shortcuts(self):
        from utils.shortcuts import SHORTCUTS
        rows = "".join(
            f"<tr><td style='padding:4px 18px 4px 0'><b>{keys}</b></td><td>{text}</td></tr>"
            for keys, text in SHORTCUTS
        )
        QMessageBox.information(self, "Keyboard shortcuts", f"<table>{rows}</table>")

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
