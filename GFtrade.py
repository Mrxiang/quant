
from pywinauto.application import Application
from time import sleep
from pywinauto.keyboard import send_keys
# app = Application(backend='win32').start(r"C:\Windows\System32\notepad.exe")
# app = Application().connect(path=r"C:\Windows\System32\notepad.exe")
# mainwin = app['无标题 - 记事本']
# mainwin.Edit.type_keys("自动化输入第一行", with_spaces = True)
# mainwin.child_window(class_name="Edit").type_keys("{ENTER} 自动化输入第二行", with_spaces = True)
# mainwin.print_control_identifiers()
#
# mainwin.menu_select('文件 -> 保存')
# app['另存为']['文件名 Edit'].set_text(r'temptest_pywapywa.txt')
# app['另存为']['保存 Button'].click()
# mainwin.print_control_identifiers()
# app['确认另存为']['是 Button'].click()
# app.top_window().type_keys('%FX')


def start():
    while True:
        try:
            app = Application().start("C:/同花顺软件/同花顺/xiadan.exe", timeout=10)
            win =app.top_window()
            print("打开应用")
            return app, win
        except Exception as e:
            print(e)
            app =Application().connect(path="C:/同花顺软件/同花顺/xiadan.exe")
            win = app.top_window()

            print("连接到应用")
            # app.kill()
            return  app, win


class Trader:
    @staticmethod
    def buy( code: str, price: float, amount: int ):
        print("开始下单买入 code %s  %f %d" %('code', price,amount))
        code = str( code )
        price = str( price)
        amount = str( amount)
        app, win =start()
        sleep(0.5)
        try:
            win.set_focus()
            sleep(0.5)
            send_keys('{F2}')
            print("按下F2")
            sleep(0.5)
            send_keys(code)
            print("输入%s"%'code')
            send_keys('{TAB}')
            send_keys('{BACK 6}')
            sleep(0.5)
            send_keys(price)
            send_keys('{TAB}')
            sleep(0.5)
            send_keys(amount)
            send_keys('{TAB}')
            send_keys('{ENTER 3}')
            # app.kill()
            return  'buy ok'
        except Exception as e:
            app.kill()
            return  e
    def sell(code:str, price: float,amount :int ):
        print('price %f' % price)


if __name__ =='__main__':
    trader = Trader()
    trader.buy('000000',2.99,100)