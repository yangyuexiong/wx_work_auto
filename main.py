# -*- coding: utf-8 -*-
# @Time    : 2025/8/3 2:17
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : main.py
# @Software: PyCharm

import os
import time

import pyautogui
from pywinauto import Application, findwindows
from pywinauto.keyboard import send_keys

ASSET_DIR = os.path.join(os.path.dirname(__file__), 'assets')


class WXWorkDict:
    ENTER = "{ENTER}"
    MESSAGE_KEY = "^1"
    CONTACTS_KEY = "^8"
    CF = "^f"
    ESC = "{ESC}"
    DLG_DICT = {
        "主窗口": {
            "title": "企业微信",
            "class_name": "WeWorkWindow"
        },
        "通讯录": {
            "title": "企业微信-通讯录",
            "class_name": "WXworkWindow - 企业微信-通讯录"
        },
    }


class WXWorkAuto:
    """企业微信4.1.39.x"""

    def __init__(self, path: str):
        self.app = Application(backend='uia').start(path)
        if not self.app.windows():
            self.app = Application(backend='uia').connect(path=path)

        self.main_dlg = None
        self.init_dlg = self.gen_dlg(widget_key="主窗口")

    def gen_dlg(self, widget_key: str):
        """
        切换当前窗口
        :param widget_key:
        :return:
        """

        widget_obj = WXWorkDict.DLG_DICT.get(widget_key)
        if not widget_obj:
            raise KeyError("not widget_key")

        title = widget_obj.get('title')
        class_name = widget_obj.get('class_name')
        dlg_handles = findwindows.find_windows(title=title, class_name=class_name)

        if dlg_handles:
            # self.main_dlg = self.app.window_(handle=dlg_handles[0])
            self.main_dlg = self.app.window(handle=dlg_handles[0])
            self.main_dlg.wait('ready', timeout=10)
            self.main_dlg.restore()
            self.main_dlg.set_focus()
            return self.main_dlg
        else:
            raise IndexError(f'获取 {title} 窗口失败')

    def close(self, *args, **kwargs):
        """
        最小化，关闭，杀进程等逻辑，自行实现...
        :param args:
        :param kwargs:
        :return:
        """

        send_keys(WXWorkDict.ESC)

    def find_and_click(self, image_name, confidence=0.8, click_offset=(0, 0)):
        """
        在屏幕上找图片，并点击
        """

        image_path = os.path.join(ASSET_DIR, image_name)
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)

        if location is None:
            raise Exception(f'无法找到 {image_name}，请检查截图是否正确。')

        # 计算点击点
        center_x, center_y = pyautogui.center(location)
        click_x = center_x + click_offset[0]
        click_y = center_y + click_offset[1]

        pyautogui.moveTo(click_x, click_y, duration=0.2)
        pyautogui.click()
        time.sleep(0.5)

    def message_tab(self):
        """消息"""

        self.main_dlg.type_keys(WXWorkDict.MESSAGE_KEY)

    def contacts_tab(self):
        """通讯录"""

        self.main_dlg.type_keys(WXWorkDict.CONTACTS_KEY)

    def send_message(self, name: str, message: str):
        """

        :param name: 用户(未去重)
        :param message: 消息
        :return:
        """

        self.message_tab()
        self.main_dlg.type_keys(WXWorkDict.CF)
        send_keys(name)
        time.sleep(1)
        send_keys(WXWorkDict.ENTER)
        send_keys(message)
        send_keys(WXWorkDict.ENTER)
        print(f"{name} 消息已发完成")
        self.close()
        print("最小化")

    def test_c(self):
        """测试组合点击"""

        self.find_and_click("txl.png")
        self.find_and_click("txl_search.png")
        send_keys("yyx")
        time.sleep(1)
        send_keys(WXWorkDict.ENTER)
        send_keys("组合测试")
        send_keys(WXWorkDict.ENTER)
