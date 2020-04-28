import pyautogui

from . import keys

KEY_MAP = {key: key.lower() for key in keys.KEYS}


def pyautogui_press(key_string):
    keys = key_string.split(' ')
    if keys[-1].isupper():
        keys.insert(-1, 'Shift')
        keys[-1].lower()
    keys = {key: KEY_MAP[key] for key in keys}
    for key in keys:
        pyautogui.keyDown(key)
    for key in keys[::-1]:  # `[::-1]` reverses list
        pyautogui.keyUp(key)


def pyautogui_insert(custom_string):
    pyautogui.write(custom_string)
