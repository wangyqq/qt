import sys

from PyQt5.QtGui import QIcon

from chat import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog




if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('images/2.jpg'))
    mainwindow = QMainWindow()
    ui = Ui_MainWindow()
    # 向主窗口添加控件
    ui.setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())