


import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QHBoxLayout, QWidget, QToolTip, QLabel, QLineEdit, \
    QDialog, QGridLayout, QTableView, QVBoxLayout
from PyQt5.QtGui import QIcon, QFont, QStandardItemModel, QStandardItem


import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QTableWidget, QHBoxLayout, QTableWidgetItem,QComboBox, QFrame
from PyQt5.QtGui import QFont, QColor, QBrush, QPixmap
from DBManager import  DBManager

import pandas as pd
class TableSheet(QWidget):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.initUi(df)

    def initUi(self,df):
        print("初始化UI"+str(df.shape))
        horizontalHeader = df.columns

        table = QTableWidget()
        table.setRowCount( df.shape[0])
        table.setColumnCount( df.shape[1])
        table.setHorizontalHeaderLabels(horizontalHeader)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectColumns)
        table.setSelectionMode(QTableWidget.SingleSelection)

        for row in range(df.shape[0]):
            # headItem = table.horizontalHeaderItem(row)
            # headItem.setFont(QFont("song", 12, QFont.Bold))
            # headItem.setForeground(QBrush(Qt.gray))
            # headItem.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            for col in range(df.shape[1]):
                print( row, col, df.loc[row][col])
                table.setColumnWidth(4, 100)
                table.setRowHeight(0, 40)
                table.setItem(row, col, QTableWidgetItem( str(df.loc[row][col])))
        # self.table.setFrameShape(QFrame.HLine)#设定样式
        # self.table.setShowGrid(False) #取消网格线
        # self.table.verticalHeader().setVisible(False) #隐藏垂直表头


        # row_count = table.rowCount()
        # table.insertRow(row_count)
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(table)
        self.setLayout(mainLayout)

        self.resize(600, 280)
        self.center()
        self.setWindowTitle("无人值守下单系统")

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    df=DBManager().read_df()
    table = TableSheet(df)
    table.show()
    sys.exit(app.exec_())
