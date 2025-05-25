import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html1(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("a", None, None, props)
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())

    def test_props_to_html2(self):
        node = HTMLNode("a", None, None, None)
        self.assertEqual("", node.props_to_html())

    def test_repr(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("a", "Click me!", None, props)
        self.assertEqual(
            "HTMLNode(a, Click me!, None, " \
            "{'href': 'https://www.google.com', 'target': '_blank'})", 
        repr(node))

    def test_to_html(self):
        node = HTMLNode("p", "Paragraph 2", None, None)
        with self.assertRaises(NotImplementedError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()