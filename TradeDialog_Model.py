from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog

from TradeDialog_UI import Trade_Ui_Dialog
from Trader import Trader


class TradeDialog(QDialog,Trade_Ui_Dialog):

    def __init__(self, tabIndex, data):
        super(TradeDialog,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("自定义消息对话框：登录窗口")

        # init TradeDialog
        self.tabWidget.setCurrentIndex( tabIndex)
        print( data )
        # self.pushButton.clicked.connect( self.sure )
        # self.lineEdit.editingFinished.connect( self.editing )
        # self.lineEdit.textChanged.connect( self.textChange )

        if tabIndex==0:
            self.lineEdit.setText( str(data['code']) )
            self.lineEdit_2.setText( str(data['name']) )
            self.lineEdit_3.setText( str(data['price']) )
            self.lineEdit_4.setText( str(data['买入数量']) )
            # self.lineEdit_3.setText( )
            self.pushButton.clicked.connect( self.sureBuy)
            self.pushButton_2.clicked.connect( self.close )
        else:
            self.lineEdit_5.setText( str(data['code']) )
            self.lineEdit_6.setText( str(data['name']) )
            self.lineEdit_7.setText( str(data['price']) )
            self.lineEdit_8.setText( str(data['卖出数量']) )
            # self.lineEdit_9.setText()
            self.pushButton_3.clicked.connect( self.sureSell)
            self.pushButton_4.clicked.connect( self.close )

    def sureBuy(self):
        print("确认买入")
        self.code = self.lineEdit.text()
        self.name = self.lineEdit_2.text()
        self.price = self.lineEdit_3.text()
        self.amount = self.lineEdit_4.text()
        self.trader = Trader()
        self.trader.buy(self.code,self.name, self.price, self.amount)
        self.close()
    def sureSell(self):
        print("确认卖出")
        self.code = self.lineEdit_5.text()
        self.name = self.lineEdit_6.text()
        self.price = self.lineEdit_7.text()
        self.amount = self.lineEdit_8.text()
        self.trader = Trader()
        self.trader.sell(self.code, self.name, self.price, self.amount)
        self.close()