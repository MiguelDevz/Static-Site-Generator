import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("div", "This is a div", props={"class": "container"})
        node2 = HTMLNode("div", "This is a div", props={"class": "container"})
        self.assertEqual(node, node2)

    def test_neq(self):
        node = HTMLNode("div", "This is a div", props={"class": "container"})
        node2 = HTMLNode("div", "This is a different div", props={"class": "container"})
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = HTMLNode("div", "This is a div", props={"class": "container"})
        self.assertEqual('<div class="container">This is a div</div>', repr(node))

    def test_props_to_html(self):
        node = HTMLNode("div", "This is a div", props={"id": "main", "class": "container"})
        self.assertEqual('id="main" class="container"', node.props_to_html())