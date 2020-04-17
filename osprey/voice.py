from typing import Set, Optional as OptionalType, Callable
import time

import evdev
from dragonfly import CompoundRule, Dictation, Choice, Integer, Repetition, Optional

from .evdev import KEY_MAP

uinput = None


def _open_uinput():
    global uinput
    if uinput is None:
        uinput = evdev.UInput()


def _close_uinput():
    global uinput
    if uinput is not None:
        uinput.close()
        uinput = None


last_command: OptionalType[Callable[[], None]] = None


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
        # needed otherwise evdev will reject some input
        time.sleep(.01)
    global last_command
    last_command = lambda: insert(custom_string)  # noqa


def repeat(count):
    global last_command
    if last_command:
        for _i in range(count):
            last_command()
            # needed otherwise evdev will reject some input
            time.sleep(.001)


context_groups = {}


class ContextGroup:
    def __init__(self, name):
        self._name = name

        self._enabled = True
        self._contexts = {}

        context_groups[name] = self

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False


default_context_group = ContextGroup('default')


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
        self._lists = {}

        group._contexts[name] = self

    def set_rules(self, rules):
        self._rules = rules

    def set_lists(self, lists):
        self._lists = lists

    def _compile(self, grammar):
        for rule, action in self._rules.items():
            extras = {}
            if '<phrase>' in rule:
                extras['phrase'] = Dictation('phrase')
            if '<n>' in rule:
                extras['n'] = Integer('n', 1, 100)
            for name, l in self._lists.items():
                if f'<{name}>*' in rule:
                    extras[name] = Optional(Repetition(Choice('', {x: x for x in l}), max=5), name=name)
                elif f'<{name}>+' in rule:
                    extras[name] = Repetition(Choice('', {x: x for x in l}), max=5, name=name)
                elif f'<{name}>' in rule:
                    extras[name] = Choice(name, {x: x for x in l})

            corrected_rule = rule.replace('*', '').replace('+', '')

            # default parameters used to fix late binding
            # https://stackoverflow.com/questions/3431676/creating-functions-in-a-loop
            def _process_recognition(self, _node, extras, identifiers=extras.keys(), action=action):
                m = {}
                for key, val in extras.items():
                    if key in identifiers:
                        if val is None:
                            m[key] = []
                        elif key == 'phrase':
                            m[key] = val.format()
                        else:
                            m[key] = val
                action(m)

            rule = type(
                f'{self._name}: {rule}',
                (CompoundRule,),
                {
                    'spec': corrected_rule,
                    'extras': list(extras.values()),
                    '_process_recognition': _process_recognition,
                },
            )()

            grammar.add_rule(rule)
