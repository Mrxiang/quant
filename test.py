import tkinter.messagebox, os
from tkinter import *
from tkinter.ttk import *
from tkinter import Menu
import datetime
import threading
import pickle
import time
import tushare as ts
import pywinauto
import pywinauto.clipboard
import pywinauto.application

NUM_OF_STOCKS = 5  # 自定义股票数量
is_start = False
is_monitor = True
set_stocks_info = []
actual_stocks_info = []
consignation_info = []
is_ordered = [1] * NUM_OF_STOCKS  # 1：未下单  0：已下单
is_dealt = [0] * NUM_OF_STOCKS  # 0: 未成交   负整数：卖出数量， 正整数：买入数量
stock_codes = [''] * NUM_OF_STOCKS


class OperationThs:
    def __init__(self):
        try:
            self.__app = pywinauto.application.Application()
            self.__app.connect(title='网上股票交易系统5.0')
            top_hwnd = pywinauto.findwindows.find_window(title='网上股票交易系统5.0')
            dialog_hwnd = pywinauto.findwindows.find_windows(top_level_only=False, class_name='#32770', parent=top_hwnd)[0]
            wanted_hwnds = pywinauto.findwindows.find_windows(top_level_only=False, parent=dialog_hwnd)
            print('wanted_hwnds length', len(wanted_hwnds))
            # 调试用、

            if len(wanted_hwnds) == 0:
                tkinter.messagebox.showerror('错误', '无法获得“同花顺双向委托界面”的窗口句柄,请将同花顺交易系统切换到“双向委托界面”！')
                exit()

            self.__main_window = self.__app.window(handle=top_hwnd)
            self.__dialog_window = self.__app.window(handle=dialog_hwnd)


        except:
            pass

    def __buy(self, code, quantity):
        """买函数
        :param code: 代码， 字符串
        :param quantity: 数量， 字符串
        """
        self.__leftMenu('买入')
        time.sleep(0.2)
        self.__dialog_window.Edit1.SetFocus()
        time.sleep(0.2)
        self.__dialog_window.Edit1.SetEditText(code)
        time.sleep(0.2)
        if quantity != '0':
            self.__dialog_window.Edit3.SetEditText(quantity)
            time.sleep(0.2)
        self.__main_window.TypeKeys('{ENTER}')
        time.sleep(0.2)

    def __sell(self, code, quantity):
        """
        卖函数
        :param code: 股票代码， 字符串
        :param quantity: 数量， 字符串
        """
        self.__leftMenu('卖出')
        self.__dialog_window.Edit1.SetFocus()
        time.sleep(0.2)
        self.__dialog_window.Edit.SetEditText(code)
        time.sleep(0.2)
        if quantity != '0':
            self.__dialog_window.Edit3.SetEditText(quantity)
            time.sleep(0.2)
        self.__dialog_window.Button6.Click()
        time.sleep(0.2)
        self.__dialog_window.TypeKeys('{ENTER}')

    def order(self, code, direction, quantity):
        """
        下单函数
        :param code: 股票代码， 字符串
        :param direction: 买卖方向， 字符串
        :param quantity: 买卖数量， 字符串
        """
        if direction == 'B':
            self.__buy(code, quantity)
        if direction == 'S':
            self.__sell(code, quantity)
        self.__closePopupWindows()

    def maxWindow(self):
        """
        最大化窗口
        """
        if self.__main_window.GetShowState() != 3:
            self.__main_window.Maximize()
        self.__main_window.SetFocus()

    def minWindow(self):
        """
        最小化窗体
        """
        if self.__main_window.GetShowState() != 2:
            self.__main_window.Minimize()

    def __closePopupWindow(self):
        """
        关闭一个弹窗。
        :return: 如果有弹出式对话框，返回True，否则返回False
        """
        popup_hwnd = self.__main_window.PopupWindow()
        if popup_hwnd:
            popup_window = self.__app.window_(handle=popup_hwnd)
            popup_window.SetFocus()
            popup_window.Button.Click()
            return True
        return False

    def __closePopupWindows(self):
        """
        关闭多个弹出窗口
        :return:
        """
        while self.__closePopupWindow():
            time.sleep(0.5)

    def refresh(self, t=0.5):
        """
        点击刷新按钮
        :param t:刷新后的等待时间
        """
        self.__dialog_window.Button5.Click()
        time.sleep(t)

    def getMoney(self):
        """
        获取可用资金
        """
        self.__leftMenu('查询')
        time.sleep(1)
        return float(self.__dialog_window.Static4.WindowText())

    @staticmethod
    def __cleanClipboardData(data, cols=11):
        """
        清洗剪贴板数据
        :param data: 数据
        :param cols: 列数
        :return: 清洗后的数据，返回列表
        """
        lst = data.strip().split()[:-1]
        matrix = []
        for i in range(0, len(lst) // cols):
            matrix.append(lst[i * cols:(i + 1) * cols])
        return matrix[1:]

    def __copyToClipboard(self):
        """
        拷贝持仓信息至剪贴板
        :return:
        """
        self.__dialog_window.CVirtualGridCtrl.RightClick(coords=(30, 30))
        self.__main_window.TypeKeys('C')

    def __getCleanedData(self):
        """
        读取ListView中的信息
        :return: 清洗后的数据
        """
        self.__copyToClipboard()
        data = pywinauto.clipboard.GetData()
        return self.__cleanClipboardData(data)

    def __selectWindow(self, choice):
        """
        选择tab窗口信息
        :param choice: 选择个标签页。持仓，撤单，委托，成交
        :return:
        """
        rect = self.__dialog_window.CCustomTabCtrl.ClientRect()
        x = rect.width() // 8
        y = rect.height() // 2
        if choice == 'W':
            x = x
        elif choice == 'E':
            x *= 3
        elif choice == 'R':
            x *= 5
        elif choice == 'A':
            x *= 7
        self.__dialog_window.CCustomTabCtrl.ClickInput(coords=(x, y))
        time.sleep(0.5)
        """
        则边菜单窗口信息
        """

    def __leftMenu(self, keyname):
        if keyname == '买入':
            key = '{F1}'
        elif keyname == '卖出':
            key = '{F2}'
        elif keyname == '撤单':
            key = '{F2}'
        elif keyname == '查询':
            key = '{F4}'

        self.__main_window.TypeKeys(key)

    def __getInfo(self, choice):
        """
        获取股票信息
        """
        self.__selectWindow(choice=choice)
        return self.__getCleanedData()

    def getPosition(self):
        """
        获取持仓
        :return:
        """
        return self.__getInfo(choice='W')


operation = OperationThs()
operation.order('601318','S','1000')
# operation.withdrawBuy()


# print(operation.getPosition())
# print(operation.maxWindow())
# ————————————————
# 原文链接：https: // blog.csdn.net / u013040887 / article / details / 79133978