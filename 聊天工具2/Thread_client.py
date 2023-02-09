import json
import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication

from chat import Ui_MainWindow
import sys
import threading
from socket import *
import base64
import struct

HOST = '127.0.0.1'
PORT = 9999
ADDR = (HOST, PORT)
data_message = []

class Test_win(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Test_win, self).__init__()
        self.setupUi(self)

        self.Button_send.clicked.connect(self.Send)
        self.Button_pic.clicked.connect(self.pic)
        self.Button_data.clicked.connect(self.msg)
        self.pushButton.clicked.connect(self.Delete)
        self.user = ['All-MESS', 'User']
        self.comboBox.addItems(self.user)

        self.tcpCliSock = socket(AF_INET, SOCK_STREAM)
        self.tcpCliSock.connect(ADDR)

        self.textEdit3.append("客户端")
        t1 = threading.Thread(target=self.Get)
        t1.start()

    def get_all(self, data_Dame, data_name, pic, zwj_data):

        if not data_Dame: # 判断文件是否是文件夹
            tu_b = base64.b64decode(pic)
            with open(data_name, 'wb') as fp:
                fp.write(tu_b)
            self.textEdit2.append("单个文件接收成功！")
        else:
            if not zwj_data:
                if not os.path.exists(data_Dame):
                    os.makedirs(data_Dame, exist_ok=True)
                tu_b = base64.b64decode(pic)
                with open(data_Dame + "/" + data_name, 'wb') as fp:
                    fp.write(tu_b)
                self.textEdit2.append("文件接收成功！")
            else:
                if not os.path.exists(data_Dame + zwj_data):
                    os.makedirs((data_Dame + zwj_data), exist_ok=True)

                tu_b = base64.b64decode(pic)
                with open(data_Dame + zwj_data + "/" + data_name, 'wb') as fp:
                    fp.write(tu_b)
                self.textEdit2.append("文件接收成功!")

    def send_all(self, data):
        dataTosend = json.dumps(data, ensure_ascii=False).encode("utf-8")
        msg_len = struct.pack('i', len(dataTosend)) # 压缩文件长度
        self.tcpCliSock.send(msg_len)
        self.tcpCliSock.send(dataTosend)
    def Delete(self):
        self.textEdit3.setPlainText(" ")

    def Get(self):
        while True:
            data = self.tcpCliSock.recv(4) # 接收4个字节
            print(data)

            # 解码要接收多大的数据
            len_data = struct.unpack('i', data)[0]
            Data = self.tcpCliSock.recv(len_data)
            dic = eval(Data.decode('utf-8'))
            user = dic['user']
            get_name = dic['get_name']

            if Data.decode('utf-8') != '':
                if len(Data) < 200:
                    text = dic['text'] # 消息内容
                    list_user = dic['list_user']

                    if get_name == 'All-MESS':
                        if user == 'Root':

                            new_user = []
                            for i in list_user:
                                if i != data_message[0]:
                                    new_user.append(i)

                            self.comboBox.clear()
                            self.user = ['All-MESS', 'User'] + new_user
                            self.comboBox.addItems(self.user)

                        else:
                            self.textEdit3.append(user + ' :' + text)
                    else:
                        user = dic['user']
                        text = dic['text']
                        self.textEdit3.append(user + ' :' + text)
                else:
                    data_name = dic['data_name']
                    pic = dic['file']
                    zwj_data = dic['zwj_data']
                    data_Dame = dic['data_Dame']

                    if user != data_message[0]:
                        if get_name == 'All-MESS':
                            self.get_all(data_Dame, data_name, pic, zwj_data)
                        else:
                            self.get_all(data_Dame, data_name, pic, zwj_data)

    def Send(self):
        # 获取用户输入
        self.text = self.textEdit.toPlainText()
        data_message.append(self.text)
        text = self.comboBox.currentText()

        if text == "User":
            self.textEdit3.append(data_message[0] + ' :' + self.text)
            text1 = {'user': data_message[0] , "get_name": text, 'text': self.text, 'list_user': ''}
            self.send_all(text1)

        elif text == 'ALL-MESS':
            text1 = {'user': data_message[0], "get_name": "ALL-MESS", 'text': self.text, 'list_user':''}
            self.send_all(text1)

        else:
            self.textEdit3.append(data_message[0] + ' :' + self.text)
            text1 = {'user': data_message[0], "get_name": text, 'text': self.text, 'list_user':''}
            self.send_all(text1)

        self.textEdit.setPlainText("")

        if self.textEdit == 'Q':
            app = QApplication.instance()
            app.quit()

    def msg(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "C:/")

        lis = self.recursion_dir_all_file(directory)
        list_data = list(set(lis))
        print(list_data)

        # 文件夹名称
        for i in range(len(directory)):
            if directory[-i] == "/":
                c = len(directory)-i+1
                data_Dame = directory[c:]
                break

        # 当循环对当前目录下的文件进行一次发送
        for i in list_data:
            # 获取文件名
            for c in range(len(i)):
                if i[-c] == "/":
                    c = len(i) - c + 1
                    data_name = i[c:]
                    break

            # 子文件夹路径
            zwj_data = i[len(directory):-len(data_name) - 1]
            with open(i, 'rb') as fp:
                tu = base64.b64decode(fp.read())
            myFile = tu.decode("utf-8")
            T1 = self.comboBox.currentText()
            data = {'user': data_message[0], "get_name": T1, 'zwj_data':zwj_data, "data_Dame": data_Dame, "data_name": data_name, "file":myFile}
            self.send_all(data)
            self.textEdit2.append("文件已发送！")

    def pic(self):
        directory = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", "./", "ALL Files (*);; Text Files (*.txt)")

        for i in range(len(directory[0])):
            if directory[0][-i] == '/':
                c = len(directory[0])-i+1
                name_pic = directory[0][c:]
                break

        with open(directory[0], 'rb') as fp:
            tu = base64.b64decode(fp.read())

        myFile = tu.decode("utf-8")
        T1 = self.comboBox.currentText()

        data = {'user': data_message[0], 'get_name': T1, 'zwj_data':'', "data_Dame": '', "data_name": name_pic, "file": myFile}
        self.send_all(data)
        self.textEdit2.append("文件已发送！")

    def recursion_dir_all_file(self, path):
        file_list = []
        for dir_path, dirs, files in os .walk(path):
            for file in files:
                file_path = os.path.join(dir_path, file)
                if "\\" in file_path:
                    file_path = file_path.replace('\\', '/')
                file_list.append(file_path)
            for dir in dirs:
                file_list.extend(self.recursion_dir_all_file(os.path.join(dir_path, dir)))
        return file_list

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Test_win()
    win.show()
    sys.exit(app.exit())