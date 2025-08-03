# -*- coding: utf-8 -*-
# @Time    : 2025/8/3 2:19
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_send_message.py
# @Software: PyCharm

import datetime

from main import WXWorkAuto
from utils import get_pid

if __name__ == '__main__':
    app_path = "D:\WXWork\WXWork.exe"
    app_pid = get_pid(name='WXWork.exe')
    wx_work_auto = WXWorkAuto(path=app_path)
    # wx_work_auto.send_message("yyx", f"你好:{datetime.datetime.now()}")

    wx_work_auto.test_c()
