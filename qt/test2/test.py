import os
import sys

from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal, QObject, QProcess
import threading


# 用于爬虫的函数，这里仅作模拟
from lagouwang import lagouSpitder


class Stream(QObject):
    """Redirects console output to text widget."""
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))

def spider_start():
    print("Spider start.")
    spider = lagouSpitder()
    spider.run()

# 线程类，运行爬虫函数
class SpiderThread(QThread):
    spider_signal = pyqtSignal()

    def __int__(self):
        super(SpiderThread, self).__init__()

    def run(self):
        spider_start()
        # 发出信号
        self.spider_signal.emit()


# GUI类，按钮按下时启动爬虫线程
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        sys.stdout = Stream(newText=self.onUpdateText)

    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.process.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()

    def on_click(self):
        sys.stdout.write('y\n')

    def initUI(self):
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle("Spider Start")

        self.btn1 = QPushButton("Start", self)
        self.btn1.clicked.connect(self.startSpider)
        self.btn1.move(300, 150)
        self.btn2 = QPushButton("Enter 'y'", self)
        self.btn2.move(300, 200)
        self.btn2.clicked.connect(self.on_click)

        self.process = QTextEdit(self, readOnly=True)
        self.process.ensureCursorVisible()
        self.process.setLineWrapColumnOrWidth(200)
        self.process.setLineWrapMode(QTextEdit.FixedPixelWidth)
        self.process.setFixedWidth(250)
        self.process.setFixedHeight(200)
        self.process.move(30, 50)
        self.show()

    # 启动爬虫线程
    def startSpider(self):
        self.thread = SpiderThread()
        self.thread.spider_signal.connect(self.spiderFinished)
        self.thread.start()

    def spiderFinished(self):
        print("Spider finished.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
