import socket
from PyQt5.QtCore import *

# 服务端
from PyQt5.QtGui import QPixmap, QTextDocument

cname = '匿名用户'
sname = '服务管理员'

class Server():
    def __init__(self, widget, ip, host, port):
        # 设定本主机的一些基本信息 ---------------------------------------
        self.widget = widget
        self.ip = ip  # 获得该主机ip
        self.hostName = host  # 获得该主机名
        self.port = port  # 设定默认端口号(服务器端口号和客户端接入端口号都是这个默认端口)
        self.serverDict = {}  # 服务线程字典
        self.serverID = 0  # 初始的服务线程id

        self.buildSocket()

    # 创建网络连接实例
    def buildSocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.initialServer()

    # 初始化服务(仅限服务器)
    def initialServer(self):
        # 首先绑定服务端口号
        self.socket.bind((self.ip, self.port))  # 绑定端口与主机名
        self.socket.listen(5)  # 设定最大连接数

        self.buildServer()  # 初始化一个服务线程

    # 创建服务线程
    def buildServer(self):
        server = ServerThread(str(self.serverID), self.socket)
        self.serverDict[str(self.serverID)] = server
        self.serverID += 1
        server._text.connect(self.getText)
        server.start()

    # 广播所有消息
    def bordCastInfo(self, info):
        print(len(self.serverDict))
        for client in self.serverDict:
            if self.serverDict[client].clientsocket != None:
                print("尝试将信息广播出去")
                self.serverDict[client].sendToClient(info)  # 将消息传入指定的客户端
                print("广播成功")

    def btnsend(self, text):
        self.widget.textBrowser.append(text)
        self.bordCastInfo(text)

    # 关闭所有的服务
    def closeThread(self):
        for server in self.serverDict:
            self.serverDict[server].runflag = False


    def getText(self, text):
        if len(text) < 25:
            self.widget.textBrowser.append(text)
            self.bordCastInfo(text)  # 广播出去
        else:
            jpg = QPixmap(text).scaled(self.widget.label.width() / 2, self.widget.label.height() / 2)
            self.widget.textBrowser.document().addResource(QTextDocument.ImageResource, QUrl(text), jpg)
            self.widget.textBrowser.append(cname)
            self.widget.textBrowser.append("<img src='" + text + "'/>")
            # self.bordCastInfo(text)  # 广播出去


# 客户端
class Client():  # 主机默认为本地主机,
    def __init__(self, widget, ip, hostName, port):
        self.widget = widget
        self.ip = ip
        self.hostName = hostName  # 获得该主机名
        self.port = port  # 设定默认端口号(服务器端口号和客户端接入端口号都是这个默认端口)
        self.buildSocket()

    def buildSocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buildClient()

    def buildClient(self):
        self.client = ClientThread(self.socket)  # 获取连接
        self.client._text.connect(self.getText)
        if self.client.connectServer(self.ip, self.port):
            self.client.start()

    def sendToServer(self, text):  # 向服务器发送消息
        self.socket.send(text.encode('utf-8'))

    def btnsend(self, text):
        self.sendToServer(text)

    def closeThread(self):
        self.runflag = False

    def getText(self, text):
        if len(text) < 25:
            self.widget.textBrowser.append(text)
        else:
            jpg = QPixmap(text).scaled(self.widget.label.width() / 2, self.widget.label.height() / 2)
            self.widget.textBrowser.document().addResource(QTextDocument.ImageResource, QUrl(text), jpg)
            self.widget.textBrowser.append(sname)
            self.widget.textBrowser.append("<img src='" + text + "'/>")


# 监听连接线程,负责构成会话(服务端线程)
class ServerThread(QThread):
    _text = pyqtSignal(str)  # 设定信号,向主线程发送接收到的信息

    def __init__(self, serverID, serverSocket):
        super(ServerThread, self).__init__()
        self.serverID = serverID  # 获得主机实例
        self.serverSocket = serverSocket
        self.clientsocket = None
        self.addr = None
        self.runflag = True

    # 自动进行该函数
    def run(self):
        self.clientsocket, self.addr = self.serverSocket.accept()  # 收到客户端的连接后返回 连接控件,地址(持续监听,直到接收到执行下一个操作)
        print(self.clientsocket)
        self.sendText("Customer IP: %s" % str(self.addr) + " is linking!")
        self.getMessage()

    # 持续接受消息
    def getMessage(self):
        while self.runflag:
            data = self.clientsocket.recv(1024).decode('utf-8')  # 接受到字符串并按照utf-8编译
            self.sendText(data)

        self.clientsocket.close()
        print("线程关闭成功")

    def sendToClient(self, info):
            self.clientsocket.send(info.encode("utf-8"))
            print("广播成功")

    # 发送接收到的消息信号
    def sendText(self, text):
        self._text.emit(text)



class ClientThread(QThread):
    _text = pyqtSignal(str)

    def __init__(self, serverSocket):
        super(ClientThread, self).__init__()
        self.serverSocket = serverSocket
        self.runflag = True
        self.connectList = ["connect", "disconnect"]  # 连接成功与连接失败

    def connectServer(self, ip, port):
        try:
            self.serverSocket.connect((ip, port))
            return True
        except Exception as reason:
            return reason

    def run(self):
        while self.runflag:
            try:
                msg = self.serverSocket.recv(1024).decode("utf-8")  # 接受服务端消息
                self.sendText(msg)
            except Exception:
                break

    def sendText(self, text):
        self._text.emit(str(text))
