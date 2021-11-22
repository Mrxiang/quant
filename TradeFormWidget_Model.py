import threading
from datetime import datetime

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QHeaderView, QAbstractItemView, QLineEdit, QComboBox, QCheckBox, QTableWidgetItem, \
    QLCDNumber

import Utils
from TradeAddDialog_Model import AddStockDialog
from RecordAddDialog_Model import RecordAddDilaog
from TradeFormWidget_UI import Trade_Ui_Form
import pandas as pd

from Trader import Trader
import tushare as ts

class TradeFormWidget(QWidget, Trade_Ui_Form):
    updateSignal = pyqtSignal()  #pyqt5信号要定义为类属性
    TraderAlive = False
    def __init__(self, root):
        super(TradeFormWidget, self).__init__(root)
        self.root = root
        self.setupUi(self)
        self.initTradeForm()
        self.startRealTime()


    def initTradeForm(self):
        self.open_time = datetime.strptime(str(datetime.now().date()) + '8:00', '%Y-%m-%d%H:%M')
        self.close_time = datetime.strptime(str(datetime.now().date()) + '18:00', '%Y-%m-%d%H:%M')
        # 让内容扁平化显示，颜色同窗口标题颜色相同
        self.lcdNumber.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber.setDigitCount(8)
        self.lcdNumber.display( datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
        # 绑定事件
        self.pushButton.clicked.connect(self.addDialogShow)
        self.pushButton_2.clicked.connect(self.delete)
        self.pushButton_4.clicked.connect(self.startUnattend )
        self.pushButton_5.clicked.connect(self.tradeBuyDialogShow )
        self.pushButton_6.clicked.connect(self.tradeSellDialogShow )

        # add you code here
        print("填入数据")
        try:
            # code 列中的数据读取为str
            self.df = pd.read_csv(Utils.realstock_csv, dtype={'code':str})
        except Exception as e:
            print(e)
            self.df = pd.DataFrame(columns=Utils.column)
            self.df.to_csv(Utils.realstock_csv, index=False)
        table_rows = self.df.shape[0]
        table_columns = self.df.shape[1]
        input_table_header = self.df.columns.values.tolist()
        # 设置表格列数
        self.tableWidget.setColumnCount(table_columns)
        # 设置表格行数
        self.tableWidget.setRowCount(table_rows)
        # 给tablewidget设置行列表头========================
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        # 水平方向标签拓展剩下的窗口部分，填满表格
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # 水平方向，表格大小拓展到适当的尺寸
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for row in range(table_rows):
            for col in range(table_columns):

                if col in [7, 8, 9, 10]:
                    lineEdit = QLineEdit()
                    lineEdit.setText(str(self.df.loc[row][col]))
                    lineEdit.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    lineEdit.editingFinished.connect(self.itemEdit)
                    self.tableWidget.setCellWidget(row, col, lineEdit)

                elif col in [11]:
                    comBox = QComboBox()
                    comBox.addItems(Utils.combobox_text)
                    comboIndex = self.df.loc[row][col]
                    print(comboIndex)
                    if pd.isnull(comboIndex):
                        comboIndex = 0
                    comBox.setCurrentIndex(comboIndex)
                    comBox.currentIndexChanged.connect(self.comboChange)
                    self.tableWidget.setCellWidget(row, col, comBox)

                elif col in [13]:
                    state = self.df.loc[row][col]
                    if state != True:
                        state = False
                    print("state", state)
                    checkBox = QCheckBox()
                    checkBox.setChecked(state)
                    checkBox.stateChanged.connect(self.checkChange)
                    self.tableWidget.setCellWidget(row, col, checkBox)

                else:
                    newItem = QTableWidgetItem(str(self.df.loc[row][col]))
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget.setItem(row, col, newItem)

    def updateTradeForm(self):
        print("4. 刷新表格控件")
        print(self.df.shape, self.df)
        table_rows = self.df.shape[0]
        table_columns = self.df.shape[1]
        # 设置表格列数
        self.tableWidget.setColumnCount(table_columns)
        # 设置表格行数
        self.tableWidget.setRowCount(table_rows)

        for row in range(self.df.shape[0]):
            for col in range(2, 10):
                if col in [2, 3, 5, 6]:
                    item = self.tableWidget.item(row, col)
                    item.setText( str(self.df.loc[row][col]))
                    # newItem = QTableWidgetItem(str(self.df.loc[row][col]))
                    # self.tableWidget.setItem(row, col, newItem)
                elif  col in[4]:
                    item = self.tableWidget.item(row, col)
                    # item.setBackground( QColor(100,100,100))
                    item.setText( str(self.df.loc[row][col]))
                    # item.setBackground( QColor(255,155,155,255) )
                    item.setBackground( QColor(230,230,230,255) )
                elif col in[7]:
                    lineEditItem = self.tableWidget.cellWidget(row, col)
                    lineEditText = lineEditItem.text()

                    print( lineEditText, type(lineEditItem.text()))
                    # if pd.isnull( self.df.loc[row][col] ) :
                    #     lineEditItem.setStyleSheet("QLineEdit { background-color : black; color : gray; }")
                    # else:
                    #     textColor=255 -( float(lineEditText) -float(self.df.loc[row][4]) )/float(self.df.loc[row][4])*100
                    #     lineEditItem.setStyleSheet("QLineEdit { background-color : red; color : gray; }")

    def itemEdit(self):
        curRow = self.tableWidget.currentRow()
        curCol = self.tableWidget.currentColumn()
        print("编辑了 ", curRow, curCol)
        cell = self.tableWidget.cellWidget(curRow, curCol)
        print(type(cell), str(cell.text()))
        self.df.iloc[curRow, curCol] = str(cell.text())
        print(self.df)
        self.df.to_csv(Utils.realstock_csv, index=False)

    def checkChange(self, state):
        curRow = self.tableWidget.currentRow()
        curCol = self.tableWidget.currentColumn()
        print("选择框 ", curRow, curCol)
        cell = self.tableWidget.cellWidget(curRow, curCol)
        print(type(cell), cell.isChecked())
        self.df.iloc[curRow, curCol] = cell.isChecked()
        print(self.df)
        self.df.to_csv(Utils.realstock_csv, index=False)

    def comboChange(self, index):
        curRow = self.tableWidget.currentRow()
        curCol = self.tableWidget.currentColumn()
        print("列表框 ", curRow, curCol, index)
        cell = self.tableWidget.cellWidget(curRow, curCol)
        print(cell.currentText())
        self.df.iloc[curRow, curCol] = index
        self.df.to_csv(Utils.realstock_csv, index=False)

    def addDialogShow(self):
        print("点击了add")
        self.addDialog = AddStockDialog()
        self.addDialog.addStockSignal.connect(self.addStock)
        self.addDialog.show()

    def addStock(self, df):
        print("增加了", df)
        self.df = self.df.append(df)
        self.df.to_csv(Utils.realstock_csv, index=False)
        print("保存到csv")

    def delete(self):
        print("点击了删除")
        row = self.tableWidget.currentRow()
        print(row)
        self.tableWidget.removeRow(row)
        self.df.drop(labels=row, inplace=True)
        self.df.to_csv(Utils.realstock_csv, index=False)

    def startUnattend(self):
        print("开启无人值守")
        self.TraderAlive = True

    def stopUnattend(self):
        print("停止无人值守")
        self.TraderAlive = False

    def tradeBuyDialogShow(self):
        print("点击了买入或卖出")
        curRow = self.tableWidget.currentRow()
        if curRow == -1 :
            print("未选择一行")
        else:
            rowData=self.df.loc[curRow]

            self.traderDialog = RecordAddDilaog(0, rowData, self.root)
            self.traderDialog.show()
    def tradeSellDialogShow(self):
        print("点击了买入或卖出")
        curRow = self.tableWidget.currentRow()
        if curRow == -1 :
            print("未选择一行")
        else:
            rowData=self.df.loc[curRow]

            self.traderDialog = RecordAddDilaog(1, rowData, self.root)
            self.traderDialog.show()
    def startRealTime(self):
        print("开启实时监测")

        self.updateSignal.connect(self.updateTradeForm)
        global timer
        timer = threading.Timer(1, self.realtdata_timer)
        timer.start()

    def realtdata_timer(self):
        print("每秒钟运行检测")
        self.lcdNumber.display( datetime.now().strftime('%Y-%m-%d %H:%M:%S') )

        # 1.获取数据
        self.codelist = self.df['code'].tolist()
        print(self.codelist)
        try:
            self.realData = ts.get_realtime_quotes(self.codelist)
            self.realData = self.realData[['code', 'name', 'open', 'pre_close', 'price', 'high', 'low']]
            print("1.获取实时数据", self.realData)
            # 2. 更新df
            print("2.更新df")
            self.df['open'] = self.realData['open']
            self.df['pre_close'] = self.realData['pre_close']
            self.df['price'] = self.realData['price']
            self.df['high'] = self.realData['high']
            self.df['low'] = self.realData['low']
        except Exception as e:
            print("error",e)

        # 3. 是否执行无人值守
        if self.TraderAlive == True:
            print("3.实时交易 working")
            table_rows = self.df.shape[0]
            table_columns = self.df.shape[1]
            for index, row in self.df.iterrows():
                print(index, row)
                if row['选中'] == True:
                    # 如果交易规则是买入, 还没有执行, 当前的价格小于等于 设置的买入价格 .则执行买入
                    if row['交易规则'] == '买入' and row['执行结果'] == 'nan' and row['price'] <= row['买入价格']:
                        Trader.buy(row['code'], row['price'], row['买入数量'])
                    # 如果交易规则是先买后卖, 还没有执行, 当前的价格小于等于 设置的买入价格 .则执行买入
                    elif row['交易规则'] == '先买后卖' and row['执行结果'] == 'nan' and row['price'] <= row['买入价格']:
                        Trader.buy(row['code'], row['price'], row['买入数量'])
                    # 如果交易规则是先卖后买, 还没有执行, 当前的价格小于等于 设置的买入价格 .则执行买入
                    elif row['交易规则'] == '先卖后买' and row['执行结果'] == '已卖' and row['price'] <= row['买入价格']:
                        Trader.buy(row['code'], row['price'], row['买入数量'])

                    elif row['交易规则'] == '卖出' and row['执行结果'] == 'nan' and row['price'] >= row['卖出价格']:
                        Trader.sell(row['code'], row['price'], row['买入数量'])
                    elif row['交易规则'] == '先卖后买' and row['执行结果'] == 'nan' and row['price'] >= row['卖出价格']:
                        Trader.sell(row['code'], row['price'], row['买入数量'])
                    elif row['交易规则'] == '先买后卖' and row['执行结果'] == '已买' and row['price'] >= row['卖出价格']:
                        Trader.sell(row['code'], row['price'], row['买入数量'])
                else:
                    print("未选中")

        else:
            print("3.实时交易 Sleep")
        # 4. 是否更新表格
        print("4. 是否更新表格")
        if  datetime.now()> self.open_time and datetime.now()<self.close_time :
            self.updateSignal.emit()  # 发射信号

        global timer
        timer = threading.Timer(Utils.ticktime, self.realtdata_timer)
        timer.start()

    def stopRealTime(self):
        print("停止实时监测")
        timer.cancel()



    def closeEvent(self, event):
        print("退出主窗口")
        self.stopRealTime()
        self.df.to_csv(Utils.realstock_csv, index=False)
