import os

from dateutil import parser
from datetime import datetime

import core
import utils

def publish_post(post, template, settings):
    file_path = os.path.join(settings['out_path'], post.get_slug())
    out_file = file(file_path, 'w')
    out_file.write(template.render({'post':post, 'settings':settings}))

def publish_posts(posts, template, settings, output_path):
    file_path = os.path.join(settings['out_path'], output_path)
    out_file = file(file_path, 'w')
    out_file.write(template.render({'posts': posts, 'settings': settings}))

def publish(blog):
    #Publish Posts

    #Publish RSS

    #Publish Home Page
  
    #Publish Pages

    #Publish Monthly Archives

    #Publish Yearly Archives

    #Publish Tag pages
    pass
