import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    #Testing block_to_block_type function
    def test_block_to_paragraph_type(self):
        paragraph_type = block_to_block_type("This is some text for a markdown paragraph")
        self.assertEqual(paragraph_type, BlockType.PARAGRAPH)

    def test_block_to_ordered_list_type(self):
        ordered_list_type = block_to_block_type("1. apple 2. orange 3. mango")
        self.assertEqual(ordered_list_type, BlockType.ORDERED_LIST)

    def test_block_to_heading_type(self):
        heading_type = block_to_block_type("### markdown 3 heading")
        self.assertEqual(heading_type, BlockType.HEADING)

    #Testing markdown_to_html_node function
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )
        
    def test_quoteblock(self):
        md = """
> This is text that _should_ remain
> the **same** even with inline stuff
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is text that <i>should</i> remain\nthe <b>same</b> even with inline stuff</blockquote></div>",
        )
                         
                    
if __name__ == "__main__":
    unittest.main()