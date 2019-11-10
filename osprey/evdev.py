from evdev.ecodes import ecodes

from .keys import KEYS


KEY_MAP = {}

PUNCTUATION = {
    '!': None,
    '"': None,
    '#': None,
    '$': 'dollar',
    '%': None,
    '&': None,
    '\'': 'apostrophe',
    '(': 'kpleftparen',
    ')': 'kprightparen',
    '*': 'kpasterisk',
    '+': 'kpplus',
    ',': 'comma',
    '-': 'minus',
    '.': 'dot',
    '/': 'slash',
    ':': None,
    ';': 'semicolon',
    '<': None,
    '=': 'equal',
    '>': None,
    '?': 'question',
    '@': None,
    '[': None,
    '\\': 'backslash',
    ']': None,
    '^': None,
    '_': None,
    '`': 'grave',
    '{': 'leftbrace',
    '|': None,
    '}': 'rightbrace',
    '~': None,
}

MODIFIERS = {
    'ctrl': 'leftctrl',
    'rctrl': 'righctrl',
    'alt': 'leftalt',
    'ralt': 'rightalt',
    'cmd': None,
    'shift': 'leftshift',
    'rshift': 'righshift',
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

KEY_MAP.update({key: ecodes[f'KEY_{key.upper()}'] for key in KEYS if key.upper() in ecodes})
KEY_MAP.update(PUNCTUATION)
KEY_MAP.update(MODIFIERS)
KEY_MAP.update(MISC)
KEY_MAP.update(KEYPAD)
KEY_MAP.update(UTILS)
