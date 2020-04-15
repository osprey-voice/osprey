import string

from evdev.ecodes import ecodes

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
