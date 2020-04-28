import string

KEYS = []

LETTERS = list(string.ascii_letters)

NUMBERS = list(string.digits)

PUNCTUATION = list(string.punctuation)

MODIFIERS = [
    'Cmd',
    'Ctrl',
    'Alt',
    'Shift',
    'Fn',
]

MISC = [
    'CapsLock',
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
    'VolumeMute',
]

WHITESPACE = [
    'Space',
    'Tab',
]

KEYS = LETTERS + NUMBERS + PUNCTUATION + MODIFIERS + MISC + FUNCTION + UTILS + WHITESPACE
