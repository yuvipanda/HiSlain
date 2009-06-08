import os
import sys

from dateutil import parser
from datetime import datetime

import core
import utils

def _write_template(template, filepath, settings, **kwargs):
    file_path = os.path.join(settings['out_path'], filepath)
    out_file = file(file_path, 'w')
    out_file.write(template.render(dict(settings=settings,**kwargs)))

def publish_post(post, template, settings):
    _write_template(template, post.meta['permalink'], post=post, settings=settings)
   
def publish_posts(posts, template, settings, output_path, **kwargs):
    _write_template(template, output_path, posts=posts, settings=settings, **kwargs)

def publish(blog):
    #Publish Posts
    for p in blog.posts:
        publish_post(p, blog.env.get_template('post.html'), blog.settings)
        print "Published Post %s" % p.title

    #Publish RSS

    #Publish Home Page
    home_posts = sorted(blog.posts, key=lambda p: p.meta['published'])[:5]
    publish_posts(home_posts, blog.env.get_template('posts.html'), blog.settings, output_path='home', title='Home Page', permalink='/')
    print "Published Home page"
  
    #Publish Pages
    for p in blog.pages:
        publish_post(p, blog.env.get_template('post.html'), blog.settings)
        print "Published Page %s" % p.title

    #Publish Monthly Archives

    #Publish Yearly Archives

    #Publish Tag pages
    tags = {}
    for p in blog.posts:
        for t in p.meta['tags']:
            if t in tags:
                tags[t].append(p)
            else:
                tags[t] = [p]

    for t in tags:
        posts = sorted(tags[t], key=lambda p: p.meta['published'])
        title = "Posts Tagged %s" % t
        output_path = "tag/%s" % t
        publish_posts(
                posts, 
                blog.env.get_template("posts.html"), 
                blog.settings, 
                output_path, 
                title=title
                )
        print "Published Tag Page for %s" % t

if __name__ == '__main__':
    path = sys.argv[1]
    b = core.Blog(path)
    publish(b)

