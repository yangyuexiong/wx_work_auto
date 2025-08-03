# -*- coding: utf-8 -*-
# @Time    : 2025/8/3 13:40
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : t2.py
# @Software: PyCharm

import uiautomation as auto

# 连接企业微信主窗口
wx = auto.WindowControl(searchDepth=1, ClassName="WeWorkWindow")
wx.SetActive()

# 找到搜索框
search_box = wx.EditControl(Name='搜索')
search_box.Click()
search_box.SendKeys('同事名字', waitTime=0.5)

# 等待搜索结果弹出，找到第一个联系人
contact = wx.ListItemControl(foundIndex=1)
contact.Click()

# 找到输入框
input_box = wx.EditControl(foundIndex=2)
input_box.Click()
input_box.SendKeys('你好，这是自动发送的消息', waitTime=0.5)

# 找到发送按钮并点击
send_button = wx.ButtonControl(Name='发送')
send_button.Click()


if __name__ == '__main__':
    pass
