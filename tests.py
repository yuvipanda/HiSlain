import unittest
import os
from StringIO import StringIO

import hislain 

class TestPost(unittest.TestCase):
    def test_basic(self):
        file = """Hello World!
Tags: hello world, beginning

Hey fellas! I'm just out here, saying hello world! :)"""
        p = hislain.Post(StringIO(file))
        self.assertEqual(p.title, "Hello World!")
        self.assertEqual(len(p.meta), 1)
        self.assertEqual(p.meta['Tags'], "hello world, beginning")
        self.assertEqual(p.content, "Hey fellas! I'm just out here, saying hello world! :)")

    def test_write(self):
        output = """Hello World!
Tags: hello world, beginning

Hey fellas! I'm just out here, saying hello world! :)"""
        p = hislain.Post()
        p.title = "Hello World!"
        p.meta['Tags'] = "hello world, beginning"
        p.content = "Hey fellas! I'm just out here, saying hello world! :)"
        so = StringIO()
        p.to_post(so)
        self.assertEqual(so.getvalue(),output)

class TestBlog(unittest.TestCase):
    def test_basic(self):
        test_dir = os.path.join(os.path.dirname(__file__), "sample-blog")
        blog = hislain.Blog(test_dir)

        self.assertEqual(len(blog.posts), 1)
        self.assertEqual(blog.settings['theme'], 'simpl')
        self.assertEqual(len(blog.settings), 1)

class TestConfig(unittest.TestCase):
    def test_basic(self):
        file = """name: YuviSense
theme: simpl

links:
    - name: Stats blog
      url: http://thestatbot.com
    - name: Scoble
      url: http://scobleizer.com"""

        conf = hislain.read_config(StringIO(file))
        
        self.assertEqual(len(conf), 3)        
        self.assertEqual(conf['name'], 'YuviSense')
        self.assertEqual(conf['theme'], 'simpl')
        self.assertEqual(len(conf['links']), 2)
        self.assertEqual(conf['links'][0]['name'], 'Stats blog')
        self.assertEqual(conf['links'][0]['url'], 'http://thestatbot.com')
        self.assertEqual(conf['links'][1]['name'], 'Scoble')
        self.assertEqual(conf['links'][1]['url'], 'http://scobleizer.com')
