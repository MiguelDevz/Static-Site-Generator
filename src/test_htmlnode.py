import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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
        self.assertEqual(' id="main"  class="container"', node.props_to_html())

class TestLeafNode(unittest.
TestCase):
    def test_leaf_to_html_p(self):
        #Test with tag and value
        node = LeafNode("p", "This is a LeafNode",)
        self.assertEqual(node.to_html(), "<p>This is a LeafNode</p>")

    def test_Leaf_to_html_no_tag(self):
        #Test with no tag
        node = LeafNode(None, "This is a LeafNode")
        self.assertEqual(node.to_html(), "This is a LeafNode")
        
    def test_leaf_to_html_no_value(self):
        #Test with no value
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>")

    def test_to_html_multiple_children(self):
        child_node1 = LeafNode("p", "This is a paragraph")
        child_node2  = LeafNode("span", "This is a span")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(),"<div><p>This is a paragraph</p><span>This is a span</span></div>")

    def test_to_html_none_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "ParentNode is missing children")

    def test_to_html_no_tag(self):
        child_node = LeafNode("p", "this is a paragraph")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have a tag")

if __name__ == "__main__":
    unittest.main()