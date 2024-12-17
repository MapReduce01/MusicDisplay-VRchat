import argparse
from pythonosc import udp_client
import time
import json
import tkinter as tk
import os
from tkinter import *
from tkinter import ttk
import time
import json
import pywinauto
import threading
from clicknium import clicknium as cc
import psutil
import tkinter.messagebox as msgbox


class Console(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.output = tk.Text(self, width=80, height=45)
        self.output.pack(side=tk.LEFT)

        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.output.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.output.configure(yscrollcommand=self.scrollbar.set)

        sys.stdout = self
        sys.stderr = self

    def write(self, txt):
        self.output.insert(tk.END,str(txt))
        self.update_idletasks()

decoder = json.JSONDecoder()

def get_history_file():
    path = os.path.join(os.path.expanduser('~'), r'AppData\Local\Netease\CloudMusic\webdata\file')
    if os.path.exists(path):
        return path
    else:
        print('cloudmusic data folder not found')
        exit(1)


def get_playing(path):
    track_info = dict()
    with open(path, encoding='utf-8') as f:
        read_string = f.read(3200)
        for _ in range(4):
            try:
                read_string += f.read(500)
                decoded_json = decoder.raw_decode(read_string[1:])
                track_info.update(decoded_json[0])
                break
            except json.JSONDecodeError:
                pass

    if not track_info:
        return None

    track_name = track_info['track']['name']
    artist_list = [i['name'] for i in track_info['track']['artists']]

    return track_name, artist_list

path = get_history_file()
history_file_path = path + '\history'

msg = ["", True]

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=9000,help="The port the OSC server is listening on")
args = parser.parse_args()
client = udp_client.SimpleUDPClient(args.ip, args.port)
title = ""

