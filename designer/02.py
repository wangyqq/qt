import sys
import socket
import time
import struct
import os
import threading
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, \
    QListWidgetItem, QPushButton, QTextEdit, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

class Chat(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(600, 600)
        self.setWindowTitle('Chat')

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # 图片
        self.label_pic = QLabel()
        self.label_pic.setFixedSize(150, 150)
        self.label_pic.setStyleSheet('QLabel{background:white;}')
        self.main_layout.addWidget(self.label_pic)

        # 显示聊天内容
        self.list_chat = QListWidget()
        self.main_layout.addWidget(self.list_chat)

        # 输入框
        self.edit_chat = QTextEdit()
        self.main_layout.addWidget(self.edit_chat)

        # 布局
        self.btn_layout = QHBoxLayout()
        self.main_layout.addLayout(self.btn_layout)

        # 发送按钮
        self.btn_send = QPushButton('发送')
        self.btn_send.clicked.connect(self.slot_send)
        self.btn_layout.addWidget(self.btn_send)

        # 选择图片
        self.btn_select = QPushButton('选择图片')
        self.btn_select.clicked.connect(self.slot_select_pic)
        self.btn_layout.addWidget(self.btn_select)

        self.show()

    # 选择图片
    def slot_select_pic(self):
        self.pic_path, _ = QFileDialog.getOpenFileName(self, '选择图片', '', 'Image Files(*.jpg *.png)')
        jpg = QPixmap(self.pic_path).scaled(self.label_pic.width(), self.label_pic.height())
        self.label_pic.setPixmap(jpg)

    # 发送图片
    def slot_send(self):
        # 发送文字
        if self.edit_chat.toPlainText():
            self.list_chat.addItem(self.edit_chat.toPlainText())
            self.edit_chat.clear()

        # 发送图片
        if self.pic_path:
            self.send_pic()
            self.pic_path = ''
            self.label_pic.clear()
            self.label_pic.setStyleSheet('QLabel{background:white;}')

    # 发送图片
    def send_pic(self):
        # 打开图片
        with open(self.pic_path, 'rb') as f:
            img_data = f.read()

        # 发送图片大小
        len_str = struct.pack('i', len(img_data))
        self.sock.send(len_str)

        # 发送图片
        self.sock.send(img_data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat = Chat()
    sys.exit(app.exec_())