import pyautogui
import sys
import time
import pynput
import argparse
from lxml import etree


inputs = etree.Element("inputs")

def on_click(x, y, button, pressed):
    if button.name == "left":
        input = etree.SubElement(inputs, "input")
        input.set("type", "lclick_on" if pressed else "lclick_off")
        input.set("x", str(x))
        input.set("y", str(y))

        print("lclick_on: {0}".format((x, y)))
    elif button.name == "right":
        return False

def on_keydown(key):
    input = etree.SubElement(inputs, "input")
    input.set("type", "key")
    input.set("key", str(key).rstrip("'").lstrip("'"))

    print("key: {0}".format(key))

#GUI操作のログを出力してGUI自動化設定を作成
def command_new(args):
    settings_path = "{0}/{1}.xml".format(args.dir.rstrip("\\").rstrip("/"), args.settings)

    key_listener = pynput.keyboard.Listener(on_release=on_keydown)
    key_listener.start()
    with pynput.mouse.Listener(
            on_click=on_click) as mouse_listener:
        mouse_listener.join()
    
    tree = etree.ElementTree(inputs)
    tree.write(settings_path, pretty_print=True)

#GUI自動化設定を使用して自動操作
def command_exec(args):
    settings_path = "{0}/{1}.xml".format(args.dir.rstrip("\\").rstrip("/"), args.settings)

    tree = etree.parse(settings_path)
    root = tree.getroot()

    for inputs in root.iter("inputs"):
        for input in root.iter("input"):
            type = input.get("type")
            if type == "lclick_on":
                pyautogui.mouseDown(int(input.get("x")), int(input.get("y")), button='left')
            elif type == "lclick_off":
                x = int(input.get("x"))
                y = int(input.get("y"))
                pyautogui.moveTo(x, y, duration=2)
                pyautogui.mouseUp(x, y, button='left')
            elif type == "key":
                pyautogui.keyDown(input.get("key"))


def main():
    #コマンドライン引数をパースしてそれぞれのサブコマンド処理を実行
    parser = argparse.ArgumentParser(description = "gui execute automation.")
    subparsers = parser.add_subparsers()

    parser_new = subparsers.add_parser("input", help = "input getting and generate settings. (right click on exit condition.")
    parser_new.add_argument("settings", help = "settings name")
    parser_new.add_argument("-d", "--dir", action = "store", required = False, help="working directory")
    parser_new.set_defaults(handler=command_new)
    
    parser_exec = subparsers.add_parser("exec", help = "auto exec gui tools.")
    parser_exec.add_argument("settings", help = "settings name")
    parser_exec.add_argument("-d", "--dir", action = "store", required = False, help="working directory")
    parser_exec.set_defaults(handler=command_exec)

    args = parser.parse_args()
    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()

    return 0

if __name__ == "__main__":
    sys.exit(main())
