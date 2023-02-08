from PyQt5 import QtCore, QtWidgets


class Window(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.button = QtWidgets.QPushButton("Run Command", self)
        self.button.clicked.connect(self.run_command)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button)

    def run_command(self):
        process = QtCore.QProcess(self)
        process.start("ls -l")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_()) 