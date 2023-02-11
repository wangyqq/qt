import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QPushButton,QHBoxLayout,QWidget

class QuitApp(QMainWindow):
    def __init__(self):
        super(QuitApp, self).__init__()
        # 设置窗口标题
        self.setWindowTitle('按键退出')
        # 设置尺寸
        self.resize(400, 300)
        # 添加按钮
        self.button1 =QPushButton('退出')
        self.button1.clicked.connect(self.onClick)

        layout = QHBoxLayout()
        layout.addWidget(self.button1)
        mainFram = QWidget()
        mainFram.setLayout(layout)

        self.setCentralWidget(mainFram)

    # 单击事件，槽
    def onClick(self):
        sender = self.sender()
        print(sender.text() + '按钮被按下')
        app = QApplication.instance()
        app.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QuitApp()
    main.show()
    sys.exit(app.exec_())