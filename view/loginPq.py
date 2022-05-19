from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import sys


class Root(QDialog):
    def __init__(self, parent=None):
        super(Root, self).__init__(parent)
        layout1 = QBoxLayout(0, self)
        button = QPushButton("Hola", self)
        button.clicked.connect(self.handle)

    def handle(self):
        print("Hola")


if __name__ == "__main__":
    app = QtGui.QGuiApplication([])
    screen_resolution = app.primaryScreen().geometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    Applicaction = QApplication([])
    App = Root()
    App.setGeometry(width / 4, -height /2, width /2, height /2)
    App.show()
    sys.exit(Applicaction.exec_())
