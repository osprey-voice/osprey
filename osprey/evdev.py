from evdev.ecodes import ecodes

from .keys import KEYS


KEY_MAP = {}

PUNCTUATION = {
    '!': ['shift', '1'],
    '"': ['shift', '\''],
    '#': ['shift', '3'],
    '$': 'dollar',
    '%': ['shift', '5'],
    '&': ['shift', '7'],
    '\'': 'apostrophe',
    '(': 'kpleftparen',
    ')': 'kprightparen',
    '*': 'kpasterisk',
    '+': 'kpplus',
    ',': 'comma',
    '-': 'minus',
    '.': 'dot',
    '/': 'slash',
    ':': ['shift', ';'],
    ';': 'semicolon',
    '<': ['shift', ','],
    '=': 'equal',
    '>': ['shift', '.'],
    '?': 'question',
    '@': ['shift', '2'],
    '[': None,
    '\\': 'backslash',
    ']': None,
    '^': ['shift', '6'],
    '_': ['shift', '-'],
    '`': 'grave',
    '{': 'leftbrace',
    '|': ['shift', '\\'],
    '}': 'rightbrace',
    '~': ['shift', '`'],
}

MODIFIERS = {
    'ctrl': 'leftctrl',
    'rctrl': 'rightctrl',
    'alt': 'leftalt',
    'ralt': 'rightalt',
    'cmd': None,
    'shift': 'leftshift',
    'rshift': 'rightshift',
}

MISC = {
    'bksp': 'backspace',
    'del': 'delete',
    'return': None,
    'pgup': 'pageup',
    'pgdown': 'pagedown',
    'escape': 'esc',
}

KEYPAD = {
    'keypad_0': 'kp0',
    'keypad_1': 'kp1',
    'keypad_2': 'kp2',
    'keypad_3': 'kp3',
    'keypad_4': 'kp4',
    'keypad_5': 'kp5',
    'keypad_6': 'kp6',
    'keypad_7': 'kp7',
    'keypad_8': 'kp8',
    'keypad_9': 'kp9',
    'keypad_clear': None,
    'keypad_equals': 'kpequal',
    'keypad_divide': 'kpslash',
    'keypad_multiply': 'kpasterisk',
    'keypad_minus': 'kpminus',
    'keypad_plus': 'kpplus',
    'keypad_decimal': 'kpdot',
    'keypad_enter': 'kpenter',
}

UTILS = {
    'volup': 'volumeup',
    'voldown': 'volumedown',
}

WHITESPACE = {
    ' ': 'space',
    '\t': 'tab',
}

KEY_MAP.update({key: key for key in KEYS})
KEY_MAP.update({key: ['shift', key.lower()] for key in KEYS if key.isupper()})
KEY_MAP.update(PUNCTUATION)
KEY_MAP.update(MODIFIERS)
KEY_MAP.update(MISC)
KEY_MAP.update(KEYPAD)
KEY_MAP.update(UTILS)
KEY_MAP.update(WHITESPACE)

KEY_MAP.update({key: ecodes[f'KEY_{value.upper()}']
                for (key, value) in KEY_MAP.items() if isinstance(value, str)})
KEY_MAP.update({key: [KEY_MAP[value[0]], KEY_MAP[value[1]]]
                for (key, value) in KEY_MAP.items() if isinstance(value, list)})
