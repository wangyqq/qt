# 服务端
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
        # socket.AF_INET(!!INET - IPv4  INET6 - IPv6)
        # socket.SOCK_STREAM - 传输控制协议(TCP)
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

        server._flag.connect(self.getFlag)
        server._signal.connect(self.getMessage)
        server._text.connect(self.getText)
        server._image.connect(self.getimage)

        server.start()

    # 广播所有消息
    def bordCastInfo(self, info):
        print(len(self.serverDict))
        for client in self.serverDict:
            try:
                if self.serverDict[client].clientsocket != None:
                    print("尝试将信息广播出去")
                    self.serverDict[client].sendToClient(info)  # 将消息传入指定的客户端
                    print("广播成功")
            except Exception as reason:
                self.getFlag("@@@".join([client, "disconnect"]))  # 运行函数,停止某个客户端的监听(相当于关闭)
                print("服务端", reason)



    # 关闭所有的服务
    def closeThread(self):
        for server in self.serverDict:
            self.serverDict[server].runflag = False

    def getFlag(self, flag):
        flag = flag.split("@@@")
        if flag[1] == "connect":  # 如果传来连接成功,则新开一个线程监听
            self.buildServer()
        elif flag[1] == "disconnect":  # 如果连接出现问题
            self.serverDict[flag[0]].runflag = False

    def getMessage(self, signal):
        signal = signal.split("@@@")
        self.widget.statusBar.showMessage("serverID " + signal[0] + " status:" + signal[1])

    # 接收文本
    def getText(self, text):
        self.widget.textBrowser.append(text)
        self.bordCastInfo(text)  # 广播出去

    # 接收图片数据
    def getimage(self, pic_path):
        pass

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
        self.client._flag.connect(self.getFlag)
        self.client._signal.connect(self.getMessage)
        self.client._text.connect(self.getText)
        if self.client.connectServer(self.ip, self.port):
            self.client.start()

    # 发送文本数据
    def sendToServer(self, text):  # 向服务器发送消息
        try:
            self.socket.send(text.encode('utf-8'))
        except Exception as reason:
            self.getMessage(reason)
            self.getFlag("disconnect")  # 发送连接失败标志
    def btnsend(self, text):
        self.sendToServer(text)

    # 发送图片数据
    def send_pic(self, pic_path):
        with open(pic_path, 'wb') as f:
            load = f.read()
        b64_data = base64.b64encode(load)
        self.socket.send(b64_data)

    def btcsend(self, pic_path):
        self.send_pic(pic_path)


    def closeThread(self):
        self.runflag = False

    def getFlag(self, flag):
        if flag == "connect":
            self.widget.statusBar.showMessage("connect success!!")
        elif flag == "disconnect":
            self.client.runflag = False

    def getMessage(self, signal):
        self.widget.statusBar.showMessage(signal)

    def getText(self, text):
        self.widget.textBrowser.append(text)

# 监听连接线程,负责构成会话(服务端线程)
class ServerThread(QThread):
    _signal = pyqtSignal(str)  # 设定信号,主要向主线程发送信号
    _text = pyqtSignal(str)  # 设定信号,向主线程发送接收到的信息
    _flag = pyqtSignal(str)  # 设定信号,向主线程发送连接状态标志
    _image = pyqtSignal(str)  # 设定信号,向主线程发送连接状态标志

    def __init__(self, serverID, serverSocket):
        super(ServerThread, self).__init__()
        self.serverID = serverID  # 获得主机实例
        self.serverSocket = serverSocket
        self.clientsocket = None
        self.addr = None
        self.runflag = True

        self.connectList = ["connect", "disconnect"]  # 连接成功与连接失败

    # 自动进行该函数
    def run(self):
        self.sendMessage("Waiting for customer......")
        self.clientsocket, self.addr = self.serverSocket.accept()  # 收到客户端的连接后返回 连接控件,地址(持续监听,直到接收到执行下一个操作)
        print(self.clientsocket)
        self.sendText("Customer IP: %s" % str(self.addr) + " is linking!")
        self.sendFlag(0)  # 发送连接成功标志
        self.getMessage()

    # 持续接受消息
    def getMessage(self):
        while self.runflag:
            try:
                data = self.clientsocket.recv(1024).decode('utf-8')  # 接受到字符串并按照utf-8编译
                self.sendText(data)
            except Exception as reason:
                self.sendMessage(str(reason))
                self.sendText(str(self.addr) + " break connect...")
                self.sendFlag(1)  # 发送断开连接标志
                break
        self.clientsocket.close()
        print("线程关闭成功")

    def sendToClient(self, info):
        print(self.clientsocket)
        try:
            self.clientsocket.send(info.encode("utf-8"))
            print("广播成功")
        except Exception as reason:
            print("广播失败原因", reason)
            self.sendMessage(self.addr + " break connect...")
            self.sendFlag(1)

    # 发送状态信号函数
    def sendMessage(self, message):
        self._signal.emit("@@@".join([self.serverID, message]))

    # 发送接收到的消息信号
    def sendText(self, text):
        self._text.emit(text)

    # 发送连接状态标志
    def sendFlag(self, flagIndex):
        self._flag.emit("@@@".join([self.serverID, self.connectList[flagIndex]]))


class ClientThread(QThread):
    _signal = pyqtSignal(str)
    _text = pyqtSignal(str)
    _flag = pyqtSignal(str)

    def __init__(self, serverSocket):
        super(ClientThread, self).__init__()
        self.serverSocket = serverSocket
        self.runflag = True
        self.connectList = ["connect", "disconnect"]  # 连接成功与连接失败

    def connectServer(self, ip, port):
        try:
            self.serverSocket.connect((ip, port))
            self.sendFlag(0)  # 发送连接成功标志
            return True
        except Exception as reason:
            self.sendMessage(reason)
            self.sendFlag(1)  # 发送链接失败标志
            return reason

    def run(self):
        while self.runflag:
            try:
                msg = self.serverSocket.recv(1024).decode("utf-8")  # 接受服务端消息
                self.sendText(msg)
            except Exception as reason:
                self.sendMessage(reason)
                self.sendFlag(1)  # 发送连接失败标志
                break

    def sendMessage(self, message):
        self._signal.emit(str(message))

    def sendText(self, text):
        self._text.emit(str(text))

    def sendFlag(self, flagIndex):
        self._flag.emit(str(self.connectList[flagIndex]))