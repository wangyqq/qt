from PyQt5.Qt import *
from talk import Ui_Form
import socket
import sys
import time

class Window(QWidget,Ui_Form):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setupUi(self)
        ipaddress = Socket_Client.get_ip() #调用类方法进行获取ip
        self.lineEdit_3.setText(ipaddress)
        self.radioButton.setChecked(True)
        self.lineEdit_4.setText("8888")
        self.pushButton.clicked.connect(self.socket_connect)
        self.pushButton_2.clicked.connect(self.send_message)
        self.radioButton.toggled.connect(self.switch_client_server)

    def switch_client_server(self):
        print("switch")
        self.pushButton.clicked.connect(self.socket_server)
        self.pushButton_2.clicked.connect(self.server_send_data)

    def socket_connect(self): #连接按钮绑定函数，建立socket连接
        QCoreApplication.processEvents();
        try:
            self.socket_client = Socket_Client(self.lineEdit_3.text(),int(self.lineEdit_4.text()))
            self.socket_client.client_socket()
            self.setWindowTitle("聊天程序1.0 连接成功")
            self.thread_1 = Thread_recv(self.socket_client,self.textEdit_2)
            self.thread_1.start()
        except Exception as e:
            print(e)
            print("error")
            self.setWindowTitle("聊天程序1.0 连接失败")

    def socket_server(self):  #服务端函数
        QCoreApplication.processEvents();
        try:
            self.server_socket = Socket_Client(self.lineEdit_3.text(),int(self.lineEdit_4.text()))
            self.server_socket.server_socket()
            self.setWindowTitle("聊天程序1.0 服务开启成功")
            self.thread_2 = Thread_sev(self.server_socket,self.textEdit_2)
            self.thread_2.start()
        except Exception as e:
            print(e)
            self.setWindowTitle("聊天程序1.0 服务开启失败")

    def send_message(self):#发送消息

        try:
            self.socket_client.send_data(self.textEdit.toPlainText())
            localtime = time.strftime("%H:%M:%S")
            self.textEdit_2.append(f"[{localtime}]:"+"发送成功!")
            self.textEdit_2.append(f"[{localtime}]:" + "我说:" + self.textEdit.toPlainText() )
            self.textEdit.clear()
            self.textEdit.moveCursor(QTextCursor.End)
        except Exception as e:
            print(e)

    def server_send_data(self):
        try:
            self.server_socket.server_send_data(self.textEdit.toPlainText())
            localtime = time.strftime("%H:%M:%S")
            self.textEdit_2.append(f"[{localtime}]:" + "发送成功!")
            self.textEdit_2.append(f"[{localtime}]:" + "我说:" + self.textEdit.toPlainText())
            self.textEdit.clear()
            self.textEdit.moveCursor(QTextCursor.End)
        except Exception as e:
            print(e)

class Thread_recv(QThread):
    def __init__(self, recv,text_edit):
        super().__init__()
        self.recv = recv
        self.text_edit = text_edit

    def run(self):
        while True:
            self.recv_data = self.recv.recv_data()
            print(self.recv_data)
            localtime = time.strftime("%H:%M:%S")
            self.text_edit.append( f"[{localtime}]:" +"对方说:"+ self.recv_data)

class Thread_sev(QThread):
    def __init__(self,server_socket,text_edit):
        super().__init__()
        self.server = server_socket
        self.text = text_edit

    def run(self):
        self.server.server_accept()
        print(self.server.client_ip_port)
        localtime = time.strftime("%H:%M:%S")
        self.text.append(f"[{localtime}]:" + f"客户端连接成功:{self.server.client_ip_port[0]}")
        while True:
            self.data = str(self.server.client.recv(1024),"gbk")
            print(self.data)
            localtime = time.strftime("%H:%M:%S")
            self.text.append(f"[{localtime}]:" + "对方说:" + self.data)

class Socket_Client(object):
    def __init__(self,ipadress,port):
        self.ipaddress = ipadress
        self.port = port

    @classmethod
    def get_ip(cls):
        socket_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            socket_ip.connect(('10.255.255.255', 1))
            return socket_ip.getsockname()[0]
        except Exception:
            return '127.0.0.1'
        finally:
            socket_ip.close()

    def client_socket(self):
        self.client_connect = socket.socket(family=-1,type=-1)
        self.client_connect.connect((self.ipaddress,self.port))

    def close_socket(self):
        self.client_connect.close()

    def server_socket(self):
        self.server_connect = socket.socket(family=-1,type=-1)
        self.server_connect.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.server_connect.bind((self.ipaddress,self.port))
        self.server_connect.listen(128)

    def server_accept(self):
        self.client,self.client_ip_port = self.server_connect.accept()

    def server_send_data(self,data):
        data = data.encode('gbk')
        print(data)
        self.client.send(data)

    def send_data(self,data):
        data = data.encode('gbk')  #进行gbk编码
        print(data)
        self.client_connect.send(data)

    def recv_data(self):
        recv = str(self.client_connect.recv(1024),'gbk') #以gbk方式转码
        return recv

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window =   Window()
    window.setWindowTitle("聊天程序1.0")
    window.show()
    sys.exit(app.exec())
