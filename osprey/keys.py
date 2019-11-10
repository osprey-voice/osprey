import string

KEYS = []

LETTERS = list(string.ascii_lowercase)

NUMBERS = list(string.digits)

PUNCTUATION = list(string.punctuation)

MODIFIERS = [
    'ctrl',
    'rctrl',
    'alt',
    'ralt',
    'cmd',
    'shift',
    'rshift',
    'fn',
]

MISC = [
    'capslock',
    'backspace',
    'bksp',
    'delete',
    'del',
    'return',
    'enter',
    'space',
    'tab',
    'up',
    'down',
    'left',
    'right',
    'pageup',
    'pgup',
    'pagedown',
    'pgdown',
    'home',
    'end',
    'escape',
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

KEYPAD = [
    'keypad_0',
    'keypad_1',
    'keypad_2',
    'keypad_3',
    'keypad_4',
    'keypad_5',
    'keypad_6',
    'keypad_7',
    'keypad_8',
    'keypad_9',
    'keypad_clear',
    'keypad_equals',
    'keypad_divide',
    'keypad_multiply',
    'keypad_minus',
    'keypad_plus',
    'keypad_decimal',
    'keypad_enter',
]

UTILS = [
    'help',
    'volup',
    'voldown',
    'mute',
]

KEYS = LETTERS + NUMBERS + PUNCTUATION + MODIFIERS + MISC + FUNCTION + KEYPAD + UTILS
