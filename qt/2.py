
import sys
import socket
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QObject, pyqtSignal

class ImageSender(QObject):
    signal = pyqtSignal(QPixmap)

    def __init__(self):
        super().__init__()
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send_socket.connect(('127.0.0.1', 9999))

    def send_image(self, image_path):
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            self.send_socket.sendall(image_data)
            self.signal.emit(QPixmap(image_path))

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.image_label = QLabel()
        self.image_label.setFixedSize(200, 200)

        self.browse_button = QPushButton('Browse...')
        self.browse_button.clicked.connect(self.browseImage)

        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.sendImage)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.send_button)
        self.setLayout(layout)

        self.image_sender = ImageSender()
        self.image_sender.signal.connect(self.showImage)

        self.show()

    def browseImage(self):
        image_path, _ = QFileDialog.getOpenFileName(self, 'Select Image', '', 'Images (*.png *.jpg *.jpeg)')
        self.image_label.setPixmap(QPixmap(image_path))

    def sendImage(self):
        self.image_sender.send_image(self.image_label.pixmap().toImage())

    def showImage(self, image):
        self.image_label.setPixmap(image)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())