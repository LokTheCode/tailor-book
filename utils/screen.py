"""Size windows to the PC's screen."""

from PySide6.QtGui import QGuiApplication


def fit_to_screen(window, ratio=0.9, min_width=1024, min_height=640):
    """Size and centre a window on the screen it opens on.

    The normal (not maximised) size is `ratio` of the screen, and the
    minimum size never exceeds the screen, so the window always fits,
    even on a small laptop.
    """
    screen = window.screen() or QGuiApplication.primaryScreen()
    if screen is None:
        return

    area = screen.availableGeometry()  # screen minus the taskbar

    window.setMinimumSize(min(min_width, area.width()), min(min_height, area.height()))

    width = max(window.minimumWidth(), int(area.width() * ratio))
    height = max(window.minimumHeight(), int(area.height() * ratio))
    window.resize(min(width, area.width()), min(height, area.height()))

    frame = window.frameGeometry()
    frame.moveCenter(area.center())
    window.move(frame.topLeft())