def start_function():
    def fetchstart2():
        global current_player
        global netease_status
        global Chrome_status
        global Edge_status
        global plugin_status

        if combo.get() == '网易云':
            try:
                if netease_status == 0:
                    print('processing netease')
                    current_player = '网易云'
                    title = ""
                    count = 0
                    if "cloudmusic.exe" not in (p.name() for p in psutil.process_iter()):
                        showMessage('网易云未运行')
                    else:
                        while (master.title() == '辣鸡软件') and (current_player == '网易云') and ("cloudmusic.exe" in (p.name() for p in psutil.process_iter())):
                            netease_status = 1
                            Chrome_status = 0
                            Edge_status = 0
                            try:
                                song, artists = get_playing(history_file_path)
                                music = f'{song} - {" / ".join(artists)}'
                                if (title != "♫ Now playing:  " + music):
                                    title = "♫ Now playing:  " + music
                                    msg[0] = f"{title}"
                                    client.send_message("/chatbox/input", msg)
                                elif (count > 15 or count == 15):
                                    title = "♫ Now playing:  " + music
                                    msg[0] = f"{title}"
                                    client.send_message("/chatbox/input", msg)
                                    count = 0
                                else:
                                    pass
                            except PermissionError:
                                pass
                            time.sleep(1)
                            count = count + 1
                else:
                    print('Not processing 网易云，Thread already existed')
            except:
                print('processing netease')
                current_player = '网易云'
                title = ""
                count = 0
                if "cloudmusic.exe" not in (p.name() for p in psutil.process_iter()):
                    showMessage('网易云未运行')
                else:
                    while (master.title() == '辣鸡软件') and (current_player == '网易云') and ("cloudmusic.exe" in (p.name() for p in psutil.process_iter())):
                        netease_status = 1
                        Chrome_status = 0
                        Edge_status = 0
                        try:
                            song, artists = get_playing(history_file_path)
                            music = f'{song} - {" / ".join(artists)}'
                            if (title != "♫ Now playing:  " + music):
                                title = "♫ Now playing:  " + music
                                msg[0] = f"{title}"
                                client.send_message("/chatbox/input", msg)
                            elif (count > 15 or count == 15):
                                title = "♫ Now playing:  " + music
                                msg[0] = f"{title}"
                                client.send_message("/chatbox/input", msg)
                                count = 0
                            else:
                                pass
                        except PermissionError:
                            pass
                        time.sleep(1)
                        count = count + 1

        elif combo.get() == 'Chrome':
            try:
                if Chrome_status == 0:
                    print('processing Chrome')
                    current_player = 'Chrome'
                    title = ""
                    count = 0
                    if "chrome.exe" not in (p.name() for p in psutil.process_iter()):
                        showMessage('Chrome未运行')
                    else:
                        while (master.title() == '辣鸡软件') and (current_player == 'Chrome') and ("chrome.exe" in (p.name() for p in psutil.process_iter())):
                            netease_status = 0
                            Chrome_status = 1
                            Edge_status = 0
                            try:
                                desktop = pywinauto.Desktop(backend="uia")
                                window = desktop.windows(title_re=".* Google Chrome$", control_type="Pane")[0]
                                wrapper_list = window.descendants(control_type="TabItem")
                                music = wrapper_list[0].window_text()
                                if (music != "All") and (title != "♫ Now playing:  " + music):
                                    title = "♫ Now playing:  " + music
                                    msg[0] = f"{title}"
                                    client.send_message("/chatbox/input", msg)
                                elif (music != "All") and (count > 15 or count == 15):
                                    title = "♫ Now playing:  " + music
                                    msg[0] = f"{title}"
                                    client.send_message("/chatbox/input", msg)
                                    count = 0
                                else:
                                    pass
                            except:
                                current_player = ""
                                Chrome_status = 0
                            time.sleep(1)
                            count = count + 1
                else:
                    print('Not processing Chrome，Thread already existed')
            except:
                print('processing Chrome')
                current_player = 'Chrome'
                title = ""
                count = 0
                if "chrome.exe" not in (p.name() for p in psutil.process_iter()):
                    showMessage('Chrome未运行')
                else:
                    while (master.title() == '辣鸡软件') and (current_player == 'Chrome') and ("chrome.exe" in (p.name() for p in psutil.process_iter())):
                        netease_status = 0
                        Chrome_status = 1
                        Edge_status = 0
                        try:
                            desktop = pywinauto.Desktop(backend="uia")
                            window = desktop.windows(title_re=".* Google Chrome$", control_type="Pane")[0]
                            wrapper_list = window.descendants(control_type="TabItem")
                            music = wrapper_list[0].window_text()
                            if (music != "All") and (title != "♫ Now playing:  " + music):
                                title = "♫ Now playing:  " + music
                                msg[0] = f"{title}"
                                client.send_message("/chatbox/input", msg)
                            elif (music != "All") and (count > 15 or count == 15):
                                title = "♫ Now playing:  " + music
                                msg[0] = f"{title}"
                                client.send_message("/chatbox/input", msg)
                                count = 0
                            else:
                                pass
                        except:
                            current_player = ""
                            Chrome_status = 0
                        time.sleep(1)
                        count = count + 1

        else:
            try:
                if Edge_status == 0:
                    print('processing Edge')
                    current_player = 'Edge'
                    title = ""
                    count = 0
                    if "Clicknium.Web.NativeMessageHost.exe" not in (p.name() for p in psutil.process_iter()):
                        showMessage('Edge未运行')
                    else:
                        while (master.title() == '辣鸡软件') and (current_player == 'Edge') and (current_player == 'Edge') and ("Clicknium.Web.NativeMessageHost.exe" in (p.name() for p in psutil.process_iter())):
                            netease_status = 0
                            Chrome_status = 0
                            Edge_status = 1
                            try:
                                if plugin_status == 1:
                                    for browser in cc.edge.browsers:
                                        for tab in browser.tabs:
                                            music = tab.title
                                            break
                                    if (music != "All") and (title != "♫ Now playing:  " + music):
                                        title = "♫ Now playing:  " + music
                                        msg[0] = f"{title}"
                                        client.send_message("/chatbox/input", msg)
                                    elif (music != "All") and (count > 15 or count == 15):
                                        title = "♫ Now playing:  " + music
                                        msg[0] = f"{title}"
                                        client.send_message("/chatbox/input", msg)
                                        count = 0
                                    else:
                                        pass

                            except:
                                if cc.edge.extension.is_installed() == False:
                                    cc.edge.extension.install_or_update()
                                plugin_status = 1
                                for browser in cc.edge.browsers:
                                    for tab in browser.tabs:
                                        music = tab.title
                                        break
                                if (music != "All") and (title != "♫ Now playing:  " + music):
                                    title = "♫ Now playing:  " + music
                                    msg[0] = f"{title}"
                                    client.send_message("/chatbox/input", msg)
                                elif (music != "All") and (count > 15 or count == 15):
                                    title = "♫ Now playing:  " + music
                                    msg[0] = f"{title}"
                                    client.send_message("/chatbox/input", msg)
                                    count = 0
                                else:
                                    pass
                            time.sleep(1)
                            count = count + 1
                else:
                    print('Not processing Edge，Thread already existed')
            except:
                print('processing Edge')
                current_player = 'Edge'
                title = ""
                count = 0
                if "Clicknium.Web.NativeMessageHost.exe" not in (p.name() for p in psutil.process_iter()):
                    showMessage('Edge未运行')
                else:
                    while (master.title() == '辣鸡软件') and (current_player == 'Edge') and ("Clicknium.Web.NativeMessageHost.exe" in (p.name() for p in psutil.process_iter())):
                        netease_status = 0
                        Chrome_status = 0
                        Edge_status = 1
                        try:
                            if plugin_status == 1:
                                for browser in cc.edge.browsers:
                                    for tab in browser.tabs:
                                        music = tab.title
                                        break
                                if (music != "All") and (title != "♫ Now playing:  " + music):
                                    title = "♫ Now playing:  " + music
                                    msg[0] = f"{title}"
                                    client.send_message("/chatbox/input", msg)
                                elif (music != "All") and (count > 15 or count == 15):
                                    title = "♫ Now playing:  " + music
                                    msg[0] = f"{title}"
                                    client.send_message("/chatbox/input", msg)
                                    count = 0
                                else:
                                    pass

                        except:
                            if cc.edge.extension.is_installed() == False:
                                cc.edge.extension.install_or_update()
                            plugin_status = 1
                            for browser in cc.edge.browsers:
                                for tab in browser.tabs:
                                    music = tab.title
                                    break
                            if (music != "All") and (title != "♫ Now playing:  " + music):
                                title = "♫ Now playing:  " + music
                                msg[0] = f"{title}"
                                client.send_message("/chatbox/input", msg)
                            elif (music != "All") and (count > 15 or count == 15):
                                title = "♫ Now playing:  " + music
                                msg[0] = f"{title}"
                                client.send_message("/chatbox/input", msg)
                                count = 0
                            else:
                                pass
                        time.sleep(1)
                        count = count + 1

    threading.Thread(target=fetchstart2).start()

