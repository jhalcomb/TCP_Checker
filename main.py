import tkinter as tk
from tkinter import ttk
import threading
from test_open_port import checkHost

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


class Root(tk.Tk): 
    def __init__(self): 
        super().__init__()
        self.title("TCP Port Checker")
        self.windowNum = 0

        self.frame_list = []

        self.mainframe = MainFrame(self)
        self.frame_list.append(self.mainframe)
        self.settingsframe = SettingsFrame(self)
        self.frame_list.append(self.settingsframe)

        self.frame_list[1].forget()  # Hide settings window at first

        self.mainframe.pack()  # Show MainWindow at first

    def switchmainframe(self):
        self.frame_list[self.windowNum].forget()
        self.windowNum = (self.windowNum + 1) % len(self.frame_list)
        self.frame_list[self.windowNum].tkraise()
        self.frame_list[self.windowNum].pack()


class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.IpInputFrame = IpInputFrame(self)
        self.IpInputFrame.pack()

        self.PortInputFrame = PortInputFrame(self)
        self.PortInputFrame.pack()

        self.CheckFrame = CheckFrame(self)
        self.CheckFrame.pack()

        self.ResultFrame = ResultFrame(self)
        self.ResultFrame.pack()

        StatusBarFrame(self).pack()


class MainSettingsFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.SettingsFrame = SettingsFrame(self.MainSettingsFrame)
        self.SettingsFrame.pack()


class IpInputFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.user_input = tk.StringVar()
        self.user_input.set("google.com") # Set Default Value
        label = ttk.Label(self, text="Enter IP", padding=(5, 1))
        entry = ttk.Entry(self, textvariable=self.user_input)
        label.grid()
        entry.grid()


class PortInputFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.user_input = tk.StringVar()
        self.user_input.set("443") # Set Default Value
        label = ttk.Label(self, text="Port", padding=(5, 1))
        entry = ttk.Entry(self, textvariable=self.user_input)
        label.grid()
        entry.grid()


class CheckFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.button = ttk.Button(self, text="Check", command=self.check, padding=(5, 5))
        self.button.grid(pady=15)

    def check(self, *args):
        root.mainframe.ResultFrame.result.set("Connecting...")
        root.mainframe.ResultFrame.label.configure(foreground="#f49855", font=("segoe UI", 12))
        self.button["state"] = "disabled"  # disable until response returns

        ip = root.mainframe.IpInputFrame.user_input.get()
        port = root.mainframe.PortInputFrame.user_input.get()
        retry = int(root.settingsframe.user_retry.get())
        delay = int(root.settingsframe.user_interval.get())
        timeout = int(root.settingsframe.user_timeout.get())

        x = threading.Thread(target=checkHost, args=(self, root, ip, port, retry, delay, timeout,))
        x.start()


class ResultFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.result = tk.StringVar()
        self.label = ttk.Label(self, textvariable=self.result, wraplength=300)
        self.label.grid()


class StatusBarFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.button = ttk.Button(self, text=">", width=5, command=lambda: root.switchmainframe())
        self.button.pack(pady=10)


class SettingsFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # Retry Field
        self.user_retry = tk.StringVar()
        self.user_retry.set("3")  # Set Default Value
        self.retry_label = ttk.Label(self, text="Retry (times)", padding=(5, 1), font=("segoe UI", 10))
        self.retry_entry = ttk.Entry(self, textvariable=self.user_retry)
        self.retry_label.grid()
        self.retry_entry.grid()

        # Interval Field
        self.user_interval = tk.StringVar()
        self.user_interval.set("5")  # Set Default Value
        self.interval_label = ttk.Label(self, text="Interval (sec)", padding=(5, 1), font=("segoe UI", 10))
        self.interval_entry = ttk.Entry(self, textvariable=self.user_interval)
        self.interval_label.grid()
        self.interval_entry.grid()

        # Timeout Field
        self.user_timeout = tk.StringVar()
        self.user_timeout.set("3")  # Set Default Value
        self.timeout_label = ttk.Label(self, text="Timeout (sec)", padding=(5, 1), font=("segoe UI", 10))
        self.timeout_entry = ttk.Entry(self, textvariable=self.user_timeout)
        self.timeout_label.grid()
        self.timeout_entry.grid()

        # Message
        msg = "Can also use a hostname if the host is able to resolve it."
        self.label = ttk.Label(self, text=msg, padding=(5, 1), wraplength=300, font=("segoe UI", 10))
        self.button = ttk.Button(self, text="<", width=5, command=lambda: root.switchmainframe())
        self.label.grid()
        self.button.grid(pady=22)



root = Root()
root.geometry("400x300")
style = ttk.Style(root)
style.configure("TLabel", font=("segoe UI", 14))
# Keyboard Binding
root.bind("<Return>", root.mainframe.CheckFrame.check)
root.resizable(False, False)
root.mainloop()
