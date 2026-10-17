"""One place for how list tables look and behave.

Every list page calls setup_table() so all tables have the same row
height, always show room for at least 10 rows (so the pagination bar
stays in the same place), select whole rows, and never cut off the
edit / delete buttons.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableWidget

ROW_HEIGHT = 46
HEADER_HEIGHT = 44


def setup_table(table: QTableWidget, visible_rows: int = 10, stretch: bool = True) -> None:
    rows = table.verticalHeader()
    rows.setVisible(False)
    rows.setDefaultSectionSize(ROW_HEIGHT)
    rows.setMinimumSectionSize(ROW_HEIGHT)
    rows.setSectionResizeMode(QHeaderView.Fixed)

    header = table.horizontalHeader()
    header.setFixedHeight(HEADER_HEIGHT)
    header.setHighlightSections(False)
    header.setDefaultAlignment(Qt.AlignCenter | Qt.AlignVCenter)
    if stretch:
        header.setSectionResizeMode(QHeaderView.Stretch)

    table.setShowGrid(False)
    table.setAlternatingRowColors(True)
    table.setWordWrap(False)
    table.setTextElideMode(Qt.ElideRight)
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    table.setSelectionMode(QAbstractItemView.SingleSelection)
    table.setFocusPolicy(Qt.NoFocus)
    table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
    table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
    table.setMouseTracking(True)

    # Room for `visible_rows` rows even when there are fewer records
    frame = table.frameWidth() * 2
    table.setMinimumHeight(HEADER_HEIGHT + ROW_HEIGHT * visible_rows + frame + 2)


def fit_column(table: QTableWidget, column: int, width: int) -> None:
    """Give a column (e.g. Actions) a fixed width."""
    table.horizontalHeader().setSectionResizeMode(column, QHeaderView.Fixed)
    table.setColumnWidth(column, width)


def fit_to_contents(table: QTableWidget, *columns: int) -> None:
    for column in columns:
        table.horizontalHeader().setSectionResizeMode(column, QHeaderView.ResizeToContents)
