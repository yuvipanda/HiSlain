import os

from datetime import datetime
from dateutil import parser

from jinja2 import Environment, FileSystemLoader
import yaml
import markdown

import utils

post_meta_defaults = {
#        meta name  : (type, default value)
        'published' : (datetime, lambda p, s: datetime.now()),
        'permalink' : (unicode, lambda p, s: utils.slugify(p.title) + '.html'),
        'tags'      : (list, []),
        'container' : (unicode, 'blog'),
        }

def _parsetype(type, data):
    if type is datetime:
        return parser.parse(data)
    elif type is unicode:
        return unicode(data, encoding='UTF-8')
    elif type is list:
        return [i.strip() for i in data.split(',')]
    else:
        return data

def _dumptype(type, data):
    if type is datetime:
        return data.isoformat()
    elif type is list:
        return ', '.join(data)
    else:
        return data

class Post():
    def __init__(self, file=None, settings=None):
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

            self.content_raw = file.read().rstrip()
            self.content = markdown.markdown(self.content_raw)

            # Set in default values, and parse according to type
            for k, v in post_meta_defaults.items():
                if k in self.meta:
                    self.meta[k] = _parsetype(v[0], self.meta[k])
                else:
                    if callable(v[1]):
                        self.meta[k] = v[1](self, settings)
                    else:
                        self.meta[k] = v[1]

    def to_file(self, file):
        file.write(self.title + '\n')
        
        for k, v in self.meta.items():
            if k in post_meta_defaults:
                v = _dumptype(post_meta_defaults[k][0], v)
                file.write(("%s: %s" % (k, v)) + '\n')

        file.write('\n')

        file.write(self.content_raw)



class Blog():
    def __init__(self, dir=None):
        if dir:
            self.settings = read_config(file(os.path.join(dir, "blog.yaml")))
            posts_dir = os.path.join(dir, self.settings.get("postspath", "posts"))
            self.posts = [
                    Post(file(os.path.join(posts_dir,post_file)), settings=self.settings) 
                    for post_file in os.listdir(posts_dir)
                    ]

            pages_dir = os.path.join(dir, self.settings.get("pagespath", "pages"))
            self.pages = [
                    Post(file(os.path.join(pages_dir, page_file))) 
                    for page_file in os.listdir(pages_dir)
                    ]

            themes_path = os.path.join(dir, self.settings.get("themespath","themes"))

            templates_path = os.path.join(themes_path, self.settings.get("theme", "simpl"))
            self.env = Environment(loader=FileSystemLoader(templates_path))
            self.settings['theme_path'] = templates_path            
            self.settings['out_path'] = os.path.join(dir, self.settings.get('out', 'out'))
            self.settings['media_path'] = os.path.join(dir, self.settings.get('media', 'media'))
            self.settings['blog_dir'] = dir
        else:
            self.env = None
            self.settings = {}
            self.posts = []

def read_config(file):
    return yaml.load(file)


