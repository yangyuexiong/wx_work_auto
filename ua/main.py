# -*- coding: utf-8 -*-
# @Time    : 2025/8/3 13:22
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : main.py
# @Software: PyCharm

import subprocess
import time

import uiautomation as auto


class WXWorkAutomator:
    def __init__(self):
        self.wx_window = None
        self.process_id = None

    def start_wxwork(self, path=None):
        """启动企业微信"""
        wx_path = path or r"C:\Program Files (x86)\WXWork\WXWork.exe"
        try:
            subprocess.Popen(wx_path)
            print("启动企业微信中...")
            time.sleep(5)  # 等待启动完成
        except Exception as e:
            print(f"启动失败: {e}")
            raise

    def connect(self, timeout=30):
        """连接企业微信窗口"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            self.wx_window = auto.WindowControl(
                Name="企业微信",
                ClassName="WeWorkWindow",
                searchDepth=1
            )
            if self.wx_window.Exists():
                self.process_id = self.wx_window.ProcessId
                print(f"已连接企业微信 (PID: {self.process_id})")
                return True
            time.sleep(1)
        raise TimeoutError("连接企业微信超时")

    def maximize_window(self):
        """最大化窗口 - 修正后的版本"""
        if self.wx_window.Exists():
            # 获取窗口当前位置和大小
            rect = self.wx_window.BoundingRectangle
            screen_width, screen_height = auto.GetScreenSize()

            # 如果窗口不是最大化状态，则最大化它
            if rect.width < screen_width - 100 or rect.height < screen_height - 100:
                # 使用窗口模式操作最大化
                maximize_btn = self.wx_window.ButtonControl(
                    Name="最大化",
                    searchDepth=2
                )
                if maximize_btn.Exists():
                    maximize_btn.Click()
                else:
                    # 备选方案：发送快捷键
                    self.wx_window.SendKeys('{Win}{Up}')
                time.sleep(1)
            return True
        return False

    def navigate_to_tab(self, tab_name):
        """导航到指定标签页(消息/通讯录/工作台)"""

        tab = self.wx_window.ButtonControl(
            Name=tab_name,
            searchDepth=3,
            foundIndex=1  # 第一个匹配的按钮
        )
        print(tab)
        print(tab.Exists())

        if tab.Exists():
            tab.Click()
            time.sleep(1.5)  # 等待页面切换
            return True
        return False

    def search_contact(self, name):
        """搜索联系人"""

        if not self.navigate_to_tab("通讯录"):
            return False

        search_box = self.wx_window.EditControl(
            Name="搜索",
            searchDepth=4
        )
        if search_box.Exists():
            search_box.SendKeys('^a{Backspace}' + name)  # 先清空再输入
            time.sleep(1)

            contact = self.wx_window.ListItemControl(
                Name=name,
                searchDepth=5
            )
            if contact.Exists():
                contact.Click()
                time.sleep(0.5)
                return True
        return False

    def send_message(self, text):
        """发送文本消息"""
        input_area = self.wx_window.EditControl(
            Name="输入消息",
            searchDepth=5
        )
        if input_area.Exists():
            input_area.SendKeys(text)

            send_btn = self.wx_window.ButtonControl(
                Name="发送",
                searchDepth=4
            )
            if send_btn.Exists():
                send_btn.Click()
            else:
                input_area.SendKeys("{Enter}")
            time.sleep(0.5)
            return True
        return False

    def close_popups(self):
        """关闭可能的弹窗"""
        popup = self.wx_window.WindowControl(
            Name="提示",
            searchDepth=2
        )
        if popup.Exists():
            confirm_btn = popup.ButtonControl(
                Name="确定",
                searchDepth=2
            )
            if confirm_btn.Exists():
                confirm_btn.Click()
                time.sleep(0.5)


if __name__ == "__main__":
    automator = WXWorkAutomator()

    try:
        # 1. 启动并连接
        automator.start_wxwork("D:\WXWork\WXWork.exe")
        if automator.connect():
            # 2. 最大化窗口
            # automator.maximize_window()

            # 3. 关闭可能的弹窗
            # automator.close_popups()

            # 4. 搜索联系人并发送消息
            contact_name = "yyx"  # 替换为实际联系人
            if automator.search_contact(contact_name):
                automator.send_message("这是一条自动化测试消息")
                # automator.send_file(r"C:\test.txt")  # 如需发送文件取消注释
                print("消息发送成功")
            else:
                print(f"未找到联系人: {contact_name}")

    except Exception as e:
        print(f"自动化执行失败: {str(e)}")
    finally:
        print("自动化流程结束")
