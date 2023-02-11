import sys
from PyQt5.QtWidgets import QMainWindow, QApplication,QDesktopWidget

class Centerform(QMainWindow):
    def __init__(self):
        super(Centerform, self).__init__()

        # 设置窗口标题
        self.setWindowTitle('居中')
        # 设置尺寸
        self.resize(400,300)

    def center(self):
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newleft =  (screen.width() - size.width()) / 2
        newtop =  (screen.width() - size.height()) / 2
        self.move(newleft, newtop)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Centerform()
    main.show()
    sys.argv(app.exec_())