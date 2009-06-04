import yaml
import os

from jinja2 import Environment, FileSystemLoader
class Post():
    def __init__(self, file=None):
        self.meta = {}
        self.title = ""
        self.content = ""
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

            print self.meta
            self.content = file.read().rstrip()
    
    def to_post(self, file):
        file.write(self.title + '\n')
        
        for k, v in self.meta.items():
            file.write(("%s: %s" % (k, v)) + '\n')

        file.write('\n')

        file.write(self.content)


class Blog():
    def __init__(self, dir=None):
        if dir:
            self.settings = read_config(file(os.path.join(dir, "blog.yaml")))
            posts_dir = os.path.join(dir, self.settings.get("postspath", "posts"))
            self.posts = [
                    Post(file(os.path.join(posts_dir,post_file))) 
                    for post_file in os.listdir(posts_dir)
                    ]

            themes_path = os.path.join(dir, self.settings.get("themespath","themes"))

            templates_path = os.path.join(themes_path, self.settings.get("theme", "simpl"))
            self.env = Environment(loader=FileSystemLoader(templates_path))
        else:
            self.env = None
            self.settings = {}
            self.posts = []

def read_config(file):
    return yaml.load(file)


