from markdown import markdown
import os

css = '<link rel="stylesheet" type="text/css" href="<base_url>static/codehilite.css" />'

def transform_markdown(post):
    if 'content-type' in post.meta and post.meta['content-type'] == 'XHTML':
        return post.content
    else:
        if not hasattr(post, 'content_html'):
            post.content_html = markdown(post.content.decode("utf-8"), ['codehilite'])
        return post.content_html

def main(blog):
    blog.hooks.add_action('render',transform_markdown)
    blog.hooks.copy_to_static(os.path.join('plugins','codehilite.css'))
    blog.hooks.add_action('html_head', 
            lambda: css.replace("<base_url>", blog.settings['base_url']))
