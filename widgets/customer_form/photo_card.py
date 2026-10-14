import qtawesome as qta
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
        self.setObjectName("PhotoCard")
        self.setStyleSheet("""
        QFrame#PhotoCard {
            background: #1F2937;
            border: 1px solid #374151;
            border-radius: 18px;
        }
        QLabel { color: white; }
        QLabel#Title { background: transparent; font-size: 18px; font-weight: bold; }
        QLabel#CustomerId { background: transparent; color: #9CA3AF; font-size: 13px; }
        QLabel#Image { background: #111827; border: 3px solid #3B82F6; border-radius: 70px; }
        QPushButton {
            background: #293548; color: white; border: none;
            border-radius: 10px; padding: 10px; font-weight: 600;
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3B82F6, stop:1 #8B5CF6);
        }
        QPushButton#Remove { background: #DC2626; }
        QPushButton#Remove:hover { background: #B91C1C; }
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(15)

        title = QLabel("Customer Photo")
        title.setObjectName("Title")
        root.addWidget(title)

        self.image = QLabel()
        self.image.setObjectName("Image")
        self.image.setFixedSize(140, 140)
        self.image.setAlignment(Qt.AlignCenter)
        self.reset_image_placeholder()
        root.addWidget(self.image, alignment=Qt.AlignCenter)

        upload = QPushButton(" Upload Photo")
        upload.setIcon(qta.icon("fa5s.camera", color="white"))
        upload.clicked.connect(self.select_photo)
        root.addWidget(upload)

        remove = QPushButton(" Remove")
        remove.setObjectName("Remove")
        remove.setIcon(qta.icon("fa5s.trash", color="white"))
        remove.clicked.connect(self.remove_photo)
        root.addWidget(remove)

        self.cid_label = QLabel("Customer ID : AUTO")
        self.cid_label.setObjectName("CustomerId")
        self.cid_label.setAlignment(Qt.AlignCenter)
        root.addWidget(self.cid_label)

        joined = QLabel("Joined : Today")
        joined.setObjectName("CustomerId")
        joined.setAlignment(Qt.AlignCenter)
        root.addWidget(joined)

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

    def get_data(self):
        return {"photo_path": self.photo_path}

    def set_data(self, data):
        self.photo_path = data.get("photo_path")
        if self.photo_path:
            self.set_photo(self.photo_path)
        else:
            self.remove_photo()
        if "id" in data:
            self.cid_label.setText(f"Customer ID : {data['id']}")