import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle('发送图片')
        self.initUI()

    def initUI(self):
        self.label1 = QLabel(self)
        self.label1.setText('请选择图片：')
        self.label1.move(20, 10)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setText('未选择图片')
        self.lineEdit.move(20, 40)

        self.btnSelect = QPushButton(self)
        self.btnSelect.setText('选择图片')
        self.btnSelect.move(20, 70)
        self.btnSelect.clicked.connect(self.slotSelect)

        self.btnSend = QPushButton(self)
        self.btnSend.setText('发送图片')
        self.btnSend.move(20, 100)
        self.btnSend.clicked.connect(self.slotSend)

    def slotSelect(self):
        fname, _ = QFileDialog.getOpenFileName(self, '选择图片', '', 'Image Files(*.jpg *.png)')
        self.lineEdit.setText(fname)

    def slotSend(self):
        fname = self.lineEdit.text()
        if fname == '':
            QMessageBox.information(self, '提示', '请先选择图片！')
            return
        pixmap = QPixmap(fname)
        self.label1.setPixmap(pixmap)
        self.label1.resize(pixmap.width(), pixmap.height())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())