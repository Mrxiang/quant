
import pywinauto
from pywinauto.application import Application
from time import sleep
from pywinauto.keyboard import send_keys

#

class User:
    def __init__(self):
        self.balance=0
        self.exe_path = "C:/同花顺软件/同花顺/xiadan.exe"
    def buy(self, code, price, amount ):
        print("buy code :%s price: %s amount: %s " %(code ,price ,amount))
        try:
            app = pywinauto.Application().connect(path=self.exe_path, timeout=10)
        except Exception:
            app = pywinauto.Application().start(self.exe_path)

        win = app['网上股票交易系统5.0']
        print("打印窗口")
        win.set_focus()
        win.wait('visible')
        print("开始操作")
        send_keys('{F1}')
        print("按下F1买入")
        sleep(0.5)
        win['证券代码Edit'].draw_outline('red')
        win['证券代码Edit'].set_focus()
        send_keys(code)
        send_keys('{TAB}')
        send_keys(price)
        send_keys('{TAB}')
        send_keys(amount)
        win['买入Button'].draw_outline('green')
        if( win['买入Button'].is_enabled() ):
            win['买入Button'].click()
            send_keys('^y')
        else:
            print("买入失败")
        print("买入完成")
    def sell(self, code, price, amount ):
        print("sell code :%s price: %s amount: %s " % (code , price , amount))
        print("buy code :%s price: %s amount: %s " %(code ,price ,amount))
        try:
            app = pywinauto.Application().connect(path=self.exe_path, timeout=10)
        except Exception:
            app = pywinauto.Application().start(self.exe_path)

        win = app['网上股票交易系统5.0']
        print("打印窗口")
        win.set_focus()
        win.wait('visible')
        print("开始操作")
        send_keys('{F2}')
        print("按下F2卖出")
        sleep(0.5)
        win['证券代码Edit'].draw_outline('red')
        win['证券代码Edit'].set_focus()
        send_keys(code)
        send_keys('{TAB}')
        send_keys(price)
        send_keys('{TAB}')
        send_keys(amount)
        win['卖出Button'].draw_outline('green')
        win['卖出Button'].click()
        send_keys('^y')
        print("卖出完成")
    def cancel(self, code, price, amount):
        print("cancel code :%s price: %s amount: %s " %( code , price , amount))


user = User()
user.buy('100000','1.00','100')
