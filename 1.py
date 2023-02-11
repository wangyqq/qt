import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QGridLayout, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
import socket
import time
import threading
import os
import cv2
import numpy as np
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 layout - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100
        self.initUI()
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        gridLayout = QGridLayout()
        self.setLayout(gridLayout)
        button = QPushButton('Start', self)
        button.setToolTip('This is an example button')
        button.move(100,70)
        button.clicked.connect(self.on_click)
        button2 = QPushButton('Stop', self)
        button2.setToolTip('This is an example button')
        button2.move(200,70)
        button2.clicked.connect(self.on_click2)
        self.label = QLabel(self)
        self.label.setText("Hello")
        gridLayout.addWidget(self.label, 0, 0)
        self.show()
    @pyqtSlot()
    def on_click(self):
        self.label.setText("Start button is pressed")
        self.thread = ThreadClass()
        self.thread.start()
    @pyqtSlot()
    def on_click2(self):
        self.label.setText("Stop button is pressed")
        self.thread.stop()
class ThreadClass(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.isRunning = True
    def run(self):
        while self.isRunning:
            print("thread is running")
            time.sleep(1)
    def stop(self):
        self.isRunning = False
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())