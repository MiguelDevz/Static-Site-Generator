import re
from textnode import TextType, TextNode


def split_nodes_delimiter(old_node, delimiter, text_type):
    node_list = []
    for node in old_node:
        if node.text_type != TextType.TEXT:
            node_list.append(node)
            continue
        #splits nodes by delimiter (ex: "_" for italic)
        split_text = node.text.split(delimiter)
        #if even # of parts markdown is invalid should be odd
        if len(split_text) % 2 == 0:
            raise Exception("invalid Markdown syntax")
        for i, text in enumerate(split_text):
            #even indexs is normal text
            if i % 2 == 0:
                node_list.append(TextNode(text, TextType.TEXT))
            #odd indexs are special md like bold or italic
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

            #Text before image
            if parts[0]:
                node_list.append(TextNode(parts[0], TextType.TEXT))

            #image node
            node_list.append(TextNode(alt, TextType.IMAGE, url))

            # If there is more text after the image keep it for the next loop
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""

        # After all images, if there is leftover text add it as a text node
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

            #Text before link
            if parts[0]:
                node_list.append(TextNode(parts[0], TextType.TEXT))

            #link node
            node_list.append(TextNode(alt, TextType.LINK, url))

            # If there is more text after the link keep it for the next loop
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""

        # After all links, if there is leftover text add it as a text node
        if current_text:
            node_list.append(TextNode(current_text, TextType.TEXT))

    return node_list


def text_to_textnodes(text):
    #passes each output as next input to check through all TextTypes
    node = [TextNode(text, TextType.TEXT)]
    image_nodes = split_nodes_image(node)
    link_nodes = split_nodes_link(image_nodes)
    bold_nodes = split_nodes_delimiter(link_nodes, "**", TextType.BOLD)
    italic_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
    code_nodes = split_nodes_delimiter(italic_nodes, "`", TextType.CODE)
    #returns a list of TextNodes of each TextType that are in the text
    return code_nodes




def extract_markdown_images(text):
    #regex for images
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    #regex for links
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)