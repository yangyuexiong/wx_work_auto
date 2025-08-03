# -*- coding: utf-8 -*-
# @Time    : 2025/8/3 4:04
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : t1.py
# @Software: PyCharm

import time

from pywinauto.timings import Timings

from main import WXWorkAuto
from utils import get_pid

# 设置全局超时时间
Timings.window_find_timeout = 2  # 单位：秒


# 方法1：通过进程ID直接访问内部控件
def get_real_content(main_win):
    # 获取企业微信渲染进程
    from pywinauto.findwindows import find_elements
    content_window = find_elements(
        process=main_win.process_id(),
        class_name="CChatCtrl",
        control_type="Pane",
        depth=3  # 搜索深度
    )
    return content_window[0] if content_window else None


# 方法2：坐标穿透（最后手段）
def click_through_decorations():
    rect = main_win.rectangle()
    # 企业微信4.1.39内容区域典型坐标
    click_points = [
        (rect.left + 100, rect.top + 150),  # 左侧导航
        (rect.left + 300, rect.top + 200)  # 主消息区
    ]
    for x, y in click_points:
        main_win.click_input(coords=(x, y))
        time.sleep(0.5)


def get_unread_messages():
    try:
        # 激活消息标签
        try:
            main_win.child_window(
                title="消息",
                control_type="TabItem"
            ).click_input()
        except:
            main_win.type_keys("^t")  # Ctrl+T切换

        time.sleep(1)

        # 获取消息容器
        container = get_real_content()
        if not container:
            click_through_decorations()
            container = get_real_content()

        if container:
            # 滚动加载
            for _ in range(2):
                container.scroll("down", "page")
                time.sleep(0.5)

            # 识别未读消息
            unreads = []
            badges = container.descendants(
                control_type="Text",
                name_re="[0-9]+条?未读?"
            )

            for badge in badges:
                try:
                    msg_item = badge.parent().parent()
                    sender = msg_item.children()[0].window_text()
                    content = msg_item.children()[1].window_text()
                    count = int(''.join(filter(str.isdigit, badge.window_text())))

                    unreads.append({
                        "sender": sender,
                        "preview": content,
                        "count": count,
                        "element": badge
                    })
                except Exception as e:
                    print(f"解析错误: {str(e)}")

            return unreads

    except Exception as e:
        print(f"致命错误: {str(e)}")
        # generate_heatmap()
        return []


"""
使用标准 Win32 控件（而非 4.x 的 DirectUI）
"""
if __name__ == '__main__':
    app_path = "D:\WXWork\WXWork.exe"
    app_pid = get_pid(name='WXWork.exe')
    wx_work_auto = WXWorkAuto(path=app_path)

    main_win = wx_work_auto.main_dlg

    print("主窗口标题:", main_win.window_text())
    print("窗口句柄:", main_win.handle)

    print(main_win.__dir__())
    print(main_win.__dict__)

    # child_controls = main_win.children()
    #
    # # 打印子控件信息
    # for i, child in enumerate(child_controls):
    #     print(f"子控件 {i}:")
    #     print(f"  类名: {child.class_name()}")
    #     print(f"  控件类型: {child.friendly_class_name()}")
    #     print(f"  标题: {child.window_text()}")
    #     print(f"  是否可见: {child.is_visible()}")
    #     print("-" * 30)

    # all_controls = main_win.descendants()
    #
    # # 打印控件信息（限制前20个以避免过多输出）
    # for i, ctrl in enumerate(all_controls[:20]):
    #     print(f"控件 {i}:")
    #     print(f"  类名: {ctrl.class_name()}")
    #     print(f"  类型: {ctrl.friendly_class_name()}")
    #     print(f"  标题: {ctrl.window_text()}")
    #     print(f"  AutomationID: {ctrl.automation_id()}")
    #     print("-" * 30)

    # 定位左侧导航栏（通常包含消息、通讯录等入口）
    # left_nav = main_win.child_window(
    #     class_name="NavCtrl",
    #     control_type="Pane"
    # )
    #
    # print(left_nav)
    #
    # # 定位主消息区域
    # msg_area = main_win.child_window(
    #     class_name="CChatCtrl",
    #     control_type="Pane"
    # )
    # print(msg_area)

    # 定位未读标记（通常为红色数字）
    # unread_badges = main_win.descendants(
    #     control_type="Text",
    #     name_re="[0-9]+"  # 匹配数字
    # )

    print(get_real_content(main_win))
