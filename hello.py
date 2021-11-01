
from pywinauto.application import Application

try:
    app = Application().connect(path=r"C:\Windows\System32\notepad.exe")
    print("连接notepad ")
except:
    print("打开notepad")
    app = Application(backend='win32').start(r"C:\Windows\System32\notepad.exe")
windows=app.windows()
print("打印窗口")
print( windows )
mainwin = app['无标题 - 记事本']
print("打印控件")
mainwin.print_control_identifiers()
mainwin.Edit.type_keys("自动化输入第一行", with_spaces = True)
mainwin.child_window(class_name="Edit").type_keys("{ENTER} 自动化输入第二行", with_spaces = True)

mainwin.menu_select('文件 -> 保存')
app['另存为']['文件名 Edit'].set_text(r'temptest_pywapywa.txt')
app['另存为']['保存 Button'].click()
print("打印控件")
mainwin.print_control_identifiers()

app['确认另存为']['是 Button'].click()
# app.top_window().type_keys('%FX')
# from pywinauto.application import Application
# app = Application(backend="uia").start("notepad.exe")
#
# # app['无标题 - 记事本'].type_keys("%FX")
# mainwin = app.window(title='无标题 - 记事本')
#
# # mainwin.menu_select('帮助 -> 关于记事本')
# # mainwin.print_control_identifiers()
# #
# # app['Dialog'].wait('visible')
# # app['Dialog']['确定'].click()
#
# mainwin.Edit.type_keys("自动化输入第一行", with_spaces = True)
# # mainwin.child_window(class_name="Edit").type_keys("{ENTER} 自动化输入第二行", with_spaces = True)
# # mainwin.Edit.type_keys("{ENTER} 自动化输入第二行", with_spaces = True)
# mainwin.menu_select('文件 -> 保存')
# app['另存为']['文件名 Edit'].set_text(r'./temptest_pywapywa.txt')
# app['另存为']['保存 Button'].click()
# app['pywa.txt - 记事本'].type_keys('%FX')
# # from subprocess import Popen
# # from pywinauto import Desktop
# #
# # Popen('calc.exe', shell=True)
# # dlg = Desktop(backend="uia").Calculator
# # dlg.wait('visible')