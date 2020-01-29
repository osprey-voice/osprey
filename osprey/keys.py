import string

KEYS = []

LETTERS = list(string.ascii_letters)

NUMBERS = list(string.digits)

PUNCTUATION = list(string.punctuation)

MODIFIERS = [
    'Cmd',
    'Ctrl',
    'RightCtrl',
    'Alt',
    'RightAlt',
    'Shift',
    'RightShift',
    'Fn',
]

MISC = [
    'Capslock',
    'Backspace',
    'Delete',
    'Enter',
    'Space',
    'Tab',
    'Up',
    'Down',
    'Left',
    'Right',
    'PageUp',
    'PageDown',
    'Home',
    'End',
    'Escape',
]

FUNCTION = [
    'F1',
    'F2',
    'F3',
    'F4',
    'F5',
    'F6',
    'F7',
    'F8',
    'F9',
    'F10',
    'F11',
    'F12',
    'F13',
    'F14',
    'F15',
    'F16',
    'F17',
    'F18',
    'F19',
    'F20',
]

UTILS = [
    'VolumeUp',
    'VolumeDown',
    'Mute',
]

WHITESPACE = [
    'Space',
    'Tab',
]

KEYS = LETTERS + NUMBERS + PUNCTUATION + MODIFIERS + MISC + FUNCTION + UTILS + WHITESPACE
