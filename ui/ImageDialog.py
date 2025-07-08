from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel


class ImageDialog(QDialog):
    def __init__(self):
        super().__init__()

    def show_image(self, image_data):
        self.setWindowTitle("查看图片")
        layout = QVBoxLayout(self)

        label = QLabel(self)
        pixmap = None

        if isinstance(image_data, bytes):
            # 如果是二进制数据，尝试加载为 QImage
            qt_image = QImage.fromData(image_data)
            pixmap = QPixmap.fromImage(qt_image)
        elif isinstance(image_data, QImage):
            pixmap = QPixmap.fromImage(image_data)
        elif isinstance(image_data, QPixmap):
            pixmap = image_data

        if pixmap and not pixmap.isNull():
            label.setPixmap(pixmap.scaled(800, 800, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            label.setText("无法加载图片")

        layout.addWidget(label)
        self.setLayout(layout)
        self.show()
