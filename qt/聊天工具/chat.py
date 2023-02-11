# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import base64

from PyQt5 import QtCore, QtGui, QtWidgets

from threading import Thread
import socket

from PyQt5.QtGui import QPixmap, QTextDocument
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from TCP import Server, Client


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.pc = None  # 预设这个变量
        self.statusBar = QtWidgets.QStatusBar()  # 状态栏


        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("#MainWindow{border-image:url(./images/3.jpg);}")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(60, 50, 421, 331))
        self.textBrowser.setObjectName("textBrowser")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(60, 430, 421, 51))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")

        self.checkBox = QtWidgets.QRadioButton(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(530, 400, 105, 22))
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.checkBox.toggled.connect(self.radiobtnChange)
        self.checkBox_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(650, 400, 105, 22))
        self.checkBox_2.setObjectName("checkBox_2")

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(520, 440, 235, 36))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # 建立服务器
        self.pushButton_4 = QtWidgets.QPushButton(self.widget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.pushButton_4.clicked.connect(self.setServer)
        self.pushButton_4.setStyleSheet("background-color: yellow;")
        # 连接服务器
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_3.clicked.connect(self.setClient)
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setStyleSheet("background-color: yellow;")

        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(90, 500, 356, 36))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.pushButton = QtWidgets.QPushButton(self.layoutWidget1) # 发送
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.sendInfo)
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton.setStyleSheet("background-color: yellow;")
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget1) # 选择图片
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.pushButton_2.clicked.connect(self.select_image)
        self.pushButton_2.setStyleSheet("background-color: yellow;")
        self.pushButton_5 = QtWidgets.QPushButton(self.layoutWidget1) # 发送图片
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.sendimage)
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.pushButton_5.setStyleSheet("background-color: yellow;")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(490, 70, 291, 191))
        self.label.setObjectName("label")
        self.label.setStyleSheet("QLabel { background-color : white; color : blue; }")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "在线聊天系统"))
        self.checkBox.setText(_translate("MainWindow", "服务端"))
        self.checkBox_2.setText(_translate("MainWindow", "客户端"))
        self.pushButton_4.setText(_translate("MainWindow", "建立服务器"))
        self.pushButton_3.setText(_translate("MainWindow", "连接服务器"))
        self.pushButton.setText(_translate("MainWindow", "发送"))
        self.pushButton_2.setText(_translate("MainWindow", "选择图片"))
        self.label.setText(_translate("MainWindow", "图片"))
        self.pushButton_5.setText(_translate("MainWindow", "发送图片"))

    def select_image(self):
        self.pic_path, _ = QFileDialog.getOpenFileName(None, '选择图片', '', 'Image Files(*.jpg *.png)')
        jpg = QPixmap(self.pic_path).scaled(self.label.width(), self.label.height())
        self.label.setPixmap(jpg)
        print(self.pic_path)

    # 单选按钮切换函数
    def radiobtnChange(self, status):
        if status:
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(True)
        else:
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(False)

    # 状态栏情况发送函数
    def sendInfo(self):
        if self.pc == None:
            self.statusBar.showMessage("sned info field case out connected!!")
        else:
            if self.lineEdit:
                print(self.lineEdit)
                info = self.lineEdit.text()
                if info != "":
                    info = self.pc.hostName + ":\n" + info
                    self.pc.btnsend(info)
                    self.lineEdit.clear()
                else:
                    self.statusBar.showMessage("input can't be none!")

    # 发送图片
    def sendimage(self):
        if self.label:
            print(self.label)
            jpg = QPixmap(self.pic_path).scaled(self.label.width() / 2 , self.label.height() / 2)
            self.textBrowser.document().addResource(QTextDocument.ImageResource, QUrl(self.pic_path), jpg)
            self.textBrowser.append(self.pc.hostName)
            self.textBrowser.append("<img src='" + self.pic_path + "'/>")
            self.pc.btnsend(self.pic_path)
            self.label.clear()

    # 设定本主机为服务器
    def setServer(self):
        self.pc = Server(self, "127.0.0.1", "服务管理员", int(9999))
        print('建立成功')
    # 设定本主机为客户端
    def setClient(self):
        self.pc = Client(self, "127.0.0.1" , "匿名用户", int(9999))
        print('连接成功')


