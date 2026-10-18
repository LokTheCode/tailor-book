import qtawesome as qta
from utils.theme import theme_color
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QPainterPath, QPixmap
from PySide6.QtWidgets import QFileDialog, QFrame, QLabel, QPushButton, QVBoxLayout


class PhotoCard(QFrame):

    photoChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self.photo_path = None
        self.build_ui()

    def build_ui(self):
        self.setObjectName("Card")

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(15)

        title = QLabel("Customer Photo")
        title.setObjectName("CardTitle")
        root.addWidget(title)

        self.image = QLabel()
        self.image.setObjectName("Avatar")
        self.image.setFixedSize(140, 140)
        self.image.setAlignment(Qt.AlignCenter)
        self.reset_image_placeholder()
        root.addWidget(self.image, alignment=Qt.AlignCenter)

        upload = QPushButton(" Upload Photo")
        upload.setIcon(qta.icon("fa5s.camera", color=theme_color("text")))
        upload.clicked.connect(self.select_photo)
        root.addWidget(upload)

        remove = QPushButton(" Remove")
        remove.setObjectName("Danger")
        remove.setIcon(qta.icon("fa5s.trash", color="white"))
        remove.clicked.connect(self.remove_photo)
        root.addWidget(remove)

        self.cid_label = QLabel("Customer ID : AUTO")
        self.cid_label.setObjectName("MutedText")
        self.cid_label.setAlignment(Qt.AlignCenter)
        root.addWidget(self.cid_label)

        self.joined_label = QLabel("Joined : New customer")
        self.joined_label.setObjectName("MutedText")
        self.joined_label.setAlignment(Qt.AlignCenter)
        root.addWidget(self.joined_label)

        root.addStretch()

    def reset_image_placeholder(self):
        self.image.setPixmap(qta.icon("fa5s.user-circle", color="#9CA3AF").pixmap(80, 80))

    def select_photo(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select Customer Photo", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if filename:
            self.photo_path = filename
            self.set_photo(filename)
            self.photoChanged.emit(filename)

    def set_photo(self, filename):
        pix = QPixmap(filename)
        if pix.isNull():
            return
        pix = pix.scaled(140, 140, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        rounded = QPixmap(140, 140)
        rounded.fill(Qt.transparent)
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, 140, 140)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pix)
        painter.end()
        self.image.setPixmap(rounded)

    def remove_photo(self):
        self.photo_path = None
        self.reset_image_placeholder()

    def clear(self):
        self.remove_photo()
        self.cid_label.setText("Customer ID : AUTO")
        self.joined_label.setText("Joined : New customer")

    def get_data(self):
        return {"photo_path": self.photo_path}

    def set_data(self, data):
        self.photo_path = data.get("photo_path")
        if self.photo_path:
            self.set_photo(self.photo_path)
        else:
            self.remove_photo()
        if data.get("id"):
            self.cid_label.setText(f"Customer ID : {data['id']}")
        if data.get("created_at"):
            self.joined_label.setText(f"Joined : {data['created_at']}")