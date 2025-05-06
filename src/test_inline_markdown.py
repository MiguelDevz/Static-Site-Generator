import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](./path/to/image.jpg)")
        self.assertListEqual([("image", "./path/to/image.jpg")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with an [link](https://www.example.com)")
        self.assertEqual([("link", "https://www.example.com")], matches)

    def test_extract_multiple_md_images(self):
        matches = extract_markdown_images("This is text with an ![image](./path/to/image.jpg) and another ![image2](./path/to/image2.jpg)")
        self.assertEqual([("image", "./path/to/image.jpg"), ("image2", "./path/to/image2.jpg")], matches)

    def test_extract_multiple_md_links(self):
        matches = extract_markdown_links("This is text with an [link](https://www.example.com) and another [link2](https://www.example2.com)")
        self.assertEqual([("link", "https://www.example.com"), ("link2", "https://www.example2.com")], matches)