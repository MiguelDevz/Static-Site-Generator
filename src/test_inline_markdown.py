import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

class TestInlineMarkdown(unittest.TestCase):
    def test_code_nodes(self):
        node_code = TextNode("Text with `code` block", TextType.TEXT)
        code_nodes = split_nodes_delimiter([node_code], "`", TextType.CODE)
        self.assertEqual(code_nodes, [
            TextNode("Text with ", TextType .TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT)
        ])

    def test_bold_nodes(self):
        node_bold = TextNode("Text with **bold** word", TextType.TEXT)
        bold_nodes = split_nodes_delimiter([node_bold], "**", TextType.BOLD)
        self.assertEqual(bold_nodes, [
            TextNode("Text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
        ])

    def test_italic_nodes(self):
        node_italic = TextNode("Text with _italic_ word", TextType.TEXT)
        italic_nodes = split_nodes_delimiter([node_italic], "_", TextType.ITALIC)
        self.assertEqual(italic_nodes, [
            TextNode("Text with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
        ])