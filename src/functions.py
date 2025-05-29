from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL_TEXT_TYPE:
            return LeafNode(None, text_node.text)
        case _:
            raise ValueError