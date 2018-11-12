# ZKTime-Py
中控科技考勤管理系统——考勤数据读取自动化脚本
==============
各模块介绍
==============
[attendance_read]()
考勤数据读取类

[setup]()
主程序入口类

[uploading]()
API 数据上传类

[cd_tools]()
工具类

[dist 文件夹]()
构建exe 存放文件夹

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

其他辅助类文件

[http_server]()
web http接口服务类

[zk_read]()
考情数据读取 副本
