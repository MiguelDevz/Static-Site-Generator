from textnode import TextType, TextNode

def split_nodes_delimiter(old_node, delimiter, text_type):
    node_list = []
    for node in old_node:
        if node.text_type != TextType.TEXT:
            node_list.append(node)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception("invalid Markdown syntax")
        for i, text in enumerate(split_text):
            if i % 2 == 0:
                node_list.append(TextNode(text, TextType.TEXT))
            else:
                node_list.append(TextNode(text, text_type))
    return node_list