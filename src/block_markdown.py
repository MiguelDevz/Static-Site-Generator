from enum import Enum
import re

def markdown_to_blocks(markdown):
    md_split_lst = markdown.split("\n\n")
    # For each block, strip whitespace and add it to blocks if it's not empty
    blocks = [block.strip() for block in md_split_lst if block.strip()]
    # blocks = list(map(lambda block: block.strip() if block.strip() else None, md_split_lst))
    return blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def block_to_block_type(md_block):
    if re.match(r"#{1,6} ", md_block):
        return BlockType.HEADING
    elif md_block.startswith("```") and md_block.endswith("```"):
        return BlockType.CODE
    elif md_block.startswith(">"):
        return BlockType.QUOTE
    elif md_block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif all(re.match(rf"{i}. ", line) for i, line in enumerate(md_block.split("\n"), start=1)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


md = markdown_to_blocks("""
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
""")
# print(md)

md_type_p = block_to_block_type("This is some text for a markdown paragraph")
md_type_ordered_list = block_to_block_type("1. apple 2. orange 3. mango")
md_type_heading = block_to_block_type("### markdown 3 heading")
print(md_type_p)
print(md_type_ordered_list)
print(md_type_heading)

