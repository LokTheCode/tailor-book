import qtawesome as qta
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
        self.setObjectName("FormButtons")
        self.setStyleSheet("""
        QFrame#FormButtons { background:#1F2937; border:1px solid #374151; border-radius:18px; }
        QPushButton { color:white; border:none; border-radius:10px; padding:12px 18px; min-height:45px; font-size:14px; font-weight:600; }
        QPushButton:hover { border:1px solid #60A5FA; }
        QPushButton#Save { background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #3B82F6,stop:1 #8B5CF6); }
        QPushButton#Save:hover { background:#2563EB; }
        QPushButton#Update { background:#10B981; }
        QPushButton#Update:hover { background:#059669; }
        QPushButton#Delete { background:#EF4444; }
        QPushButton#Delete:hover { background:#DC2626; }
        QPushButton#Reset { background:#F59E0B; }
        QPushButton#Reset:hover { background:#D97706; }
        QPushButton#Cancel { background:#6B7280; }
        QPushButton#Cancel:hover { background:#4B5563; }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)

        layout.addStretch()

        self.cancel = QPushButton(" Cancel")
        self.cancel.setObjectName("Cancel")
        self.cancel.setIcon(qta.icon("fa5s.times", color="white"))
        self.cancel.clicked.connect(self.cancelClicked.emit)
        layout.addWidget(self.cancel)

        self.reset = QPushButton(" Reset")
        self.reset.setObjectName("Reset")
        self.reset.setIcon(qta.icon("fa5s.undo", color="white"))
        self.reset.clicked.connect(self.resetClicked.emit)
        layout.addWidget(self.reset)

        self.delete = QPushButton(" Delete")
        self.delete.setObjectName("Delete")
        self.delete.setIcon(qta.icon("fa5s.trash", color="white"))
        self.delete.clicked.connect(self.deleteClicked.emit)
        layout.addWidget(self.delete)

        self.update = QPushButton(" Update")
        self.update.setObjectName("Update")
        self.update.setIcon(qta.icon("fa5s.edit", color="white"))
        self.update.clicked.connect(self.updateClicked.emit)
        layout.addWidget(self.update)

        self.save = QPushButton(" Save Customer")
        self.save.setObjectName("Save")
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