from core import *
from hislain_script import *

b = Blog('sample-blog')
p = b.posts[0]


publish_posts(b.posts, b.env.get_template('home.html'), b.settings, 'home') 
