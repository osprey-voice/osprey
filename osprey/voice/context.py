from . import DEFAULT_CONTEXT_GROUP


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
