# -*- coding: utf-8 -*-
# @Time    : 2025/8/3 2:17
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : utils.py
# @Software: PyCharm

import psutil


def get_pid(name: str):
    for proc in psutil.process_iter():
        try:
            if proc.name().lower() == name.lower():
                print(proc.pid)
                return proc.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return -1
