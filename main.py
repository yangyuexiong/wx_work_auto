# -*- coding: utf-8 -*-
# @Time    : 2025/8/3 2:17
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : main.py
# @Software: PyCharm

import time

from pywinauto import Application, findwindows
from pywinauto.keyboard import send_keys


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
