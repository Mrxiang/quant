import Utils
import pandas as pd
from datetime import datetime

# from MainWindow_Model import MainWindow


class Trader:

    def __init__(self, root):
        self.root = root
        self.balance=0;
        try:
            self.df= pd.read_csv(Utils.record_csv)
        except Exception as e:
            print(e)
            self.df = pd.DataFrame(columns=Utils.record_column)
            self.df.to_csv(Utils.record_csv, index=False)
    def buy(self, code, name,  price, amount):
        print( "买入记录", code, name, price, amount)
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data =pd.DataFrame([currentTime, code, name, '买入', price, amount, 0,'']).T
        data.columns =self.df.columns
        self.df=self.df.append( data, ignore_index=True)
        print("更新记录", self.df )
        self.df.to_csv( Utils.record_csv, index=False)
        self.root.updateRecordSignal.emit( self.df )
    def sell(self, code, name,  price, amount):
        print("卖出记录", code, name, price, amount, self.df)
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = pd.DataFrame([currentTime, code, name, '卖出', price, amount, 0, '']).T
        data.columns = self.df.columns
        print("data", data)
        self.df = self.df.append(data, ignore_index=True)
        print("更新记录", self.df)
        self.df.to_csv(Utils.record_csv, index=False)
        self.root.updateRecordSignal.emit( self.df )

    def cancel(self, code, name, price, amount):
        print("撤单记录",code, name, price, amount)
        currentTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data =pd.DataFrame([currentTime, code, name, '撤单', price, amount, price*amount,'']).T
        data.columns=self.df.columns
        self.df=self.df.append( data, ignore_index=True)
        print("更新记录", self.df )
        self.df.to_csv( Utils.record_csv, index=False)
        self.root.updateRecordSignal.emit( self.df )
