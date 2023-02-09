import sys
from chat import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog




if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = QMainWindow()
    ui = Ui_MainWindow()
    # 向主窗口添加控件
    ui.setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())