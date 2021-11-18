import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from MainWindow_Model import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./icons/pixiu.png"))
    myWin = MainWindow()
    myWin.show()
    sys.exit(app.exec_())