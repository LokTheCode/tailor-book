import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from database.database import init_db
from database.seed import seed_initial_data

from views.login.login_window import LoginWindow
from views.dashboard.dashboard_window import DashboardWindow


# ==========================================================
# DEVELOPMENT MODE
# ==========================================================
# True  = Open dashboard directly
# False = Show normal login screen
DEV_MODE = True


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
        self.login_window.show()

    # ======================================================
    # DASHBOARD
    # ======================================================

    def show_dashboard(self, admin):
        """Hide login window and open dashboard."""

        if self.login_window:
            self.login_window.close()
            self.login_window = None

        self.dashboard_window = DashboardWindow(
            user=admin
        )

        self.dashboard_window.show()


def apply_stylesheet(app: QApplication, relative_path: str = "assets/styles/style.qss"):
    """Loads and sets the central QSS stylesheet for the application."""
    style_file = Path(__file__).parent / relative_path
    if style_file.exists():
        with open(style_file, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"Warning: Stylesheet file not found at {style_file}")


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

    # Apply central style globally to all windows and widgets
    apply_stylesheet(app, "assets/styles/style.qss")

    manager = AppManager()

    # ======================================================
    # DEVELOPMENT / PRODUCTION
    # ======================================================

    if DEV_MODE:

        # --------------------------------------------------
        # TEST USER
        # --------------------------------------------------
        test_admin = {
            "id": 1,
            "name": "Test Admin",
            "email": "admin@test.com",
            "role": "admin",
        }

        manager.show_dashboard(test_admin)

    else:

        # Normal application flow
        manager.show_login()

    # ======================================================
    # EVENT LOOP
    # ======================================================

    sys.exit(app.exec())


if __name__ == "__main__":
    main()