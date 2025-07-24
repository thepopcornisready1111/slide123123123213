import tkinter as tk
import subprocess
import ctypes
import sys
import threading
import psutil
import json
import os
import win32api
import win32con
import win32process

# Commands for clumsy
#command1 = r'clumsy.exe --filter "outbound" --lag on --lag-time 6000'
command2 = "clumsy.exe --lag off"
command3 = r'clumsy.exe --filter "inbound" --lag on --lag-time 8000'
#retired button 1 cuz it lowkey does nothing but js in case im keeping it in
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def kill_clumsy():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'clumsy.exe' in proc.info['name']:
            print(f"Killing clumsy.exe process with PID {proc.info['pid']}")
            proc.kill()

#def button1_action():
    #print("You pressed the lag button")
    #kill_clumsy()
    #threading.Thread(target=run_cmd, args=(command1,)).start()

def button2_action():
    print("You pressed the disable button")
    kill_clumsy()
    threading.Thread(target=run_cmd, args=(command2,)).start()

def button3_action():
    print("Pressed the other lag button")
    kill_clumsy()
    threading.Thread(target=run_cmd, args=(command3,)).start()

def main():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, sys.argv[0], None, 1)
        sys.exit()

    root = tk.Tk()
    root.title("Lag switcher for steal a brainrot (Roblox)")
    root.config(bg="black")
    root.geometry("250x150")
    root.attributes("-topmost", True)

    #button1 = tk.Button(root, text="TP", command=button1_action, width=20, height=2)
    button2 = tk.Button(root, text="Fast as fuck boy", command=button3_action, width=23, height=2)
    button3 = tk.Button(root, text="Disable lag", command=button2_action, width=20, height=2)

    #button1.pack(pady=15)
    button2.pack(pady=15)
    button3.pack(pady=15)

    root.mainloop()

def run_cmd(command):
    try:
        startupinfo = win32process.STARTUPINFO()
        startupinfo.dwFlags = win32con.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = win32con.SW_HIDE

        win32process.CreateProcess(
            None,
            command,
            None, None, False,
            win32con.CREATE_NO_WINDOW,
            None, None,
            startupinfo
        )
    except Exception as e:
        print(f"Error running the command: {e}")

if __name__ == "__main__":
    main()
