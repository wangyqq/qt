# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Administrator\Desktop\qt\talk\talk.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(290, 40, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(290, 90, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(20, 10, 31, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 150, 31, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setGeometry(QtCore.QRect(300, 130, 93, 31))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Form)
        self.radioButton_2.setGeometry(QtCore.QRect(300, 160, 93, 31))
        self.radioButton_2.setObjectName("radioButton_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(280, 220, 111, 31))
        self.lineEdit_3.setText("")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(310, 200, 54, 12))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(290, 260, 41, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_2.setFont(font)
        self.label_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_2.setAutoFillBackground(False)
        self.label_2.setObjectName("label_2")
        self.lineEdit_4 = QtWidgets.QLineEdit(Form)
        self.lineEdit_4.setGeometry(QtCore.QRect(320, 260, 61, 21))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(20, 40, 241, 101))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(Form)
        self.textEdit_2.setGeometry(QtCore.QRect(20, 180, 241, 101))
        self.textEdit_2.setObjectName("textEdit_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "连接/开启"))
        self.pushButton_2.setText(_translate("Form", "发送"))
        self.lineEdit.setText(_translate("Form", "发送"))
        self.lineEdit_2.setText(_translate("Form", "接收"))
        self.radioButton.setText(_translate("Form", "客户端"))
        self.radioButton_2.setText(_translate("Form", "服务端"))
        self.label.setText(_translate("Form", "ip地址"))
        self.label_2.setToolTip(_translate("Form", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.label_2.setText(_translate("Form", "端口"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
