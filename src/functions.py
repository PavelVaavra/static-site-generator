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
            new_nodes.extend(old_node)
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