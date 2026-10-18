import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMessageBox

from database.database import init_db
from database.seed import seed_initial_data

from views.login.login_window import LoginWindow
from views.dashboard.dashboard_window import DashboardWindow
from services.user_service import SUPER_ADMIN_EMAIL, UserService
from models.admin import Admin
from database.database import SessionLocal
from sqlalchemy import func
from utils.theme import apply_theme
from utils.brand import app_icon
from config import APP_NAME, APP_PUBLISHER, APP_VERSION
from services import license_service
from utils.background import run_in_background


# ==========================================================
# DEVELOPMENT MODE
# ==========================================================
# True  = Skip the login screen and open as the super admin
# False = Show normal login screen
DEV_MODE = False


class AppManager:
    """Manages window switching across the application lifetime."""

    def __init__(self):
        self.login_window = None
        self.dashboard_window = None
        self.activation_window = None
        self.update_info = None
        self.checked_online = False

    # ======================================================
    # LICENSE
    # ======================================================

    def start(self):
        """Activation screen first if this PC has no license, then login."""
        if license_service.required() and not license_service.current():
            self.show_activation()
        else:
            self.show_login()

    def show_activation(self, message=""):
        from views.license.activation_window import ActivationWindow

        self.activation_window = ActivationWindow(message)
        self.activation_window.activated.connect(self.on_activated)
        self.activation_window.showMaximized()

    def on_activated(self, license_):
        window = self.activation_window
        self.show_login()
        if window:
            window.close()
            window.deleteLater()
        self.activation_window = None

    def run_online_checks(self):
        """Once per run: weekly license check and 'is there a newer version?'."""
        if self.checked_online or not license_service.server_url():
            return
        self.checked_online = True

        if license_service.current() and license_service.check_due():
            # Offline / server down: keep working, try again next start
            run_in_background(license_service.check, self.on_license_checked, lambda _e: None)

        run_in_background(license_service.latest, self.on_latest, lambda _e: None)

    def on_license_checked(self, status):
        if status == "active":
            return
        message = license_service.STATUS_MESSAGES.get(status, "This license is no longer valid.")
        parent = self.dashboard_window or self.login_window
        QMessageBox.warning(parent, "License", message + "\n\nPlease enter a valid license key to keep using the app.")
        self.show_activation(message)
        for attr in ("dashboard_window", "login_window"):
            window = getattr(self, attr)
            if window:
                window.close()
                window.deleteLater()
                setattr(self, attr, None)

    def on_latest(self, info):
        if info and license_service.is_newer(info.get("version")):
            self.update_info = info
            if self.dashboard_window:
                self.dashboard_window.topbar.show_update(info["version"])

    def show_update(self):
        from views.license.update_dialog import UpdateDialog

        if self.update_info:
            UpdateDialog(self.update_info, self.dashboard_window).exec()

    # ======================================================
    # LOGIN
    # ======================================================

    def show_login(self):
        self.login_window = LoginWindow()
        self.login_window.login_successful.connect(
            self.show_dashboard
        )
        # Open full screen on whatever PC / screen size it runs on
        self.login_window.showMaximized()

    # ======================================================
    # DASHBOARD
    # ======================================================

    def show_dashboard(self, user):
        """Hide login window and open dashboard for this user dict."""

        if self.login_window:
            self.login_window.close()
            self.login_window = None

        self.dashboard_window = DashboardWindow(
            user=user
        )

        self.connect_dashboard(self.dashboard_window)

        # Open full screen on whatever PC / screen size it runs on
        self.dashboard_window.showMaximized()

        # A few seconds after opening, so start-up stays quick
        QTimer.singleShot(3000, self.run_online_checks)

    def connect_dashboard(self, window):
        window.logoutRequested.connect(self.logout)
        window.topbar.updateClicked.connect(self.show_update)
        if self.update_info:
            window.topbar.show_update(self.update_info["version"])
        # Wait until Settings has finished saving before rebuilding
        window.appearanceChanged.connect(
            lambda: QTimer.singleShot(0, self.rebuild_dashboard)
        )

    # ======================================================
    # THEME CHANGE
    # ======================================================

    def rebuild_dashboard(self):
        """Re-create the main window in the new theme, back on Appearance."""

        old = self.dashboard_window
        if old is None:
            return

        user = UserService.get(old.user["id"]) or old.user

        new = DashboardWindow(user=user)
        self.connect_dashboard(new)

        new.restoreGeometry(old.saveGeometry())
        new.show_page("settings")
        new.pages["settings"].open_section("Appearance")
        new.pages["settings"].saved_label.setText("Theme applied")

        if old.isMaximized():
            new.showMaximized()
        else:
            new.show()

        # Show the new window before closing the old one, so the app
        # never has zero windows open
        self.dashboard_window = new
        old.close()
        old.deleteLater()

    # ======================================================
    # LOGOUT
    # ======================================================

    def logout(self):
        """Close the dashboard and go back to the login screen."""

        # Show login first so the app never has zero windows open
        # (Qt would otherwise quit when the last window closes)
        self.show_login()

        if self.dashboard_window:
            self.dashboard_window.close()
            self.dashboard_window.deleteLater()
            self.dashboard_window = None


def main():

    # ======================================================
    # DATABASE
    # ======================================================

    init_db()
    seed_initial_data()

    # ======================================================
    # APPLICATION
    # ======================================================

    # Windows: show the Tailor Book icon in the taskbar (not Python's)
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("TailorBook.Desktop")
        except Exception:
            pass

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName(APP_PUBLISHER)
    app.setWindowIcon(app_icon())

    # One shared theme (assets/styles/theme.qss) for every window
    apply_theme(app)

    manager = AppManager()

    # ======================================================
    # DEVELOPMENT / PRODUCTION
    # ======================================================

    if DEV_MODE:

        # Open directly as the real super admin account
        db = SessionLocal()
        try:
            admin_id = (
                db.query(Admin.id)
                .filter(func.lower(Admin.email) == SUPER_ADMIN_EMAIL.lower())
                .scalar()
            )
        finally:
            db.close()

        manager.show_dashboard(UserService.get(admin_id))

    else:

        # Normal application flow: activation (if needed), then login
        manager.start()

    # ======================================================
    # EVENT LOOP
    # ======================================================

    exit_code = app.exec()

    # Settings > Backup: "Back up automatically when the app closes"
    # (skipped right after a restore, which closes the app on purpose)
    if not app.property("skipExitBackup"):
        try:
            from services import backup_service, settings_service
            if settings_service.get_bool("backup_on_exit"):
                backup_service.backup_now(auto=True)
        except Exception as error:
            print(f"Automatic backup failed: {error}")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()