def readmeclick():
    console = Console()
    console.pack(fill='both', expand=True)
    print('若要显示Chrome页面不要将Chrome最小化'+'\n' + '\n' + '使用Chrome和Edge时需把想要显示的Tab移到最前，只会读取第一个Tab'+'\n'
          + '\n' +'使用Edge时，如未安装Clicknium插件，第一次运行系统会弹窗提示安装，进入Edge右上角会提示启用插件，启用后重启Edge即可')

def restart_program():
    current_player = ""

def showMessage(message, timeout=1500):
    root = tk.Tk()
    root.withdraw()
    root.after(timeout, root.destroy)
    msgbox.showinfo('Info', message, master=root)


master = tk.Tk()
master.title("辣鸡软件")
master.iconbitmap("logo.ico")
# master.geometry("500x300")
combo = ttk.Combobox(master,font=("微软雅黑", 16), width=30)
combo["values"] = ("网易云", "Chrome", "Microsoft Edge")
combo.current(0)
combo.pack()

startButton = tk.Button(master, text='Start', font=("Arial", 26), command=lambda:start_function())
startButton.pack()
restart_button = tk.Button(master, text='Stop', font=("微软雅黑", 16), command=lambda:restart_program())
restart_button.pack()
# readme = tk.Button(master, text='Readme!!! 兼 console output', font=("微软雅黑", 12), command=lambda:readmeclick())
# readme.pack()

link = tk.Label(master, text='Readme!!! 兼 console output', font=("Arial", 10) , fg="blue", cursor="hand2")
link.bind("<Button-1>", lambda e: readmeclick())
link.pack(pady=10)

master.mainloop()