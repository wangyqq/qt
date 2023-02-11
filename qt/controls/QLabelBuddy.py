
from PyQt5.QtWidgets import *
import sys

class QLabelBuddy(QDialog):
    def __init__(self):
        super(QLabelBuddy, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('label与伙伴关系')
        namelabel = QLabel('&Name',self)
        namelineEdit = QLineEdit(self)
        # 设置伙伴关系
        namelabel.setBuddy(namelineEdit)

        passwordlabel = QLabel('&OK', self)
        passwordlineEdit = QLineEdit(self)
        # 设置伙伴关系
        passwordlabel.setBuddy(passwordlineEdit)

