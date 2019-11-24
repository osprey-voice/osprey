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
    '[': 'leftbrace',
    '\\': 'backslash',
    ']': 'rightbrace',
    '^': ['shift', '6'],
    '_': ['shift', '-'],
    '`': 'grave',
    '{': ['shift', '['],
    '|': ['shift', '\\'],
    '}': ['shift', ']'],
    '~': ['shift', '`'],
}

MODIFIERS = {
    'ctrl': 'leftctrl',
    'rctrl': 'rightctrl',
    'alt': 'leftalt',
    'ralt': 'rightalt',
    'shift': 'leftshift',
    'rshift': 'rightshift',
}

WHITESPACE = {
    ' ': 'space',
    '\t': 'tab',
}

KEY_MAP.update({key: key for key in KEYS})
KEY_MAP.update({key: ['shift', key.lower()] for key in KEYS if key.isupper()})
KEY_MAP.update(PUNCTUATION)
KEY_MAP.update(MODIFIERS)
KEY_MAP.update(WHITESPACE)

KEY_MAP.update({key: ecodes[f'KEY_{value.upper()}']
                for (key, value) in KEY_MAP.items() if isinstance(value, str)})
KEY_MAP.update({key: [KEY_MAP[value[0]], KEY_MAP[value[1]]]
                for (key, value) in KEY_MAP.items() if isinstance(value, list)})
