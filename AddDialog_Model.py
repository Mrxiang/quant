from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QCompleter

import Utils
from AddDialog_UI import Ui_Dialog
import tushare as ts
import pandas as pd

items_list=["C","C++","JavaScript","C#"]

class AddStockDialog(QDialog,Ui_Dialog):
    addStockSignal = pyqtSignal( object )

    def __init__(self):
        super(AddStockDialog,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("自定义消息对话框：登录窗口")
        self.pushButton.clicked.connect( self.sure )
        self.lineEdit.editingFinished.connect( self.editing )
        self.lineEdit.textChanged.connect( self.textChange )
    def sure(self):
        print("确认")
        name = str(self.lineEdit.text())
        print(name)
        try:
            new_df = ts.get_realtime_quotes(name)
            print(new_df)
            new_df2 = pd.DataFrame( columns=Utils.column )
            new_df2.code = new_df.code
            new_df2.name = new_df.name
            print("new df", new_df2 )
            self.addStockSignal.emit( new_df2)
            self.close()
        except Exception as e:
            print(e)
    def editing(self):
        print(self.lineEdit.text())


    def textChange(self):
        print("text changed")
        print(self.lineEdit.text())
        # 增加自动补全
        self.completer = QCompleter(items_list)
        # 设置匹配模式  有三种： Qt.MatchStartsWith 开头匹配（默认）  Qt.MatchContains 内容匹配  Qt.MatchEndsWith 结尾匹配
        self.completer.setFilterMode(Qt.MatchContains)
        # 设置补全模式  有三种： QCompleter.PopupCompletion（默认）  QCompleter.InlineCompletion   QCompleter.UnfilteredPopupCompletion
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        # 给lineedit设置补全器
        self.lineEdit.setCompleter(self.completer)


# https://www.jianshu.com/p/60561380f789