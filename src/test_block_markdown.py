import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

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
                         
                    
if __name__ == "__main__":
    unittest.main()