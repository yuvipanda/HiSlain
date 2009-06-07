import unittest
import os
from StringIO import StringIO

import core 
import hislain_script

class TestPost(unittest.TestCase):
    def test_basic(self):
        file = """Hello World!
tags: hello world, beginning

Hey fellas! I'm just out here, saying hello world! :)"""
        p = core.Post(StringIO(file))
        self.assertEqual(p.title, "Hello World!")
        self.assertEqual(p.meta['tags'], ['hello world', 'beginning'])
        self.assertEqual(p.content_raw, "Hey fellas! I'm just out here, saying hello world! :)")

    def test_write(self):
        output = """Hello World!
tags: hello world, beginning

Hey fellas! I'm just out here, saying hello world! :)"""
        p = core.Post()
        p.title = "Hello World!"
        p.meta['tags'] = ['hello world', 'beginning']
        p.content_raw = "Hey fellas! I'm just out here, saying hello world! :)"
        so = StringIO()
        p.to_file(so)
        self.assertEqual(so.getvalue(),output)

class TestBlog(unittest.TestCase):
    def test_basic(self):
        test_dir = os.path.join(os.path.dirname(__file__), "sample-blog")
        blog = core.Blog(test_dir)

        self.assertEqual(len(blog.posts), 2)
        self.assertEqual(blog.settings['theme'], 'simpl')
        self.assertEqual(len(blog.settings), 2)

class TestConfig(unittest.TestCase):
    def test_basic(self):
        file = """name: YuviSense
theme: simpl

links:
    - name: Stats blog
      url: http://thestatbot.com
    - name: Scoble
      url: http://scobleizer.com"""

        conf = core.read_config(StringIO(file))
        
        self.assertEqual(len(conf), 3)        
        self.assertEqual(conf['name'], 'YuviSense')
        self.assertEqual(conf['theme'], 'simpl')
        self.assertEqual(len(conf['links']), 2)
        self.assertEqual(conf['links'][0]['name'], 'Stats blog')
        self.assertEqual(conf['links'][0]['url'], 'http://thestatbot.com')
        self.assertEqual(conf['links'][1]['name'], 'Scoble')
        self.assertEqual(conf['links'][1]['url'], 'http://scobleizer.com')
