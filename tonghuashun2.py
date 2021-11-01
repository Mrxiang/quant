import pywinauto
from pywinauto.application import Application
from time import sleep
from pywinauto.keyboard import send_keys

exe_path="C:/同花顺软件/同花顺/xiadan.exe"
try:
    app = pywinauto.Application().connect(path=exe_path, timeout=1)
except Exception:
    app = pywinauto.Application().start(exe_path)

win = app['网上股票交易系统5.0']
print("打印窗口")
win.print_control_identifiers()
print("开始操作")
win.set_focus()
print(win.Static4.texts())
print(win.Static6.window_text())
# print(win.Static7.texts())


send_keys('{F2}')
print("按下F2")
# sleep(0.5)
send_keys('000000')
print("输入%s" % 'code')
send_keys('{TAB}')
send_keys('{BACK 6}')
sleep(0.5)
send_keys('1.00')
send_keys('{TAB}')
sleep(0.5)
send_keys('200')
send_keys('{TAB}')
send_keys('{ENTER 3}')