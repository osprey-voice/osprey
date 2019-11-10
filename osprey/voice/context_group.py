class ContextGroup:
    def __init__(self, name):
        self._name = name

        self._contexts = {}

    def _set_context(self, context):
        self._contexts[context._name] = context

    def load(self):
        pass
