import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_a_tag(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        self.assertEqual('<a href="https://www.google.com" ' \
            'target="_blank">Click me!</a>', 
            LeafNode("a", "Click me!", props).to_html())
        
    def test_p_tag(self):
        self.assertEqual("<p>This is a paragraph of text.</p>",
            LeafNode("p", "This is a paragraph of text.").to_html())
        
    def test_img_tag(self):
        props = {
            "src": "img_girl.jpg", 
            "alt": "Girl in a jacket",
            "width": "500",
            "height": "600"
        }
        self.assertEqual('<img src="img_girl.jpg" alt="Girl in a jacket" ' \
            'width="500" height="600">',
            LeafNode("img", "", props).to_html())


if __name__ == "__main__":
    unittest.main()