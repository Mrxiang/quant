import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QHeaderView, QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets

import Utils
from MainWindow_UI import Ui_MainWindow

import pandas as pd

from RecordFormWidget_Model import RecordFormWidget
from TradeFormWidget_Model import TradeFormWidget


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.initWindow()

    def initWindow(self):
        print("init main window")
        # self.tab = QtWidgets.QWidget()
        _translate = QtCore.QCoreApplication.translate

        self.setWindowTitle(_translate("MainWindow", "貔貅"))
        self.tab = TradeFormWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        # self.tab_2 = QtWidgets.QWidget()
        self.tab_2 = RecordFormWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "监测"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "记录"))
        self.tabWidget.setCurrentIndex(0)

    def closeEvent(self,event):
        print("窗体关闭")