import re
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


def split_nodes_image(old_nodes):
    node_list =[]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            node_list.append(node)
            continue

        img_md = extract_markdown_images    (node.text)
        if img_md == []:
            node_list.append(node)
            continue

        current_text = node.text
        for alt, url in img_md:
            full_image_markdown = f"![{alt}]({url})"
            parts = current_text.split(full_image_markdown, 1)

            if parts[0]:
                node_list.append(TextNode(parts[0], TextType.TEXT))

            node_list.append(TextNode(alt, TextType.IMAGE, url))

            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""

        if current_text:
            node_list.append(TextNode(current_text, TextType.TEXT))

    return node_list


def split_nodes_link(old_nodes):
    node_list =[]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            node_list.append(node)
            continue

        link_md = extract_markdown_links    (node.text)
        if link_md == []:
            node_list.append(node)
            continue

        current_text = node.text
        for alt, url in link_md:
            full_image_markdown = f"[{alt}]({url})"
            parts = current_text.split(full_image_markdown, 1)

            if parts[0]:
                node_list.append(TextNode(parts[0], TextType.TEXT))

            node_list.append(TextNode(alt, TextType.LINK, url))

            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""

        if current_text:
            node_list.append(TextNode(current_text, TextType.TEXT))

    return node_list


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
