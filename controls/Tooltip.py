import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QPushButton,QHBoxLayout,QWidget,QToolTip
from PyQt5.QtGui import QFont

class TooltipForm(QMainWindow):
    def __init__(self):
        super(TooltipForm, self).__init__()
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SanSerif', 12))
        self.setToolTip('今天是<b>星期五</b>')
        self.setGeometry(300,30,200,300)
        self.setWindowTitle('设置控件提示消息')

        self.button1 = QPushButton('按钮')
        self.button1.setToolTip('1111121')

        layout = QHBoxLayout()
        layout.addWidget(self.button1)
        mainFram = QWidget()
        mainFram.setLayout(layout)

        self.setCentralWidget(mainFram)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = TooltipForm()
    main.show()
    sys.exit(app.exec_())

