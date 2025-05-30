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