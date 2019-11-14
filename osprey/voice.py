import evdev

from ..evdev import KEY_MAP


def press(key_string):
    keys = key_string.split('-')
    for key in keys:
        if isinstance(KEY_MAP[key], list):
            uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key][0], 1)
            uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key][1], 1)
        else:
            uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key], 1)
    for key in reverse(keys):
        if isinstance(KEY_MAP[key], list):
            uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key][1], 0)
            uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key][0], 0)
        else:
            uinput.write(evdev.ecodes.EV_KEY, KEY_MAP[key], 0)


def Rep(repeate_count):
    pass


def Str(custom_string):
    def callback():
        pass
    return callback


def Key(key_string):
    def callback():
        pass
    return callback


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

        self._keymap = None
        self._lists = {}

        self._group._set_context(self)

    def keymap(self, keymap):
        self._keymap = keymap

    def set_list(self, name, keys):
        self._lists[name] = keys


class ContextGroup:
    def __init__(self, name):
        self._name = name

        self._contexts = {}

    def _set_context(self, context):
        self._contexts[context._name] = context

    def load(self):
        pass


DEFAULT_CONTEXT_GROUP = ContextGroup('default')
CONTEXT_GROUPS = [DEFAULT_CONTEXT_GROUP]
