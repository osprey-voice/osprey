import evdev
import re

from .evdev import KEY_MAP

uinput = evdev.UInput()


def press(key_string):
    key_combinations = key_string.split(' ')
    for key_combination in key_combinations:
        keys = key_combination.split('-')
        for key in keys:
            if isinstance(KEY_MAP[key], list):
                uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key][0], 1)
                uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key][1], 1)
            else:
                uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key], 1)
        for key in keys[::-1]:  # reverses list
            if isinstance(KEY_MAP[key], list):
                uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key][1], 0)
                uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key][0], 0)
            else:
                uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key], 0)


def insert(custom_string):
    for char in custom_string:
        press(char)


def repeate(count):
    pass


CONTEXT_GROUPS = {}


class ContextGroup:
    def __init__(self, name):
        self._name = name

        self._contexts = {}

        CONTEXT_GROUPS[name] = self


DEFAULT_CONTEXT_GROUP = ContextGroup('default')


class Context:
    def __init__(self, name, app=None, exe=None, bundle=None,
                 title=None, func=None, group=DEFAULT_CONTEXT_GROUP):
        self._name = name

        self._app = app
        self._exe = exe
        self._bundle = bundle
        self._title = title
        self._func = func
        self._group = group

        self._keymap = {}
        self._regexes = {}
        self._lists = {}

        group._contexts[name] = self

    def set_keymap(self, keymap):
        self._keymap = keymap

    def _compile(self):
        for string, callback in self._keymap.items():
            self._regexes[re.compile(string)] = callback

    def _match(self, input):
        for regex, callback in self._regexes.items():
            match = regex.fullmatch(input)
            if match:
                callback(match)
                return True
        return False
