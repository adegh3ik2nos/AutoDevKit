import pyautogui
import sys
import time
import pynput
import argparse
from lxml import etree

key_name_table = {
    "cmd": "winleft"
}

inputs = etree.Element("inputs")

def on_click(x, y, button, pressed):
    if button.name == "left":
        input = etree.SubElement(inputs, "input")
        input.set("type", "lclick_on" if pressed else "lclick_off")
        input.set("x", str(x))
        input.set("y", str(y))

        print("lclick_on: {0}".format((x, y)))

def on_keydown(key):
    try:
        key_name = key.name
        if key_name in key_name_table:
            key_name = key_name_table[key_name]

        if key_name == "esc":
            return False
        else:
            input = etree.SubElement(inputs, "input")
            input.set("type", "key_down")
            input.set("key", key_name)

            print("key: {0}".format(key_name))
    except AttributeError:
        input = etree.SubElement(inputs, "input")
        input.set("type", "key_down")
        input.set("key", str(key).rstrip("'").lstrip("'"))

        print("key: {0}".format(key))

def on_keyup(key):
    try:
        key_name = key.name
        if key_name in key_name_table:
            key_name = key_name_table[key_name]

        if key_name == "esc":
            return False
        else:
            input = etree.SubElement(inputs, "input")
            input.set("type", "key_up")
            input.set("key", key_name)

            print("key: {0}".format(key_name))
    except AttributeError:
        input = etree.SubElement(inputs, "input")
        input.set("type", "key_up")
        input.set("key", str(key).rstrip("'").lstrip("'"))

        print("key: {0}".format(key))


#GUI操作のログを出力してGUI自動化設定を作成
def command_new(args):
    settings_path = "{0}/{1}.xml".format(args.dir.rstrip("\\").rstrip("/"), args.settings)

    mouse_listener = pynput.mouse.Listener(on_click=on_click)
    mouse_listener.start()
    with pynput.keyboard.Listener(on_press=on_keydown, on_release=on_keyup) as key_listener:
        key_listener.join()
        
    tree = etree.ElementTree(inputs)
    tree.write(settings_path, pretty_print=True)

#GUI自動化設定を使用して自動操作
def command_exec(args):
    dir = "."
    if len(args.dir) > 0:
        dir = args.dir.rstrip("\\").rstrip("/")
    
    settings_path = "{0}/{1}.xml".format(dir, args.settings)

    tree = etree.parse(settings_path)
    root = tree.getroot()

    for inputs in root.iter("inputs"):
        for input in root.iter("input"):
            type = input.get("type")
            if type == "lclick_on":
                pyautogui.mouseDown(int(input.get("x")), int(input.get("y")), button="left")
            elif type == "lclick_off":
                x = int(input.get("x"))
                y = int(input.get("y"))
                pyautogui.moveTo(x, y, duration=2)
                pyautogui.mouseUp(x, y, button="left")
            elif type == "key_down":
                pyautogui.keyDown(input.get("key"))
            elif type == "key_up":
                pyautogui.keyUp(input.get("key"))


def main():
    #コマンドライン引数をパースしてそれぞれのサブコマンド処理を実行
    parser = argparse.ArgumentParser(description = "gui execute automation.")
    subparsers = parser.add_subparsers()

    parser_new = subparsers.add_parser("input", help = "input getting and generate settings. (esc key on exit condition.")
    parser_new.add_argument("settings", help = "settings name")
    parser_new.add_argument("-d", "--dir", action = "store", required = False, help="working directory", type = str, default = ".")
    parser_new.set_defaults(handler=command_new)
    
    parser_exec = subparsers.add_parser("exec", help = "auto exec gui tools.")
    parser_exec.add_argument("settings", help = "settings name")
    parser_exec.add_argument("-d", "--dir", action = "store", required = False, help="working directory", type = str, default = ".")
    parser_exec.set_defaults(handler=command_exec)

    args = parser.parse_args()
    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()

    return 0

if __name__ == "__main__":
    sys.exit(main())
