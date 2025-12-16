import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
import datetime
import sys
import json
import os

class HealthReminder:
    def __init__(self):
        self.root = None
        self.settings_root = None
        self.reminder_active = True
        self.snooze_time = 0
        self.running = True
        self.config_file = "config.json"
        self.icon_file = "health_reminder.ico"  # 图标文件名
        
        # 检查配置文件是否存在，用于判断是否首次运行
        self.is_first_run = not os.path.exists(self.config_file)
        
        # 加载配置
        self.load_config()
        
        # 检查图标文件是否存在
        self.icon_path = self.get_resource_path(self.icon_file)
        
        # 如果是首次运行，创建隐藏的主窗口并打开设置窗口
        if self.is_first_run:
            self.root = tk.Tk()
            self.root.withdraw()  # 隐藏主窗口
            self.create_settings_window()
    
    def get_resource_path(self, relative_path):
        """获取资源文件的绝对路径，兼容打包后的环境"""
        try:
            # PyInstaller 创建临时文件夹，将路径存储在 _MEIPASS 中
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)
    
    def load_config(self):
        """加载配置文件"""
        default_config = {
            "days": [1, 2, 3, 4, 5],  # 周一到周五
            "morning_start": "08:30",
            "morning_end": "11:30",
            "afternoon_start": "14:00",
            "afternoon_end": "18:00",
            "reminder_interval": 60,  # 分钟
            "snooze_duration": 5  # 分钟
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = default_config
                self.save_config()
        except:
            self.config = default_config
    
    def save_config(self):
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except:
            pass
    
    def create_reminder_window(self):
        if self.root is not None and self.root.winfo_exists():
            return
            
        if self.root is None or not self.root.winfo_exists():
            self.root = tk.Tk()
            
        self.root.title("健康提醒")
        self.root.geometry("300x150")
        
        # 设置窗口图标
        if os.path.exists(self.icon_path):
            self.root.iconbitmap(self.icon_path)
        
        # 居中显示窗口
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # 添加提醒文本
        label = tk.Label(self.root, text="该活动一下了，喝口水吧", font=("Arial", 14))
        label.pack(pady=20)
        
        # 添加按钮框架
        button_frame = tk.Frame(self.root)
        button_frame.pack()
        
        # 添加"我知道了"按钮
        ok_button = tk.Button(button_frame, text="我知道了", command=self.close_reminder, width=10)
        ok_button.pack(side=tk.LEFT, padx=10)
        
        # 添加"过会再提醒"按钮
        snooze_button = tk.Button(button_frame, text="过会再提醒", command=self.snooze_reminder, width=10)
        snooze_button.pack(side=tk.LEFT, padx=10)
        
        # 添加"设置"按钮
        settings_button = tk.Button(self.root, text="设置", command=self.open_settings)
        settings_button.pack(pady=10)
        
        # 窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.close_reminder)
        
        self.root.mainloop()
    
    def create_settings_window(self):
        if self.settings_root is not None and self.settings_root.winfo_exists():
            return
            
        if self.settings_root is None or not self.settings_root.winfo_exists():
            self.settings_root = tk.Toplevel()
            
        self.settings_root.title("提醒设置")
        self.settings_root.geometry("400x500")
        
        # 设置窗口图标
        if os.path.exists(self.icon_path):
            self.settings_root.iconbitmap(self.icon_path)
        
        # 居中显示窗口
        self.settings_root.update_idletasks()
        width = self.settings_root.winfo_width()
        height = self.settings_root.winfo_height()
        x = (self.settings_root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.settings_root.winfo_screenheight() // 2) - (height // 2)
        self.settings_root.geometry(f'{width}x{height}+{x}+{y}')
        
        # 创建设置界面
        self.create_settings_ui()
        
        # 窗口关闭事件
        self.settings_root.protocol("WM_DELETE_WINDOW", self.on_settings_close)
        
        self.settings_root.mainloop()
    
    def create_settings_ui(self):
        # 创建主框架
        main_frame = ttk.Frame(self.settings_root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 星期选择
        days_frame = ttk.LabelFrame(main_frame, text="提醒星期", padding="10")
        days_frame.pack(fill=tk.X, pady=5)
        
        self.day_vars = []
        days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        
        for i, day in enumerate(days):
            var = tk.IntVar(value=1 if (i+1) in self.config["days"] else 0)
            self.day_vars.append(var)
            cb = ttk.Checkbutton(days_frame, text=day, variable=var)
            cb.grid(row=i//4, column=i%4, sticky=tk.W, padx=5, pady=2)
        
        # 时间设置
        time_frame = ttk.LabelFrame(main_frame, text="提醒时间", padding="10")
        time_frame.pack(fill=tk.X, pady=5)
        
        # 上午时间
        ttk.Label(time_frame, text="上午:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(time_frame, text="开始:").grid(row=0, column=1, sticky=tk.W, pady=2)
        self.morning_start_var = tk.StringVar(value=self.config["morning_start"])
        morning_start_entry = ttk.Entry(time_frame, textvariable=self.morning_start_var, width=8)
        morning_start_entry.grid(row=0, column=2, padx=5, pady=2)
        
        ttk.Label(time_frame, text="结束:").grid(row=0, column=3, sticky=tk.W, pady=2)
        self.morning_end_var = tk.StringVar(value=self.config["morning_end"])
        morning_end_entry = ttk.Entry(time_frame, textvariable=self.morning_end_var, width=8)
        morning_end_entry.grid(row=0, column=4, padx=5, pady=2)
        
        # 下午时间
        ttk.Label(time_frame, text="下午:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Label(time_frame, text="开始:").grid(row=1, column=1, sticky=tk.W, pady=2)
        self.afternoon_start_var = tk.StringVar(value=self.config["afternoon_start"])
        afternoon_start_entry = ttk.Entry(time_frame, textvariable=self.afternoon_start_var, width=8)
        afternoon_start_entry.grid(row=1, column=2, padx=5, pady=2)
        
        ttk.Label(time_frame, text="结束:").grid(row=1, column=3, sticky=tk.W, pady=2)
        self.afternoon_end_var = tk.StringVar(value=self.config["afternoon_end"])
        afternoon_end_entry = ttk.Entry(time_frame, textvariable=self.afternoon_end_var, width=8)
        afternoon_end_entry.grid(row=1, column=4, padx=5, pady=2)
        
        # 提醒间隔
        interval_frame = ttk.LabelFrame(main_frame, text="提醒设置", padding="10")
        interval_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(interval_frame, text="提醒间隔(分钟):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.interval_var = tk.IntVar(value=self.config["reminder_interval"])
        interval_spinbox = ttk.Spinbox(interval_frame, from_=1, to=120, textvariable=self.interval_var, width=10)
        interval_spinbox.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(interval_frame, text="稍后提醒(分钟):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.snooze_var = tk.IntVar(value=self.config["snooze_duration"])
        snooze_spinbox = ttk.Spinbox(interval_frame, from_=1, to=60, textvariable=self.snooze_var, width=10)
        snooze_spinbox.grid(row=1, column=1, padx=5, pady=2)
        
        # 按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        save_button = ttk.Button(button_frame, text="保存", command=self.save_settings)
        save_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = ttk.Button(button_frame, text="取消", command=self.close_settings)
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def save_settings(self):
        """保存设置"""
        try:
            # 保存星期设置
            self.config["days"] = [i+1 for i, var in enumerate(self.day_vars) if var.get() == 1]
            
            # 保存时间设置
            self.config["morning_start"] = self.morning_start_var.get()
            self.config["morning_end"] = self.morning_end_var.get()
            self.config["afternoon_start"] = self.afternoon_start_var.get()
            self.config["afternoon_end"] = self.afternoon_end_var.get()
            
            # 保存提醒设置
            self.config["reminder_interval"] = self.interval_var.get()
            self.config["snooze_duration"] = self.snooze_var.get()
            
            # 保存到文件
            self.save_config()
            
            messagebox.showinfo("成功", "设置已保存")
            self.close_settings()
        except Exception as e:
            messagebox.showerror("错误", f"保存设置失败: {str(e)}")
    
    def on_settings_close(self):
        """设置窗口关闭时的处理"""
        if self.is_first_run:
            # 如果是首次运行且用户关闭了设置窗口，询问是否退出程序
            result = messagebox.askyesno("退出", "您尚未保存设置，是否退出程序？")
            if result:
                self.close_settings()
                if self.root:
                    self.root.destroy()
                sys.exit(0)
            else:
                # 用户选择不退出，重新显示设置窗口
                return
        self.close_settings()
    
    def close_settings(self):
        if self.settings_root:
            self.settings_root.destroy()
            self.settings_root = None
        
        # 如果是首次运行且设置窗口已关闭，销毁隐藏的主窗口
        if self.is_first_run and self.root:
            self.root.destroy()
            self.root = None
            self.is_first_run = False
    
    def open_settings(self):
        self.create_settings_window()
    
    def close_reminder(self):
        if self.root:
            self.root.destroy()
            self.root = None
        self.reminder_active = True
    
    def snooze_reminder(self):
        if self.root:
            self.root.destroy()
            self.root = None
        self.reminder_active = False
        self.snooze_time = time.time() + (self.config["snooze_duration"] * 60)  # 使用配置的稍后时间
    
    def check_time(self):
        while self.running:
            now = datetime.datetime.now()
            current_time = now.time()
            current_day = now.weekday() + 1  # 1是周一，7是周日
            
            # 检查是否是设置的提醒日
            is_reminder_day = current_day in self.config["days"]
            
            # 解析时间字符串
            morning_start = datetime.datetime.strptime(self.config["morning_start"], "%H:%M").time()
            morning_end = datetime.datetime.strptime(self.config["morning_end"], "%H:%M").time()
            afternoon_start = datetime.datetime.strptime(self.config["afternoon_start"], "%H:%M").time()
            afternoon_end = datetime.datetime.strptime(self.config["afternoon_end"], "%H:%M").time()
            
            # 检查是否在指定时间段内
            in_morning = morning_start <= current_time <= morning_end
            in_afternoon = afternoon_start <= current_time <= afternoon_end
            
            # 检查是否到了提醒时间
            minutes_since_hour = now.minute
            should_remind = (minutes_since_hour % self.config["reminder_interval"] == 0)
            
            # 检查是否需要提醒
            need_remind = (is_reminder_day and (in_morning or in_afternoon) and 
                          should_remind and self.reminder_active)
            
            # 检查是否过了推迟时间
            if not self.reminder_active and time.time() >= self.snooze_time:
                self.reminder_active = True
            
            # 如果需要提醒，创建提醒窗口
            if need_remind:
                self.create_reminder_window()
                self.reminder_active = False  # 防止同一间隔内多次提醒
            
            # 每分钟检查一次
            time.sleep(60)
    
    def start(self):
        # 如果不是首次运行，启动时间检查线程
        if not self.is_first_run:
            # 在新线程中运行时间检查
            self.thread = threading.Thread(target=self.check_time)
            self.thread.daemon = True
            self.thread.start()
        
        try:
            # 保持主线程运行
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.running = False
            sys.exit(0)

if __name__ == "__main__":
    reminder = HealthReminder()
    reminder.start()