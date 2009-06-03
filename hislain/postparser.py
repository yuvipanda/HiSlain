import re

class Post():
    title = ""
    meta = {}
    content = ""

def post_from_file(file):
    p = Post()
    p.title = file.readline().rstrip()

    l = file.readline()
    
    while l != "\n":
        l = l.rstrip()
        meta = l.split(":")
        key = meta[0]
        value = ":".join(meta[1:]).lstrip()
        p.meta[key] = value
        l = file.readline()

    p.content = file.read().rstrip()

    return p
