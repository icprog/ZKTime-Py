# ZKTime-Py
中控科技考勤管理系统——考勤数据读取自动化脚本
==============


[setup](https://github.com/liucaide/ZKTime-Py/blob/master/checking/setup.py)
主程序入口类

[attendance_read](https://github.com/liucaide/ZKTime-Py/blob/master/checking/attendance_read.py)
考勤数据读取类

[uploading](https://github.com/liucaide/ZKTime-Py/blob/master/checking/uploading.py)
API 数据上传类

[cd_tools](https://github.com/liucaide/ZKTime-Py/blob/master/checking/cd_tools.py)
工具类


项目引入了一下第三方库

pywin32      :python 链接 C 语言类库文件
```
pip install pywin32
```
schedule     ：定时任务
```
pip install schedule
```
requests     ：网络服务
```
pip install requests
```

exe 构建 使用 pyinstaller
```
pip install pyinstaller
```
使用 pyinstaller 构建 弹出终端的exe
```
pyinstaller -F setup.py
```
使用 pyinstaller 构建 不弹出终端的exe
```
pyinstaller --windowed --onefile --clean --noconfirm setup.py
```

其他文件

[http_server](https://github.com/liucaide/ZKTime-Py/blob/master/checking/http_server.py)
web http接口服务类

[zk_read](https://github.com/liucaide/ZKTime-Py/blob/master/checking/zk_read.py)
考情数据读取 副本
