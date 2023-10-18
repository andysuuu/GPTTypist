import os
import time
import utils


def input_action(res: list, hint_text: str):
    x_avg, y_avg = calculate_coordinate(res)

    hint_text = hint_text.replace('\'', '')
    hint_text = hint_text.replace(' ', '')
    tap_cmd = "adb shell input tap " + x_avg + " " + y_avg
    input_cmd = "adb shell input text '" + hint_text + "'"
    os.system(tap_cmd)
    time.sleep(0.5)
    os.system(input_cmd)
    time.sleep(0.5)
    utils.close_soft_keyboard()


def tap_action(res: list):
    x_avg, y_avg = calculate_coordinate(res)

    tap_cmd = "adb shell input tap " + x_avg + " " + y_avg
    os.system(tap_cmd)
    time.sleep(0.5)
    utils.close_soft_keyboard()


def back_action():
    back_cmd = "adb shell input keyevent 4"
    os.system(back_cmd)
    time.sleep(0.5)


def scroll_down_action():
    scroll_up_cmd = "adb shell input swipe 540 2000 540 500 1000"
    os.system(scroll_up_cmd)


def scroll_up_action():
    scroll_down_cmd = "adb shell input swipe 540 500 540 2000 1000"
    os.system(scroll_down_cmd)


def calculate_coordinate(res: list):
    try:
        x1 = int(res[0])
        y1 = int(res[1])
        x2 = int(res[2])
        y2 = int(res[3])
    except IndexError:
        raise "Index does not found"

    h = y2 - y1
    if h < 100:
        y2 = y1 + 10
    x_avg = str(x1 + round(x2 - x1 + 1) / 2)
    y_avg = str(y1 + round(y2 - y1 + 1) / 2)

    return x_avg, y_avg
