import unittest
import postparser
from StringIO import StringIO

class TestParser(unittest.TestCase):
    def test_basic(self):
        file = """Hello World!
Tags: hello world, beginning

Hey fellas! I'm just out here, saying hello world! :)
        """
        p = postparser.post_from_file(StringIO(file))
        self.assertEqual(p.title, "Hello World!")
        self.assertEqual(len(p.meta), 1)
        self.assertEqual(p.meta['Tags'], "hello world, beginning")
        self.assertEqual(p.content, "Hey fellas! I'm just out here, saying hello world! :)")
