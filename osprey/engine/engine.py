from ..voice import DEFAULT_CONTEXT_GROUP


class Engine:
    def __init__(self):
        pass

    def mimic(self, input_array):
        for context in DEFAULT_CONTEXT_GROUP:
            context.match(input)

    def register(self, TODO, action):
        pass
