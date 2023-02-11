import sys

from PyQt5.QtGui import QIcon

import chat
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow




if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('images/1.jpg'))
    mainwindow = QMainWindow()
    ui = chat.Ui_MainWindow()
    # 向主窗口添加控件
    ui.setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())