import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('PyQt5 Image')

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        self.select_button = QPushButton('选择图片')
        self.select_button.clicked.connect(self.select_image)

        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.select_button)

        self.setLayout(vbox)
        self.show()

    def select_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, '选择图片', '', 'Image Files(*.jpg *.png)')
        self.image_label.setPixmap(QPixmap(fname))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())