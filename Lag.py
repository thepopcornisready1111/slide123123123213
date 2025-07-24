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

# Default hotkeys with 'enabled' field
default_hotkeys = {
    "button1": "F1",
    "button2": "F2",
    "button3": "F3",
    "enabled": "on"  # Hotkeys are enabled by default
}

# File where hotkeys are saved
hotkeys_file = "hotkeys.json"

# Load hotkeys from JSON file
def load_hotkeys():
    if os.path.exists(hotkeys_file):
        try:
            with open(hotkeys_file, "r") as file:
                hotkeys = json.load(file)
                if "enabled" not in hotkeys:
                    hotkeys["enabled"] = "on"
                return hotkeys
        except Exception as e:
            print(f"Error loading hotkeys: {e}")
            return default_hotkeys
    else:
        return default_hotkeys

# Save hotkeys to JSON file
def save_hotkeys(hotkeys):
    try:
        with open(hotkeys_file, "w") as file:
            json.dump(hotkeys, file)
    except Exception as e:
        print(f"Error saving hotkeys: {e}")

# Commands for clumsy
command1 = r'clumsy.exe --filter "outbound" --lag on --lag-time 6000'
command2 = "clumsy.exe --lag off"
command3 = r'clumsy.exe --filter "inbound" --lag on --lag-time 8000'

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

def button1_action():
    print("You pressed the lag button")
    kill_clumsy()
    threading.Thread(target=run_cmd, args=(command1,)).start()

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

    hotkeys = load_hotkeys()

    root = tk.Tk()
    root.title("Lag switcher for steal a brainrot (Roblox)")
    root.config(bg="black")
    root.geometry("400x300")
    root.attributes("-topmost", True)

    button1 = tk.Button(root, text="TP", command=button1_action, width=20, height=2)
    button2 = tk.Button(root, text="Less knockback/Freeze all", command=button3_action, width=23, height=2)
    button3 = tk.Button(root, text="Disable lag", command=button2_action, width=20, height=2)

    button1.pack(pady=15)
    button2.pack(pady=15)
    button3.pack(pady=15)

    if hotkeys["enabled"] == "on":
        root.bind(f"<{hotkeys['button1']}>", lambda e: button1_action())
        root.bind(f"<{hotkeys['button2']}>", lambda e: button2_action())
        root.bind(f"<{hotkeys['button3']}>", lambda e: button3_action())

    settings_button = tk.Button(root, text="Settings", command=lambda: settings_window(hotkeys))
    settings_button.pack(pady=15)

    root.mainloop()

def settings_window(hotkeys):
    settings = tk.Toplevel()
    settings.title("Settings")
    settings.geometry("350x300")

    enabled_label = tk.Label(settings, text="Hotkeys enabled:")
    enabled_label.pack(pady=5)

    enabled_var = tk.StringVar(value=hotkeys["enabled"])
    enabled_toggle = tk.Checkbutton(
        settings,
        text="Enable Hotkeys",
        variable=enabled_var,
        onvalue="on",
        offvalue="off"
    )
    enabled_toggle.pack(pady=5)

    hotkey1_label = tk.Label(settings, text="Hotkey for Button 1 (TP):")
    hotkey1_label.pack(pady=5)
    hotkey1_entry = tk.Entry(settings)
    hotkey1_entry.insert(0, hotkeys["button1"])
    hotkey1_entry.pack(pady=5)

    hotkey2_label = tk.Label(settings, text="Hotkey for Button 2 (Freeze):")
    hotkey2_label.pack(pady=5)
    hotkey2_entry = tk.Entry(settings)
    hotkey2_entry.insert(0, hotkeys["button2"])
    hotkey2_entry.pack(pady=5)

    hotkey3_label = tk.Label(settings, text="Hotkey for Button 3 (Disable Lag):")
    hotkey3_label.pack(pady=5)
    hotkey3_entry = tk.Entry(settings)
    hotkey3_entry.insert(0, hotkeys["button3"])
    hotkey3_entry.pack(pady=5)

    save_button = tk.Button(settings, text="Save Settings", command=lambda: save_settings(enabled_var, hotkey1_entry, hotkey2_entry, hotkey3_entry, hotkeys, settings))
    save_button.pack(pady=15)

def save_settings(enabled_var, hotkey1_entry, hotkey2_entry, hotkey3_entry, hotkeys, settings):
    hotkeys["enabled"] = enabled_var.get()
    hotkeys["button1"] = hotkey1_entry.get()
    hotkeys["button2"] = hotkey2_entry.get()
    hotkeys["button3"] = hotkey3_entry.get()

    save_hotkeys(hotkeys)
    settings.destroy()

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
