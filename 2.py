服务端：

import socket
import base64

#声明socket类型，同时生成socket连接对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#绑定本机IP和任意端口(端口范围： 0-65535)
s.bind(('127.0.0.1', 9999))

#开始监听端口
s.listen(5)

while True:
    #等待客户端连接
    connection, address = s.accept()
    #接收客户端发送的数据
    recv_data = connection.recv(1024)
    #解码
    img_data = base64.b64decode(recv_data)
    #保存图片
    with open('image.png','wb') as f:
        f.write(img_data)
    print('图片接收完成')
    #关闭连接
    connection.close()

客户端：

import socket
import base64

#声明socket类型，同时生成socket连接对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#建立连接
s.connect(('127.0.0.1', 9999))

#读取图片文件
with open('image.png', 'rb') as f:
    data = f.read()
    #编码
    b64_data = base64.b64encode(data)
    #发送编码后的图片数据
    s.send(b64_data)
#关闭连接
s.close()