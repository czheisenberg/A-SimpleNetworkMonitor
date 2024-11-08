# A Simple Network Monitor

这是一个简单的网络监视器 —— 悬浮窗


一个用Python编写的简单网络监控工具，显示实时下载速度↓和本次开机以用流量数量↓↓，该工具使用“Tkinter”作为图形用户界面(GUI)，使用“psutil”获取网络统计数据，使用“pystray”进行系统托盘集成。

## 特征

- 实时网速监控: ↓ 和 ↓↓
- 应用半透明并指定显示。
- 便于访问的系统托盘图标。

## 依赖

要运行该应用程序，您需要安装以下Python库:

- `psutil` – 用于收集系统和网络统计信息。
- `pystray` – 用于创建系统托盘图标和菜单。
- `Tkinter` – 用于创建GUI(通常预装Python)。

## 运行

```bash
python3 app.py
```
 - 运行后可自由拖动更改位置。

## Releases
 - 前往 [Releases](https://github.com/czheisenberg/A-SimpleNetworkMonitor/releases/tag/0.1)  页面下载可执行程序，同时确保icon.ico在可执行程序的同一目录下。
![](./images/3.png)

## 效果
 - 半透明悬浮窗.

![](./images/1.png)

![](./images/2.png)

 - 任务栏右键图标可选择: Show 和 Quit
![](./images/show-quit.png)

---
---
---

## v0.2
 - 调低了透明度
 - 添加：实时上传速度与上传总量， 两行显示
### 运行效果
![](./images/v0.2.png)

---
---
---

## v0.3
 - 新增可自定义设置是否显示：实时下载速度，实时上传速度，下载总量，上传总量以及自定义透明度。
 - 右键系统托盘中图标点击 Edit
![](./images/v0.3-Edit.png)
 - 点击 Edit 后弹出 编辑界面
![](./images/v0.3-Edit-main.png)
 - 此时可根据需要进行调整。