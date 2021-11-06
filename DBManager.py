

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine



class DBManager():
    def __init__(self):
        print("初始化db")
        self.column=['代码','名字','上个交易日收盘价格','开盘价格','买入价格','买入数量','卖出价格','卖出数量','交易顺序']
        self.engine = create_engine('sqlite:///report.db')

    def read_df(self):
        print("读取数据")
        df=pd.DataFrame(columns=self.column)
        print(df)
        try:
            sql_cmd = "SELECT * FROM real_data"
            df = pd.read_sql(sql=sql_cmd, con=self.engine)
        except:
            print("db empty")
            df = pd.DataFrame( columns=self.column)
        print(df)
        return  df
    def  save_df(self, df):
        print("保存数据")
        df.to_sql("real_data", self.engine, if_exists='replace')


if __name__ == '__main__':
    df = DBManager().read_df()
    print( df )
    if df.size==0 :
        data = [[1,'Alice','100'],[2,'Bob','200'],[3,'Cindy','300'],[4,'Eric','300'],[5,'Helen','300'],[6,'Grace ','300']]
        df = pd.DataFrame( data,columns=['代码','名字','价格'])
    print(df)
    DBManager().save_df(df)