# 健康提醒小程序

一个可自定义参数的桌面健康提醒小程序，使用 Python 和 tkinter 开发。

## 功能特点
- ⏰ 可自定义提醒时间（星期、时间段）
- 🔄 可设置提醒频率（每30分钟-3小时）
- 💤 支持"过会再提醒"功能
- 🎨 支持自定义图标
- ⚙️ 可视化设置界面
- 💾 自动保存配置

## 使用方法
- 安装依赖
```bash
pip install pyinstaller
```
## 运行程序
```bash
python health_reminder.py
```
首次运行会弹出设置窗口，根据需要配置提醒参数
打包为可执行文件
```bash
pyinstaller --onefile --windowed --icon=health_reminder.ico health_reminder.py
```

## 配置说明
在设置窗口中可以配置：

提醒星期：选择需要提醒的星期（周一至周日）
提醒时间：设置每天的提醒时间段（上午和下午）
提醒间隔：设置提醒频率（每30分钟、1小时、2小时、3小时）
稍后时间：点击"过会再提醒"后的等待时间（1-60分钟）

## 系统要求
Python 3.8+
Windows/Linux/macOS
tkinter（通常已内置）

## 许可证
MIT License
