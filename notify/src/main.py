import sys
import time
import argparse
from plyer import notification
import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog as simpledialog
import os


APP_NAME = "notify"

# バルーン通知
def command_notice_balloon(args):
    if os.path.exists(args.icon):
        notification.notify(
            title = args.title,
            message = args.msg,
            app_name = APP_NAME, 
            app_icon = args.icon)
    else:
        notification.notify(
            title = args.title,
            message = args.msg,
            app_name = APP_NAME)

# ポップアップ通知
def command_notice_popup(args):
    root = tk.Tk()
    root.withdraw() #小さなウィンドウを表示させない
    messagebox.showinfo(
        title = args.title, 
        message = args.msg)


def main():
    #コマンドライン引数をパースしてそれぞれのサブコマンド処理を実行
    parser = argparse.ArgumentParser(description = "gui execute automation.")
    subparsers = parser.add_subparsers()

    parser_new = subparsers.add_parser("balloon", help = "notice info by balloon.")
    parser_new.add_argument("title")
    parser_new.add_argument("msg")
    parser_new.add_argument("-ic", "--icon", action = "store", required = False, help=".ico file path", type = str, default = "")
    parser_new.set_defaults(handler=command_notice_balloon)
    
    parser_new = subparsers.add_parser("popup", help = "notice info by popup.")
    parser_new.add_argument("title")
    parser_new.add_argument("msg")
    parser_new.set_defaults(handler=command_notice_popup)

    args = parser.parse_args()
    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()

    return 0

if __name__ == "__main__":
    sys.exit(main())
