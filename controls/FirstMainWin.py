import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QIcon

class FirstMainWin(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口的标题
        self.setWindowTitle('first')

        # 设置窗口尺寸
        self.resize(400, 300)
        self.status = self.statusBar()
        self.status.showMessage('只存在5秒', 5000)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('../聊天工具/images/1.jpg'))
    main = FirstMainWin()
    main.show()
    sys.exit(app.exec_())
