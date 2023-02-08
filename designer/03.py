import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle("打开图片")

        # 创建按钮
        self.btn = QPushButton("选择图片", self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        # 创建标签
        self.label = QLabel(self)
        self.label.setGeometry(20, 60, 300, 300)

        self.show()

    def showDialog(self):
        # 打开文件对话框
        fname = QFileDialog.getOpenFileName(self, '打开文件', './')

        # 设置图片
        self.label.setPixmap(QPixmap(fname[0]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())