import unittest

from textnode import TextNode, TextType
from functions import text_node_to_html_node

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT_TYPE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text", TextType.BOLD_TEXT_TYPE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text")
        self.assertEqual(html_node.to_html(), "<b>This is a bold text</b>")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC_TEXT_TYPE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")
    
    def test_code(self):
        node = TextNode("print('Hello world')", TextType.CODE_TEXT_TYPE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello world')")
        self.assertEqual(html_node.to_html(), "<code>print('Hello world')</code>")

    def test_link(self):
        node = TextNode("Click me!", TextType.LINK_TEXT_TYPE, "google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.to_html(), '<a href="google.com">Click me!</a>')

    def test_link(self):
        node = TextNode("face", TextType.IMAGE_TEXT_TYPE, "src/face.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.to_html(), '<img src="src/face.png" alt="face">')

if __name__ == "__main__":
    unittest.main()