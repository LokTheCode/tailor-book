import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from database.database import init_db
from database.seed import seed_initial_data

from views.login.login_window import LoginWindow
from views.dashboard.dashboard_window import DashboardWindow
from services.user_service import SUPER_ADMIN_EMAIL, UserService
from models.admin import Admin
from database.database import SessionLocal
from sqlalchemy import func
from utils.theme import apply_theme


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

    def connect_dashboard(self, window):
        window.logoutRequested.connect(self.logout)
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

    app = QApplication(sys.argv)

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

        # Normal application flow
        manager.show_login()

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