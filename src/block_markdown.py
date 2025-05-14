from enum import Enum
import re
from htmlnode import HTMLNode, LeafNode, ParentNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown):
    md_split_lst = markdown.split("\n\n")
    # For each block, strip whitespace and add it to blocks if it's not empty
    blocks = [block.strip() for block in md_split_lst if block.strip()]
    # blocks = list(map(lambda block: block.strip() if block.strip() else None, md_split_lst))
    return blocks


def block_to_block_type(md_block):
    lines = md_block.splitlines()

    #Checks for BlockType match, if conditions not met return a paragraph
    if re.match(r"#{1,6} ", md_block):
        return BlockType.HEADING
    elif md_block.startswith("```") and md_block.endswith("```"):
        return BlockType.CODE
    elif md_block.startswith(">"):
        return BlockType.QUOTE
    elif md_block.startswith("- "):
        return BlockType.UNORDERED_LIST
    #check if each line matches the str with the count incremented
    elif all(re.match(rf"{i}. ", line) for i, line in enumerate(md_block.split("\n"), start=1)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    

def text_to_children(text):
    htmlnode_list = []
    from inline_markdown import text_to_textnodes
    from textnode import TextType
    textnodes = text_to_textnodes(text)
    for node in textnodes:
        match(node.text_type):
            case TextType.BOLD:
                htmlnode_list.append(LeafNode("b", node.text))
            case TextType.ITALIC:
                htmlnode_list.append(LeafNode("i", node.text))
            case TextType.CODE:
                htmlnode_list.append(LeafNode("code", node.text))
            case _:
                htmlnode_list.append(LeafNode(None, node.text))
    return htmlnode_list


def markdown_to_html_node(markdown):
    from textnode import TextNode, TextType, text_node_to_html_node
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match(block_type):
            case BlockType.HEADING:
                #splits to 2 groups by ()
                match = re.match(r"(#{1,6}) (.*)", block)
                if match:
                    level = match.group(1)
                    value = match.group(2)
                    tag = f"h{len(level)}"
                    html_nodes.append(ParentNode(tag=tag, children=text_to_children(value), props=None))
            case BlockType.CODE:
                lines = block.splitlines()
                if lines[0].strip() == "```":
                    lines = lines[1:]
                if lines[-1].strip() == "```":
                    lines = lines[:-1]
                #strip "`" join the lines and add newline if needed
                text = "\n".join(lines)
                if not text.endswith("\n"):
                    text += "\n"
                html_nodes.append(ParentNode(tag="pre", children=[text_node_to_html_node(TextNode(text, TextType.CODE))], props=None))
            case BlockType.QUOTE:
                #Removes ">" then strips leading/trailing whitespces
                lines = block.splitlines()
                cleaned = [line.lstrip("> ").strip() for line in lines]
                text = "\n".join(cleaned)
                html_nodes.append(ParentNode(tag="blockquote", children=text_to_children(text), props=None))
            case BlockType.UNORDERED_LIST:
                #a list of lines
                lines = block.split("\n")
                li_nodes = []
                for line in lines:
                    text = line[2:] # removes "- "
                    li_nodes.append(ParentNode(tag="li", children=text_to_children(text), props=None))
                html_nodes.append(ParentNode(tag="ul", children=li_nodes, props=None))
            case BlockType.ORDERED_LIST:
                #a list of lines
                lines = block.split("\n")
                li_nodes = []
                for line in lines:
                    #remove(sub) start(^) of the line with any num of digits(\d+) (1, 2, 3, etc)
                    text = re.sub(r"^\d+\. ", "", line)
                    li_nodes.append(ParentNode(tag="li", children=text_to_children(text), props=None))
                html_nodes.append(ParentNode(tag="ol", children=li_nodes, props=None))
            case _:
                paragraph_text = " ".join(block.splitlines())
                html_nodes.append(ParentNode(tag="p", children=text_to_children(paragraph_text), props=None))
    return ParentNode(tag="div", children=html_nodes, props=None)
            



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
# print(md_type_p)
# print(md_type_ordered_list)
# print(md_type_heading)

print(markdown_to_html_node("""
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
""").to_html())

