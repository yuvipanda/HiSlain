class Hooker:
    def __init__(self):
        self.actions = {}

    def add_action(self, name, function):
        if name in self.actions:
            self.actions[name].append(function)
        else:
            self.actions[name] = [function]

    def _exec_action(self, name, *args):
        for h in self.actions[name]:
            yield h(*args)

    def __getattr__(self, name):
        if name in self.actions:
            return lambda *args: self._exec_action(name, *args)
        else:
            raise AttributeError(name)

    def string(self, name, *args):
        return "\n".join(self._exec_action(name, *args))
