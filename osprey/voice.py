import evdev
import re

from .evdev import KEY_MAP

uinput = evdev.UInput()
enabled = True


def enable():
    global enabled
    enabled = True


def disable():
    global enabled
    enabled = False


def toggle():
    global enabled
    enabled = not enabled


def is_enabled():
    global enabled
    return enabled


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
    uinput.syn()


def insert(custom_string):
    for char in custom_string:
        if char == ' ':
            press('Space')
        if char == '\t':
            press('Tab')
        else:
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


def _convert_keymap(keymap, lists):
    def named_regex(name, regex):
        return r'(?P<{}>{})'.format(name, regex)

    def list_to_regex(list):
        return r'(\b({})\b\s?)'.format('|'.join(list))

    quantifiers = ['*', '+']

    regexes = {key: list_to_regex(val) for key, val in lists.items()}
    quantified_regexes = {f'{key}{quantifier}': rf'{val}{quantifier}' for key,
                          val in regexes.items() for quantifier in quantifiers}
    named_regexes = {key: named_regex(key[:-1], val) for key, val in quantified_regexes.items()}

    def convert_rule(rule):
        return rule.format(**named_regexes)

    def convert_match(match, lists):
        return {key: match.group(key).strip().split(' ') for key in lists if key in match.groupdict() and match.group(key)}

    converted = {}
    for key, val in keymap.items():
        def callback(m):
            if isinstance(val, list):
                converted_match = convert_match(m, lists)
                for cb in val:
                    cb(converted_match)
            else:
                val(convert_match(m, lists))
        converted[convert_rule(key)] = callback

    return converted


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

    def set_lists(self, lists):
        self._lists = lists

    def _compile(self):
        keymap = _convert_keymap(self._keymap, self._lists)
        for string, callback in keymap.items():
            self._regexes[re.compile(string)] = callback

    def _match(self, input):
        for regex, callback in self._regexes.items():
            match = regex.fullmatch(input)
            if match:
                callback(match)
                return True
        return False
