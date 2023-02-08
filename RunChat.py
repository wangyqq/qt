import sys
from test import Ui_Form
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow




if __name__ == '__main__':
    app = QApplication(sys.argv)
    qwidget = QWidget()
    my = Ui_Form()
    my.setupUi(qwidget)
    qwidget.show()
    sys.exit(app.exec_())