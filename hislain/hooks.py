class Hooker:
    def __init__(self):
        self.actions = {}
        self.static_files = [] 

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

    def as_string(self, name, *args):
        if not name in self.actions:
            raise KeyError('%s hook not found' % name)
        return "\n".join(self._exec_action(name, *args))
    
    def copy_to_static(self, path):
        self.static_files.append(path)
