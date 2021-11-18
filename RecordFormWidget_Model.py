from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLCDNumber, QAbstractItemView, QHeaderView, QTableWidgetItem

import Utils
from RecordFormWidget_UI import Record_Ui_Form
import pandas as pd

class RecordFormWidget(QWidget, Record_Ui_Form):
    def __init__(self, parent=None):
        super(RecordFormWidget, self).__init__(parent)
        self.setupUi(self)
        self.initRecordForm()
    def initRecordForm(self):
        self.lcdNumber.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber.setDigitCount(8)
        self.lcdNumber.display( datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
        try:
            self.df= pd.read_csv(Utils.record_csv)
        except Exception as e:
            print(e)
            self.df = pd.DataFrame(columns=Utils.record_column)
            self.df.to_csv(Utils.record_csv, index=False)
        table_rows = self.df.shape[0]
        table_columns= self.df.shape[1]
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
                newItem = QTableWidgetItem(str(self.df.loc[row][col]))
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(row, col, newItem)