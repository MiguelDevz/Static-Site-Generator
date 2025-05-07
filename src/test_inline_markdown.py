import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestInlineMarkdown(unittest.TestCase):

    #Test split_nodes_delimiter
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

    #Test extract_markdown function
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

    #Test split_nodes_image
    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](./images/img) and another ![second image](./images/img2)",
        TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "./images/img"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "./images/img2"
            ),
        ],
        new_nodes,)


    def test_split_links(self):
        node = TextNode("This is text with an [link](https://www.example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com")
        ], new_nodes)

    #Test text_to_textnodes
    def test_nested_text_to_textnodes(self):
        textnodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![image](./images/img) and a [link](https://example.com)")
        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "./images/img"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),

        ], textnodes)

    def test_italic_text_to_testnodes(self):
        textnodes = text_to_textnodes("This is text with an _italic_ word")
        self.assertListEqual([
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
        ], textnodes)
