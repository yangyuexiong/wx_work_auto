# wx_work_auto

企业微信PC自动化，版本号：`4.1.39.x`

```shell
pip install -U pywinauto
```

### 消息发送(仅基础功能，暂时未对控件进行`穿透`;`降级`;`重试`;等适配处理，请自行实现)

- 先打开企业微信后再运行代码

```python
import datetime

from main import WXWorkAuto
from utils import get_pid

if __name__ == '__main__':
    app_path = "D:\WXWork\WXWork.exe"  # 安装路径
    app_pid = get_pid(name='WXWork.exe')  # 可执行文件名称
    wx_work_auto = WXWorkAuto(path=app_path)  # 实例
    wx_work_auto.send_message("yyx", f"你好:{datetime.datetime.now()}")  # 消息发送
```

### 其他功能(陆续实现...)