import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QFileDialog, QLabel
from PyQt5.QtCore import pyqtSlot,QThread,QObject, pyqtSignal
import socket
import os

class MyThread(QThread):
    trigger = pyqtSignal(str)
    def __init__(self,ip,port):
        super().__init__()
        self.ip = ip
        self.port = port
    def run(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.ip,self.port))

    def send_pic(self,pic_path):
        file_name = os.path.basename(pic_path)
        file_size = os.stat(pic_path).st_size
        self.client.send(file_name.encode('utf-8'))
        self.client.send(str(file_size).encode('utf-8'))
        with open(pic_path,'rb') as f:
            m = f.read(1024)
            while m:
                self.client.send(m)
                m = f.read(1024)
        self.trigger.emit('图片发送成功')

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = '发送照片'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()
        #创建线程
        self.thread = MyThread('127.0.0.1',5000)
        self.thread.trigger.connect(self.show_message)
        self.thread.start()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.btn = QPushButton('选择图片', self)
        self.btn.move(20,20)
        self.btn.clicked.connect(self.get_pic)
        self.label = QLabel('未选择图片',self)
        self.label.move(20,50)
        self.show()

    @pyqtSlot()
    def get_pic(self):
        file_name,_ = QFileDialog.getOpenFileName(self, '选择图片', '', 'PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;All Files (*)')
        if file_name:
            self.label.setText(file_name)
            self.thread.send_pic(file_name)
    def show_message(self,message):
        self.label.setText(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())