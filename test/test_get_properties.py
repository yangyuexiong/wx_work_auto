# -*- coding: utf-8 -*-
# @Time    : 2025/8/3 2:19
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_send_message.py
# @Software: PyCharm

def test(wx_work_auto):
    """
    调试代码
    :return:
    """
    print(wx_work_auto.main_dlg)
    print(wx_work_auto.main_dlg.children())

    # if hasattr(wx_work_auto.main_dlg, 'refresh'):
    #     wx_work_auto.main_dlg.refresh()
    #     print("refresh")

    # print(wx_work_auto.main_dlg.__dir__())
    # print(wx_work_auto.main_dlg.__dict__)
    for child in wx_work_auto.main_dlg.children():
        print(f"get_properties: {child.get_properties()}")
        print(f"控件类型: {child.friendly_class_name()}")
        print(f"标题: {child.window_text()}")
        print(f"自动化ID: {child.automation_id()}")
        print("-" * 50)

    main_window = wx_work_auto.app.window(class_name="WeWorkWindow", visible_only=True)
    print(main_window)

    # 方法1：直接查找内容容器（企业微信4.1典型结构）
    content = main_window.child_window(
        class_name="QWidget",  # 企业微信主内容区类名
        control_type="Pane",
        found_index=0
    )
    print(content)

    if content.exists():
        real_content = content.wrapper_object()  # 获取实际控件对象
        print("成功穿透装饰层，内容区域属性：")
        print(f"类名: {real_content.class_name()}")
        print(f"矩形区域: {real_content.rectangle()}")
        print(f"子控件数: {len(real_content.children())}")
    else:
        print("穿透失败，尝试备用方案...")

    # WXWorkDict.DLG_DICT.get("主窗口")
    # parent_hwnd = findwindows.find_windows(title="企业微信", class_name="WeWorkWindow")[0]
    # child_windows = findwindows.find_windows(parent=parent_hwnd)
    #
    # for hwnd in child_windows:
    #     print(f"子窗口句柄: {hwnd}")
    #     print(f"标题: {win32gui.GetWindowText(hwnd)}")
    #     print(f"类名: {win32gui.GetClassName(hwnd)}")
    #     print("-" * 50)


if __name__ == '__main__':
    pass
