import string

KEYS = []

LETTERS = list(string.ascii_letters)

NUMBERS = list(string.digits)

PUNCTUATION = list(string.punctuation)

MODIFIERS = [
    'ctrl',
    'rctrl',
    'alt',
    'ralt',
    'shift',
    'rshift',
    'fn',
]

MISC = [
    'capslock',
    'backspace',
    'delete',
    'enter',
    'space',
    'tab',
    'up',
    'down',
    'left',
    'right',
    'pageup',
    'pagedown',
    'home',
    'end',
    'esc',
]

FUNCTION = [
    'f1',
    'f2',
    'f3',
    'f4',
    'f5',
    'f6',
    'f7',
    'f8',
    'f9',
    'f10',
    'f11',
    'f12',
    'f13',
    'f14',
    'f15',
    'f16',
    'f17',
    'f18',
    'f19',
    'f20',
]

UTILS = [
    'volumeup',
    'volumedown',
    'mute',
]

WHITESPACE = [
    ' ',
    '\t',
]

KEYS = LETTERS + NUMBERS + PUNCTUATION + MODIFIERS + MISC + FUNCTION + UTILS + WHITESPACE
