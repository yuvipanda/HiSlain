import re

def slugify(text):
    return re.sub(r'\W+', '-', text.lower()).rstrip('-')
