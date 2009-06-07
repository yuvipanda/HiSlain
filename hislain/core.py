import os

from datetime import datetime
from dateutil import parser

from jinja2 import Environment, FileSystemLoader
import yaml
import markdown

import utils

post_meta_defaults = {
#        meta name  : (type, default value)
        'published' : (datetime, lambda p: datetime.now()),
        'permalink' : (unicode, lambda p: utils.slugify(p.title)),
        'tags'      : (list, []),
        }

def _parsetype(type, data):
    if type is datetime:
        return parser.parse(data)
    elif type is str:
        return unicode(data, encoding='UTF-8')
    elif type is list:
        return [i.strip() for i in data.split(',')]
    else:
        return data


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

            self.raw_content = file.read().rstrip()
            self.content = markdown.markdown(self.raw_content)

            # Set in default values, and parse according to type
            for k, v in post_meta_defaults.items():
                if k in self.meta:
                    self.meta[k] = _parsetype(v[0], self.meta[k])
                else:
                    if callable(v[1]):
                        self.meta[k] = v[1](self)
                    else:
                        self.meta[k] = v[1]

    def to_file(self, file):
        file.write(self.title + '\n')
        
        for k, v in self.meta.items():
            file.write(("%s: %s" % (k, v)) + '\n')

        file.write('\n')

        file.write(self.raw_content)

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

            self.settings['out_path'] = os.path.join(dir, self.settings['out_path'])
        else:
            self.env = None
            self.settings = {}
            self.posts = []

def read_config(file):
    return yaml.load(file)


