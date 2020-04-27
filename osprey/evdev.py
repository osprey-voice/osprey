import string
import time

from evdev.ecodes import ecodes
import evdev

from .keys import KEYS


KEY_MAP = {}

PUNCTUATION = {
    '-': 'minus',
    '=': 'equal',
    '\'': 'apostrophe',
    ',': 'comma',
    '.': 'dot',
    '/': 'slash',
    ';': 'semicolon',
    '[': 'leftbrace',
    ']': 'rightbrace',
    '\\': 'backslash',
    '`': 'grave',
    '!': ['Shift', '1'],
    '@': ['Shift', '2'],
    '#': ['Shift', '3'],
    '$': ['Shift', '4'],
    '%': ['Shift', '5'],
    '^': ['Shift', '6'],
    '&': ['Shift', '7'],
    '*': ['Shift', '8'],
    '(': ['Shift', '9'],
    ')': ['Shift', '0'],
    '_': ['Shift', '-'],
    '+': ['Shift', '='],
    '"': ['Shift', '\''],
    ':': ['Shift', ';'],
    '<': ['Shift', ','],
    '>': ['Shift', '.'],
    '?': ['Shift', '/'],
    '{': ['Shift', '['],
    '}': ['Shift', ']'],
    '|': ['Shift', '\\'],
    '~': ['Shift', '`'],
}

MODIFIERS = {
    'Cmd': None,
    'Ctrl': 'leftctrl',
    'Alt': 'leftalt',
    'Shift': 'leftshift',
}

MISC = {
    'Escape': 'esc',
}

KEY_MAP.update({key: key for key in KEYS})
KEY_MAP.update({key: ['Shift', key.lower()] for key in string.ascii_uppercase})
KEY_MAP.update(PUNCTUATION)
KEY_MAP.update(MODIFIERS)
KEY_MAP.update(MISC)

KEY_MAP.update({key: ecodes[f'KEY_{value.upper()}']
                for (key, value) in KEY_MAP.items() if isinstance(value, str)})
KEY_MAP.update({key: [KEY_MAP[value[0]], KEY_MAP[value[1]]]
                for (key, value) in KEY_MAP.items() if isinstance(value, list)})


uinput = None


def _open_uinput():
    global uinput
    if uinput is None:
        uinput = evdev.UInput()


def _close_uinput():
    global uinput
    if uinput is not None:
        uinput.close()
        uinput = None


def evdev_press(key_string):
    keys = key_string.split(' ')
    for key in keys:
        if isinstance(KEY_MAP[key], list):
            uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key][0], 1)
            uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key][1], 1)
        else:
            uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key], 1)
    for key in keys[::-1]:  # `[::-1]` reverses list
        if isinstance(KEY_MAP[key], list):
            uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key][1], 0)
            uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key][0], 0)
        else:
            uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key], 0)
    uinput.syn()


def evdev_insert(custom_string):
    for char in custom_string:
        if char == ' ':
            evdev_press('Space')
        elif char == '\t':
            evdev_press('Tab')
        else:
            evdev_press(char)
        # needed otherwise evdev will reject some input
        time.sleep(.01)
