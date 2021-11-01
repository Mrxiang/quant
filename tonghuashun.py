import pywinauto
from pywinauto.application import Application
from time import sleep
from pywinauto.keyboard import send_keys

exe_path="C:/同花顺软件/同花顺/xiadan.exe"
try:
    app = pywinauto.Application().connect(path=exe_path, timeout=1)
except Exception:
    app = pywinauto.Application().start(exe_path)
# app = Application().start("C:/同花顺软件/同花顺/xiadan.exe", timeout=10)
# app = Application().connect(path="")
# app.__getattribute__()
# win =app.top_window()
# win =app.windows()
win = pywinauto.findwindows.find_window(title='网上股票交易系统5.0')
print("打印窗口")
print( win )
dialog_hwnd = pywinauto.findwindows.find_windows(top_level_only=False, class_name='#32770', parent=win)[0]
wanted_hwnds = pywinauto.findwindows.find_windows(top_level_only=False, parent=dialog_hwnd)
dialog_window = app.window(handle=dialog_hwnd)
dialog_window.print_control_identifiers()
print("打开应用")
dialog_window.set_focus()

# afxwnd = app['窗格']
# afxwnd.print_control_identifiers()
# sleep(0.5)
send_keys('{F2}')
print("按下F2")
# sleep(0.5)
send_keys('00000')
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