import psutil
import tkinter as tk
from tkinter import ttk, Toplevel, Text, Checkbutton, PhotoImage
from threading import Thread
import pystray
from PIL import Image, ImageDraw
from pystray import MenuItem as item

class NetworkMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("traffic")
        #self.root.geometry("157x28")  # 增加窗口宽度，适应并排显示
        
        root.overrideredirect(True)  # 去掉标题栏和边框
        self.root.attributes('-topmost', True)  # 默认置顶屏幕

        # 透明度
        self.opacity = tk.DoubleVar(value=0.6)
        self.root.wm_attributes('-alpha', self.opacity.get()) # 设置半透明 0 - 1

        # 初始化上传和下载数据
        self.upload_speed = tk.StringVar(value="↑: 0 MB/s") # 上传速度
        self.download_speed = tk.StringVar(value="↓: 0 MB/s")   # 下载速度
        self.total_sent = tk.StringVar(value="↑↑: 0 MB")    # 上传总量
        self.total_received = tk.StringVar(value="↓↓: 0 MB") # 下载总量

        # 初始化是否置顶状态
        self.is_topmost = tk.BooleanVar(value=False)

        # 选项状态（是否显示各项内容）
        self.show_download_speed = tk.BooleanVar(value=True)
        self.show_upload_speed = tk.BooleanVar(value=True)
        self.show_total_received = tk.BooleanVar(value=True)
        self.show_total_sent = tk.BooleanVar(value=True)

        # 设置 GUI 元素
        self.setup_ui()

        # 开始监控网络
        self.running = True
        self.prev_counters = psutil.net_io_counters()
        self.update_network_data()

        # 设置系统托盘图标
        self.setup_tray_icon()

        # 添加拖动功能
        self.drag_data = {"x": 0, "y": 0}
        self.root.bind("<Button-1>", self.on_drag_start)  # 鼠标按下
        self.root.bind("<B1-Motion>", self.on_drag_motion)  # 鼠标拖动

    def setup_ui(self):
        # 创建一个框架来管理并排布局
        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        # 上传速度显示
        upload_label = ttk.Label(frame, textvariable=self.upload_speed, font=("Arial", 8), foreground="blue")
        upload_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")

        # 上传总量显示
        total_sent_label = ttk.Label(frame, textvariable=self.total_sent, font=("Arial", 8), foreground="purple")
        total_sent_label.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        # 下载速度显示 (并排显示)
        download_label = ttk.Label(frame, textvariable=self.download_speed, font=("Arial", 8), foreground="green")
        download_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")

        # 总接收量显示 (并排显示)
        total_received_label = ttk.Label(frame, textvariable=self.total_received, font=("Arial", 8), foreground="black")
        total_received_label.grid(row=1, column=1, padx=5, pady=2, sticky="e")

        # 列宽相同
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

    def update_network_data(self):
        if not self.running:
            return

        # 获取当前网络流量数据
        counters = psutil.net_io_counters()
        sent = counters.bytes_sent
        recv = counters.bytes_recv

        # 计算速度
        sent_speed = (sent - self.prev_counters.bytes_sent) / 1024 / 1024  # MB/s
        recv_speed = (recv - self.prev_counters.bytes_recv) / 1024 / 1024  # MB/s

        # 更新上次记录的 counters
        self.prev_counters = counters

        # 更新 Tkinter 显示的数据
        # self.upload_speed.set(f"↑: {sent_speed:.2f} MB/s")
        # self.download_speed.set(f"↓: {recv_speed:.2f} MB/s")
        # self.total_received.set(f"↓↓: {recv / 1024 / 1024:.2f} MB")
        # self.total_sent.set(f"↑↑: {sent / 1024 / 1024:.2f} MB")
        # 更新 Tkinter 显示的数据，根据复选框状态控制显示
        if self.show_upload_speed.get():
            self.upload_speed.set(f"↑: {sent_speed:.2f} MB/s")
        else:
            self.upload_speed.set("")

        if self.show_download_speed.get():
            self.download_speed.set(f"↓: {recv_speed:.2f} MB/s")
        else:
            self.download_speed.set("")

        if self.show_total_sent.get():
            self.total_sent.set(f"↑↑: {sent / 1024 / 1024:.2f} MB")
        else:
            self.total_sent.set("")

        if self.show_total_received.get():
            self.total_received.set(f"↓↓: {recv / 1024 / 1024:.2f} MB")
        else:
            self.total_received.set("")

        # 每秒更新一次
        self.root.after(1000, self.update_network_data)

    def setup_tray_icon(self):
        # 创建托盘图标图像
        #image = Image.new('RGB', (64, 64), color=(73, 109, 137))
        #draw = ImageDraw.Draw(image)
        #draw.ellipse((16, 16, 48, 48), fill="white")
        image = Image.open("icon.ico")


        # 创建托盘菜单
        menu = pystray.Menu(
            item('Edit', lambda icon, item: self.show_editor()),
            item('Show', lambda icon, item: self.show_window()),
            item('Quit', lambda icon, item: self.quit_application())
        )

        # 初始化系统托盘图标
        self.tray_icon = pystray.Icon("network_monitor", image, "Network Monitor", menu)
        tray_thread = Thread(target=self.tray_icon.run)
        tray_thread.start()

    def toggle_topmost(self):
        # 切换置顶状态
        self.is_topmost.set(not self.is_topmost.get())
        self.root.attributes('-topmost', self.is_topmost.get())

    def show_window(self):
        # 显示窗口
        self.root.deiconify()
    
    def show_editor(self):
        # 显示编辑窗口
        editor_window = Toplevel(self.root)
        editor_window.title("编辑")
        editor_window.geometry("300x200")

        # 编辑窗口标题栏图标
        icno_image = PhotoImage(file="icon.ico")
        editor_window.iconphoto(True, icno_image)

        # 添加滑块来调整透明度
        ttk.Label(editor_window, text="设置透明度:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        opacity_scale = ttk.Scale(
            editor_window, from_=0.1, to=1.0, variable=self.opacity,
            orient="horizontal", command=self.adjust_opacity
        )
        opacity_scale.grid(row=0, column=1, padx=10, pady=5, sticky="w")

         # 添加复选框
        ttk.Checkbutton(editor_window, text="显示实时下载速度", variable=self.show_download_speed).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Checkbutton(editor_window, text="显示实时上传速度", variable=self.show_upload_speed).grid(row=1, column=1, padx=10, pady=5, sticky="e")
        ttk.Checkbutton(editor_window, text="显示下载总量", variable=self.show_total_received).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        ttk.Checkbutton(editor_window, text="显示上传总量", variable=self.show_total_sent).grid(row=2, column=1, padx=10, pady=5, sticky="w")
        

    def adjust_opacity(self, value):
        self.root.attributes('-alpha', float(value))

    def quit_application(self):
        # 停止更新并退出应用
        self.running = False
        self.tray_icon.stop()
        self.root.quit()

    def hide_window(self):
        # 隐藏窗口
        self.root.withdraw()

    def on_drag_start(self, event):
        # 记录鼠标点击的位置
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_drag_motion(self, event):
        # 计算窗口新位置并更新
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]
        new_x = self.root.winfo_x() + delta_x
        new_y = self.root.winfo_y() + delta_y
        self.root.geometry(f"+{new_x}+{new_y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkMonitorApp(root)
    root.protocol("WM_DELETE_WINDOW", app.hide_window)  # 点击关闭按钮时隐藏窗口而非退出
    root.mainloop()
