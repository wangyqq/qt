import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        qbtn = QPushButton('触发程序', self)
        qbtn.clicked.connect(self.run_program)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('触发程序')
        self.show()


    def run_program(self):
        # 在此处完成你要执行的后端控制台程序
        pass

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())