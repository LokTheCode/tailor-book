from PySide6.QtWidgets import QWidget, QGridLayout
from widgets.dashboard.stat_card import StatCard

class StatSection(QWidget):
    def __init__(self):
        super().__init__()
        self.cards = []
        self.build_ui()

    def build_ui(self):
        self.setObjectName("StatSection")
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setHorizontalSpacing(20)
        self.grid.setVerticalSpacing(20)

    def update_data(self, cards_data):
        # Clear existing cards
        for card in self.cards:
            self.grid.removeWidget(card)
            card.deleteLater()
        self.cards.clear()

        columns = 3
        for index, data in enumerate(cards_data):
            row = index // columns
            col = index % columns
            card = StatCard(
                title=data[0],
                value=data[1],
                icon=data[2],
                color=data[3],
                trend=data[4]
            )
            self.grid.addWidget(card, row, col)
            self.cards.append(card)

        for col in range(columns):
            self.grid.setColumnStretch(col, 1)