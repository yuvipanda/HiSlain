import yaml

class Post():
    title = ""
    meta = {}
    content = ""

    def __init__(self, file=None):
        if file:
            self.title = file.readline().rstrip()

            l = file.readline()
            
            while l != "\n":
                l = l.rstrip()
                meta = l.split(":")
                key = meta[0]
                value = ":".join(meta[1:]).lstrip()
                self.meta[key] = value
                l = file.readline()

            self.content = file.read().rstrip()

def read_config(file):
    return yaml.load
