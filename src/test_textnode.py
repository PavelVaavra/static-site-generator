import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT_TYPE, None)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT_TYPE)
        self.assertEqual(node, node2)

    def test_not_eg(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT_TYPE)
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT_TYPE)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is some anchor text", TextType.LINK_TEXT_TYPE, "https://www.boot.dev")
        self.assertEqual(repr(node), "TextNode(This is some anchor text, link, https://www.boot.dev)")


if __name__ == "__main__":
    unittest.main()