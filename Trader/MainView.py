import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow
# from CustomTableView import *
from TableWidgetMainView import  *
# from TableViewMainView import  *
import pandas as pd

pd.set_option('display.width', 300)
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.startRealTime()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./icons/pixiu.png"))

    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
