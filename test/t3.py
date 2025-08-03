# -*- coding: utf-8 -*-
# @Time    : 2025/8/3 14:03
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : t3.py
# @Software: PyCharm


import os
import time

import pyautogui
import uiautomation as auto

# 配置图片路径
ASSET_DIR = os.path.join(os.path.dirname(__file__), '../assets')


def find_and_click(image_name, confidence=0.8, click_offset=(0, 0)):
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


def main():
    print("开始执行企业微信自动发消息...")

    # 确保企业微信窗口置前
    wx_window = auto.GetForegroundControl()
    print(f"当前前台窗口: {wx_window.Name} | {wx_window.ClassName}")

    # 等待企业微信稳定
    time.sleep(1)

    # 1. 点击搜索框
    find_and_click('txl.png', confidence=0.9)

    # 2. 输入联系人名称
    pyautogui.write('测试联系人', interval=0.05)
    pyautogui.press('enter')
    time.sleep(1)

    # 3. 点击聊天输入框
    # find_and_click('message_input_box.png', confidence=0.9)

    # 4. 输入消息内容
    # pyautogui.write('你好，这是一条自动化消息', interval=0.05)
    # pyautogui.press('enter')

    print("消息发送完成！")


if __name__ == "__main__":
    main()
