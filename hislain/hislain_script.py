import os
import sys
import shutil

from dateutil import parser
from datetime import datetime
from hashlib import md5

import PyRSS2Gen as RSS2
import yaml

import core
import utils

def _write_template(template, filepath, blog, **kwargs):
    file_path = os.path.join(blog.settings['out_path'], filepath)
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    out_file = file(file_path, 'w')
    out_file.write(template.render(dict(settings=blog.settings, hooks=blog.hooks, **kwargs)))

def publish_post(post, template, blog):
    _write_template(template, post.meta['permalink'], post=post, blog=blog)
   
def publish_posts(posts, template, blog, output_path, **kwargs):
    _write_template(template, output_path, posts=posts, blog=blog, **kwargs)

def publish(blog):
  # Get currently published blog posts list, if it's there    
    published_path = os.path.join(blog.settings['blog_dir'], '.published')
    if not os.path.exists(published_path): 
        published = {}
    else:
        published = yaml.load(file(published_path))

    for p in blog.posts:
        hash = md5(p.content).hexdigest()
        if p.source_path in published:
            if not hash == published[p.source_path]:
                p.save()
        else:
            p.save()
        published[p.source_path] = hash
    yaml.dump(published, file(published_path, 'w'))

  # Move the static & media files
    to_move = [ (os.path.join(blog.settings['theme_path'], 'static'),
                 os.path.join(blog.settings['out_path'], 'static')),
                (blog.settings['media_path'],
                 os.path.join(blog.settings['out_path'], 'media'))
              ]    
    for f, t in to_move:
        if os.path.exists(t):
            shutil.rmtree(t)
        shutil.copytree(f, t)
        print "Copied %s" % t

#   Move files added by plugins
    for f in blog.hooks.static_files:
        shutil.copyfile(os.path.join(blog.settings['blog_dir'], f),
                        os.path.join(blog.settings['out_path'], 'static', os.path.basename(f)))


  # Publish Posts
    for p in blog.posts:
        publish_post(p, blog.env.get_template('post.html'), blog)
        print "Published Post %s" % p.title


    #Publish Home Page
    home_posts = sorted(blog.posts, key=lambda p: p.meta['published'])[-10:][::-1]
    publish_posts(home_posts, blog.env.get_template('posts.html'), blog, output_path='index.html', title='Home Page', permalink='/')
    print "Published Home page"
  
    # Publish RSS
    rss_posts = [ 
            RSS2.RSSItem(
                title=p.title,
                link=blog.settings['base_url'] + p.meta['permalink'],
                description=p.render_html(),
                guid=RSS2.Guid(blog.settings['base_url'] + p.meta['permalink']),
                pubDate=p.meta['published']
                )
            for p in home_posts
            ]

    rss = RSS2.RSS2(
            title=blog.settings['name'],
            link=blog.settings['base_url'],
            lastBuildDate=datetime.now(),
            description=blog.settings['tagline'],
            items=rss_posts )
    rss_file = file(os.path.join(blog.settings['out_path'], 'feed'), 'w')
    rss.write_xml(rss_file)
    rss_file.close()
    print "Published RSS Feed"

    # Publish Pages
    for p in blog.pages:
        publish_post(p, blog.env.get_template('post.html'), blog)
        print "Published Page %s" % p.title

    # Publish Monthly Archives

    # Publish Yearly Archives

    # Publish Tag pages
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
        output_path = "tag/%s.html" % t
        publish_posts(
                posts, 
                blog.env.get_template("posts.html"), 
                blog, 
                output_path, 
                title=title
                )
        print "Published Tag Page for %s" % t

if __name__ == '__main__':
    path = sys.argv[1]
    b = core.Blog(path)
    publish(b)

