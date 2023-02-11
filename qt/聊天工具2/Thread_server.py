import json
import struct

from PyQt5 import QtWidgets
import os
from chat import Ui_MainWindow
import sys
import threading
from socket import *
import base64

HOST = '127.0.0.1'
PORT = 9999
ADDR = (HOST, PORT)

user_data = dict()
name_ip = dict()

class Test_win(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Test_win, self).__init__()
        self.setupUi(self)

        self.Button_send.clicked.connect(self.Send)
        self.Button_pic.clicked.connect(self.pic)
        self.Button_data.clicked.connect(self.msg)
        self.pushButton.clicked.connect(self.Delete)

        self.comboBox.addItems(['ALL-MESS'])

        self.tcpSerSock = socket(AF_INET, SOCK_STREAM)
        self.tcpSerSock.connect(ADDR)
        self.tcpSerSock.listen(5)

        self.socks = [] # 所有连接用户

        # 启动线程
        t1 = threading.Thread(target=self.Link)
        t1.start()

    def Link(self):
        self.textEdit3.append("服务端")
        self.textEdit3.append("等待客户端连接...")

        while True:
            client, addr = self.tcpSerSock.accept()
            self.textEdit3.append("成功与客户端" + str(addr) + "连接!")
            text = '请输入昵称开始聊天'

            text = {'user': "user", "get_name":"user", 'text':text, 'list_user': ""}
            self.send_once(text, client)
            self.socks.append(client)

            threading.Thread(target=self.Get, args=(client,addr,name_ip)).start()

    def Delete(self):
        self.textEdit3.setPlainText(" ")

    def Send(self):
        self.text = self.textEdit.toPlainText()
        print(self.text)

        self.textEdit3.append(('user :' + self.text))
        self.textEdit.setPlainText("")

        text = self.comboBox.currentText()
        text1 = {'user': 'user', 'get_name': text, 'text':self.text, 'list_user':''}
        dataToSend = json.dumps(text1).encode('utf-8')
        msg_len = struct.pack('i', len(dataToSend))

        if text == 'ALL-MESS':
            self.send_all( msg_len, dataToSend)

        elif text in user_data.keys():
            user_data[text]["clients"].send(msg_len)
            user_data[text]["clients"].send(dataToSend)
        self.Button_send.clicked.connect(self.Send)

    def send_all(self,msg_len,dataToSend):
        for x in self.socks:
            x.send(msg_len)
            x.send(dataToSend)

    def send_onec(self, text, clinet):
        dataToSend = json.dumps(text, ensure_ascii=False).encode("utf-8")
        msg_len = struct.pack('i', len(dataToSend))
        clinet.send(msg_len)
        clinet.send(dataToSend)

    def get_data(self, get_name, addr, text, data, Data):
        if get_name == 'ALL-MESS':
            self.textEdit3.append(name_ip[addr] + ' :' + text)
            self.send_all(data, Data)
        elif get_name == 'User':
            self.textEdit3.append(name_ip[addr] + ' :' + text)
        else:
            user_data[get_name]["clients"].send(data)
            user_data[get_name]["clients"].send(Data)

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

    def Get(self, client, addr, name_ip):
        data = client.recv(4)
        len_data = struct.unpack('i', data)[0]
        Data = client.recv(len_data)
        dic = eval(Data.decode('utf-8'))

        name = dic['text']
        print(f'客户端 {addr} 设置的昵称是:', name)

        data1 = {'addr': addr, 'clients':client}
        user_data[name] = data1
        name_ip[addr] = name

        text1 = {'user': "Root", 'get_name':'All-MESS', 'text': name, 'list_user': list(user_data.keys())}
        dataToSend = json.dumps(text1).encode('utf-8')
        msg_len = struct.pack('i', len(dataToSend))
        self.send_all(msg_len, dataToSend)

        self.comboBox.clear()
        self.user = ['ALL-MESS'] + list(user_data.keys())
        self.comboBox.addItems(self.user)
        self.textEdit3.append("当前连接人数为" + str(len(list(user_data.keys()))) + "人。。。。。")

        while True:
            data = self.tcpCliSock.recv(4) # 接收4个字节

            # 解码要接收多大的数据
            len_data = struct.unpack('i', data)[0]
            Data = self.tcpCliSock.recv(len_data)
            dic = eval(Data.decode('utf-8'))

            get_name = dic['get_name']
            user = dic['user']

            if Data.decode('utf-8') != '':
                if len(Data) < 200:
                    text = dic['text'] # 消息内容
                    if text == 'Q':
                        new_user = []
                        print('用户已断开连接')
                        self.textEdit3.append("用户" + user + "已退出聊天！")
                        for i in list(user_data.keys()):
                            if i != user:
                                new_user.append(i)

                        self.comboBox.clear()
                        text1 = {'user':"Root", 'get_name': 'ALL-MESS', 'text':name, 'list_user': new_user}
                        msg_len = struct.pack('i', len(dataToSend))
                        self.send_all(msg_len, dataToSend)

                        # 更新当前连接用户
                        self.user = ['ALL-MESS'] + new_user
                        self.comboBox.addItems(self.user)
                    else:
                        self.get_data(get_name, addr, text, data, Data)
                else:
                    data_name = dic['data_name']
                    pic = dic['file']
                    zwj_data = dic['zwj_data']
                    data_Dame = dic['data_Dame']


                    if get_name == 'All-MESS':
                        self.send_all(data, Data)
                        self.get_all(data_Dame, data_name, pic, zwj_data)
                    elif get_name == 'User':
                        self.get_all(data_Dame, data_name, pic, zwj_data)
                    else:

                        user_data[get_name]["clients"].send(data)
                        user_data[get_name]["clients"].send(Data)

    def msg(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "C:/")
        list_data = self.recursion_dir_all_file(directory)
        print(list_data)

        # 文件夹名称
        for i in range(len(directory)):
            if directory[-i] == "/":
                c = len(directory)-i+1
                data_Dame = directory[c:]
                break

        # 当循环对当前目录下的文件进行一次发送
        for i in list_data:
           myFile, data_name = self.get_dataname(i)
           T1 = self.comboBox.currentText()
           zwj_data = i[len(directory): -len(data_name) - 1]
           data = {'user': 'user', "get_name": T1, 'zwj_data': zwj_data, "data_Dame": data_Dame,
                   "data_name": data_name, "file": myFile}
           self.send_all(data)
           dataToSend = json.dumps(data,ensure_ascii=False).encode("utf-8")
           msg_len = struct.pack('i', len(dataToSend))
           if T1 == 'ALL-MESS':
               self.textEdit2.append('文件已发送')
               self.send_all(msg_len, dataToSend)
           elif T1 in user_data.keys():

               user_data[T1]['client'].send(msg_len)
               user_data[T1]['client'].send(dataToSend)
               self.textEdit2.append('文件已发送')

    def get_dataname(self, name):
        for i in range(len(name)):
            if name[-i] == "/":
                c = len(name) - i + 1
                data_name = name[c:]
                break
        with open(name, 'rb') as fp:
            tu = base64.b64decode(fp.read())
        myFile = tu.decode("utf-8")
        return myFile,data_name

    def pic(self):
        directory = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", "./", "ALL Files (*);; Text Files (*.txt)")

        myFile, data_name = self.get_dataname(directory[0])
        T1 = self.comboBox.currentText()
        data = {'user': 'user', "get_name": T1,
                "data_name": data_name, "file": myFile}
        dataToSend = json.dumps(data, ensure_ascii=False).encode("utf-8")
        msg_len = struct.pack('i', len(dataToSend))
        if T1 == 'ALL-MESS':
            self.textEdit2.append('文件已发送')
            self.send_all(msg_len, dataToSend)
        elif T1 in user_data.keys():
            user_data[T1]['client'].send(msg_len)
            user_data[T1]['client'].send(dataToSend)
            self.textEdit2.append('文件已发送')

    def recursion_dir_all_file(self, path):
        file_list = []
        for dir_path, dirs, files in os.walk(path):
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

