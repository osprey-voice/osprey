import re
from typing import Set, Optional, Callable

import evdev

from .evdev import KEY_MAP

uinput = evdev.UInput()

enabled = True
preferred_phrases: Set[str] = set()
last_command: Optional[Callable[[], None]] = None


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
    keys = key_string.split(' ')
    for key in keys:
        if isinstance(KEY_MAP[key], list):
            uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key][0], 1)
            uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key][1], 1)
        else:
            uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key], 1)
    for key in keys[::-1]:  # `[::-1]` reverses list
        if isinstance(KEY_MAP[key], list):
            uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key][1], 0)
            uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key][0], 0)
        else:
            uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key], 0)
    uinput.syn()

    global last_command
    last_command = lambda: press(key_string)  # noqa


def insert(custom_string):
    for char in custom_string:
        if char == ' ':
            press('Space')
        elif char == '\t':
            press('Tab')
        else:
            press(char)
    global last_command
    last_command = lambda: insert(custom_string)  # noqa


def repeat(count):
    global last_command
    if last_command:
        for _i in range(count):
            last_command()


context_groups = {}


class ContextGroup:
    def __init__(self, name):
        self._name = name

        self._contexts = {}

        context_groups[name] = self


default_context_group = ContextGroup('default')


def _convert_rules(rules, lists):
    def named_regex(name, regex):
        return r'(?P<{}>{})'.format(name, regex)

    def list_to_regex(list):
        return r'(\b({})\b\s?)'.format('|'.join(list))

    quantifiers = ['*', '+']

    regexes = {key: list_to_regex(val) for key, val in lists.items()}
    quantified_regexes = {f'{key}{quantifier}': rf'{val}{quantifier}' for key,
                          val in regexes.items() for quantifier in quantifiers}
    regexes.update(quantified_regexes)
    regexes.update({'word': r'\w+'})
    regexes.update({'phrase': r'\w+(\s\w+)*'})
    named_regexes = {key: named_regex(
        key[:-1] if key[-1] in quantifiers else key, val) for key, val in regexes.items()}

    def convert_rule(rule):
        return rule.format(**named_regexes)

    def convert_match(match, lists):
        converted_match = {}
        for name, val in match.groupdict().items():
            if val != '':
                if name in lists:
                    matches = []
                    tokens = val.strip().split(' ')[::-1]  # `[::-1]` reverses list
                    cur = ""
                    while len(tokens) != 0:
                        cur = tokens.pop() if cur == "" else cur + " " + tokens.pop()
                        if cur in lists[name]:
                            matches.append(cur)
                            cur = ""
                    converted_match[name] = matches
                else:
                    converted_match[name] = [val]
        return converted_match

    converted = {}
    for key, val in rules.items():
        # `val=val` used to fix late binding
        # https://stackoverflow.com/questions/3431676/creating-functions-in-a-loop
        def callback(m, val=val):
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
                 title=None, func=None, group=default_context_group):
        self._name = name

        self._app = app
        self._exe = exe
        self._bundle = bundle
        self._title = title
        self._func = func
        self._group = group

        self._rules = {}
        self._regexes = {}
        self._lists = {}

        group._contexts[name] = self

    def set_rules(self, rules):
        self._rules = rules
        for rule in rules:
            for word in rule.split(' '):
                if '{' not in word:
                    preferred_phrases.add(word)

    def set_lists(self, lists):
        self._lists = lists
        for val in lists.values():
            preferred_phrases.update(set(val))

    def _compile(self):
        rules = _convert_rules(self._rules, self._lists)
        for string, callback in rules.items():
            self._regexes[re.compile(string)] = callback

    def _match(self, transcript):
        for regex, callback in self._regexes.items():
            match = regex.match(transcript)
            if match:
                callback(match)
                transcript = transcript.replace(match[0], '').strip()
                return (True, transcript)
        return (False, transcript)
