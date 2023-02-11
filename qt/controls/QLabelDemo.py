import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QHBoxLayout, QWidget, QToolTip, QLabel,QVBoxLayout
from PyQt5.QtGui import QPalette,QPixmap
from PyQt5.QtCore import Qt


class QLabelDemo(QWidget):
    def __init__(self):
        super(QLabelDemo, self).__init__()
        self.initUI()

    def initUI(self):
        label1 = QLabel(self)
        label2 = QLabel(self)
        label3 = QLabel(self)
        label4 = QLabel(self)

        label1.setText("<font color=yellow>这是一个文本标签.</font>")
        label1.setAutoFillBackground(True)
        palette = QPalette() # 涂色对象
        palette.setColor(QPalette.Window,Qt.blue)
        label1.setPalette(palette)
        label1.setAlignment(Qt.AlignCenter)

        label2.setText("<a href='#'>欢迎使用</a>")

        # 对齐方式，将控件文本居中对其
        label3.setAlignment(Qt.AlignCenter)
        label3.setToolTip('这是图片标签')
        label3.setPixmap(QPixmap('../聊天工具/images/2.jpg'))

        label4.setOpenExternalLinks(True) # True:打开浏览器  Flase:调用槽
        label4.setText("<a href='https://www.baidu.com'>百度一下</a>")
        label4.setAlignment(Qt.AlignCenter)
        label4.setToolTip('超级链接')

        vbox = QVBoxLayout()

        vbox.addWidget(label1)
        vbox.addWidget(label2)
        vbox.addWidget(label3)
        vbox.addWidget(label4)

        label2.linkHovered.connect(self.linkHovered)
        label4.linkActivated.connect(self.ccc)

        self.setLayout(vbox)
        self.setWindowTitle('QLable演示')

    def linkHovered(self):
        print('label2划过')

    def ccc(self):
        print('label4点击')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QLabelDemo()
    main.show()
    sys.exit(app.exec_())

