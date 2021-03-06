import logging
import os
import time
from typing import Callable, Optional as OptionalType

from dragonfly import Choice, CompoundRule, Dictation, Integer, Optional, Repetition

IS_WAYLAND_RUNNING = os.environ.get('XDG_SESSION_TYPE') == 'wayland'

if IS_WAYLAND_RUNNING:
    from .evdev import evdev_press, evdev_insert
    PRESS_FUNCTION = evdev_press
    INSERT_FUNCTION = evdev_insert
else:
    from .pyautogui import pyautogui_press, pyautogui_insert
    PRESS_FUNCTION = pyautogui_press
    INSERT_FUNCTION = pyautogui_insert


last_command: OptionalType[Callable[[], None]] = None


def press(key_string):
    PRESS_FUNCTION(key_string)

    global last_command
    last_command = lambda: press(key_string)


previously_inserted_string: OptionalType[str] = None


def insert(custom_string):
    INSERT_FUNCTION(custom_string)

    global last_command
    last_command = lambda: insert(custom_string)

    global previously_inserted_string
    previously_inserted_string = custom_string


def undo_insert():
    global previously_inserted_string
    if previously_inserted_string:
        press('Backspace')
        repeat(len(previously_inserted_string) - 1)


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

        self._commands = {}
        self._choices = {}

        group._contexts[name] = self

    def set_commands(self, commands):
        self._commands = commands

    def set_choices(self, choices):
        self._choices = choices

    def _compile(self, grammar):
        for rule, action in self._commands.items():
            placeholders = {}
            if '<phrase>' in rule:
                placeholders['phrase'] = Dictation('phrase')
            if '<word>' in rule:
                placeholders['word'] = Dictation('word')
            if '<n>' in rule:
                placeholders['n'] = Integer('n', 0, 1_000_000_000)
            for name, choice in self._choices.items():
                if f'<{name}>*' in rule:
                    placeholders[name] = Optional(Repetition(
                        Choice('', {x: x for x in choice}), max=5), name=name)
                elif f'<{name}>+' in rule:
                    placeholders[name] = Repetition(
                        Choice('', {x: x for x in choice}), max=5, name=name)
                elif f'<{name}>' in rule:
                    placeholders[name] = Choice(name, {x: x for x in choice})

            normalized_rule = rule.replace('*', '').replace('+', '')

            # default parameters used to fix late binding
            # https://stackoverflow.com/questions/3431676/creating-functions-in-a-loop
            def _process_recognition(self, node, extras, placeholder_keys=placeholders.keys(),
                                     action=action):
                m = {
                    'transcript': ' '.join(node.words()),
                }
                for key in placeholder_keys:
                    if key in extras:
                        val = extras[key]
                        if val is None:
                            m[key] = []
                        elif key in {'phrase', 'word'}:
                            m[key] = val.format()
                        else:
                            m[key] = val
                    else:
                        m[key] = None
                action(m)

            name = f'{self._name}: \'{rule}\''

            try:
                rule = type(
                    name,
                    (CompoundRule,),
                    {
                        'spec': normalized_rule,
                        'extras': list(placeholders.values()),
                        '_process_recognition': _process_recognition,
                    },
                )()
            except Exception as e:
                logging.exception(f'Error occurred while compiling rule \'{name}\': {e}')
            else:
                grammar.add_rule(rule)
                logging.info(f'Compiled rule \'{name}\'')
