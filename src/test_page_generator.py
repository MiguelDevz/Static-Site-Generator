import unittest
from page_generator import extract_title

class TestPageGenerator(unittest.TestCase):
    def test_extract_title(self):
        title = extract_title("""
# My Title
""")
        self.assertEqual(title, "My Title")


    def test_extract_multiple_titles(self):
        title = extract_title("""
### My Title 3
## My Title 2
# My Title 1
""")
        self.assertEqual(title, "My Title 1")