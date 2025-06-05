import re

from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL_TEXT_TYPE:
            return LeafNode(None, text_node.text)
        case TextType.BOLD_TEXT_TYPE:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC_TEXT_TYPE:
            return LeafNode("i", text_node.text)
        case TextType.CODE_TEXT_TYPE:
            return LeafNode("code", text_node.text)
        case TextType.LINK_TEXT_TYPE:
            return LeafNode("a", text_node.text, { "href": text_node.url })
        case TextType.IMAGE_TEXT_TYPE:
            return LeafNode("img", "", {
                "src": text_node.url,
                "alt": text_node.text
            })
        case _:
            raise ValueError
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT_TYPE:
            new_nodes.append(old_node)
            continue
        parts = old_node.text.split(delimiter)
        if len(parts) % 2 != 1:
            raise Exception("split_nodes_delimiter(): delimiters aren't in pairs")
        normal_text_type = True
        for part in parts:
            if part == "":
                continue
            if normal_text_type:
                new_nodes.append(TextNode(part, TextType.NORMAL_TEXT_TYPE))
            else:
                new_nodes.append(TextNode(part, text_type))
            normal_text_type = not(normal_text_type)

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((\S*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((\S*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT_TYPE:
            new_nodes.append(old_node)
            continue
        delimiter = extract_markdown_images(old_node.text)
        if len(delimiter) == 0:
            new_nodes.append(old_node)
            continue
        parts = old_node.text.split(f"![{delimiter[0][0]}]({delimiter[0][1]})")
        if parts[0] != "":
            new_nodes.append(TextNode(parts[0], TextType.NORMAL_TEXT_TYPE))
        new_nodes.append(TextNode(delimiter[0][0], TextType.IMAGE_TEXT_TYPE, delimiter[0][1]))
        if parts[-1] != "":
            new_nodes.extend(split_nodes_image([TextNode(parts[-1], TextType.NORMAL_TEXT_TYPE)]))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT_TYPE:
            new_nodes.append(old_node)
            continue
        delimiter = extract_markdown_links(old_node.text)
        if len(delimiter) == 0:
            new_nodes.append(old_node)
            continue
        parts = old_node.text.split(f"[{delimiter[0][0]}]({delimiter[0][1]})")
        if parts[0] != "":
            new_nodes.append(TextNode(parts[0], TextType.NORMAL_TEXT_TYPE))
        new_nodes.append(TextNode(delimiter[0][0], TextType.LINK_TEXT_TYPE, delimiter[0][1]))
        if parts[-1] != "":
            new_nodes.extend(split_nodes_link([TextNode(parts[-1], TextType.NORMAL_TEXT_TYPE)]))

    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.NORMAL_TEXT_TYPE)
    text_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT_TYPE)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC_TEXT_TYPE)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE_TEXT_TYPE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes