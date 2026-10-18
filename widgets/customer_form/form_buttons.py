import qtawesome as qta
from utils.theme import theme_color
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton


class FormButtons(QFrame):

    saveClicked = Signal()
    updateClicked = Signal()
    deleteClicked = Signal()
    resetClicked = Signal()
    cancelClicked = Signal()

    def __init__(self):
        super().__init__()
        self.build_ui()

    def build_ui(self):
        self.setObjectName("Card")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)

        layout.addStretch()

        self.cancel = QPushButton(" Cancel")
        self.cancel.setIcon(qta.icon("fa5s.times", color=theme_color("text")))
        self.cancel.clicked.connect(self.cancelClicked.emit)
        layout.addWidget(self.cancel)

        self.reset = QPushButton(" Reset")
        self.reset.setObjectName("Warning")
        self.reset.setIcon(qta.icon("fa5s.undo", color="white"))
        self.reset.clicked.connect(self.resetClicked.emit)
        layout.addWidget(self.reset)

        self.delete = QPushButton(" Delete")
        self.delete.setObjectName("Danger")
        self.delete.setIcon(qta.icon("fa5s.trash", color="white"))
        self.delete.clicked.connect(self.deleteClicked.emit)
        layout.addWidget(self.delete)

        self.update = QPushButton(" Update")
        self.update.setObjectName("Success")
        self.update.setIcon(qta.icon("fa5s.edit", color="white"))
        self.update.clicked.connect(self.updateClicked.emit)
        layout.addWidget(self.update)

        self.save = QPushButton(" Save Customer")
        self.save.setObjectName("Primary")
        self.save.setIcon(qta.icon("fa5s.save", color="white"))
        self.save.clicked.connect(self.saveClicked.emit)
        layout.addWidget(self.save)

    def add_mode(self):
        self.save.show()
        self.cancel.show()
        self.reset.show()
        self.update.hide()
        self.delete.hide()

    def edit_mode(self):
        self.save.hide()
        self.cancel.show()
        self.reset.show()
        self.update.show()
        self.delete.show()