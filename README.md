# wx_work_auto

企业微信PC自动化

- 版本号：`3.1.10.x`
- 版本号：`4.1.39.x`

- 企业微信4.1是`DirectUI`技术（也有一些自己定制的控件容器，例如 WeWorkWindow, PerryShadowWnd），这些控件不暴露标准的`UI
  Automation Patterns`（如 Invoke、Value、TextPattern 等），导致大多数自动化工具无法直接操控它，DirectUI（自绘界面）**
  不走标准Windows控件体系，很多控件并不是独立的 UI Automation 元素。
    - 解决方案一：组合键+穿透
    - 解决方案二：降低到`3.1.10`使用`pywinauto`平滑处理
    - 解决方案三：使用`uiautomation`+`PyAutoGUI`以及图像识别，坐标处理（不稳定，易受分辨率、颜色变化等因素影响）

```shell
pip install -U pywinauto
pip install uiautomation
pip install pyautogui
```

### 消息发送(仅基础功能，暂时未对控件进行`穿透`;`降级`;`重试`;等适配处理，请自行实现)

- 先打开企业微信后再运行代码

```python
import datetime

from main import WXWorkAuto
from utils import get_pid

if __name__ == '__main__':
    app_path = "D:\WXWork\WXWork.exe"  # 安装路径
    app_pid = get_pid(name='WXWork.exe')  # 可执行文件名称，获取进程ID在后续的操作中进行控件窗口的切换等相关操作
    wx_work_auto = WXWorkAuto(path=app_path)  # 实例
    wx_work_auto.send_message("yyx", f"你好:{datetime.datetime.now()}")  # 消息发送

    # UI + 坐标的模式
    # wx_work_auto.test_c()
```

- UI点击方法（有几率被检测导致强退，后续优化）
    - 通讯录：`self.find_and_click("txl.png")`
    - 通讯录-搜索：`self.find_and_click("txl_search.png")`
    - 其他参照例子自行补充

### 其他功能(陆续实现...)