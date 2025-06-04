import unittest

from textnode import TextNode, TextType
from functions import (
    text_node_to_html_node, 
    split_nodes_delimiter, 
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)

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

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL_TEXT_TYPE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT_TYPE)
        self.assertEqual(new_nodes, [
                            TextNode("This is text with a ", TextType.NORMAL_TEXT_TYPE),
                            TextNode("code block", TextType.CODE_TEXT_TYPE),
                            TextNode(" word", TextType.NORMAL_TEXT_TYPE),
                        ])
        
    def test_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.NORMAL_TEXT_TYPE)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT_TYPE)
        self.assertEqual(new_nodes, [
                            TextNode("This is text with a ", TextType.NORMAL_TEXT_TYPE),
                            TextNode("bolded phrase", TextType.BOLD_TEXT_TYPE),
                            TextNode(" in the middle", TextType.NORMAL_TEXT_TYPE),
                        ])
        
    def test_italic(self):
        node = TextNode("This is text with a _italic phrase_ in the middle", TextType.NORMAL_TEXT_TYPE)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT_TYPE)
        self.assertEqual(new_nodes, [
                            TextNode("This is text with a ", TextType.NORMAL_TEXT_TYPE),
                            TextNode("italic phrase", TextType.ITALIC_TEXT_TYPE),
                            TextNode(" in the middle", TextType.NORMAL_TEXT_TYPE),
                        ])
        
    def test_more_italic(self):
        node = TextNode("This is _text_ with a _more italic phrases_ in the middle", TextType.NORMAL_TEXT_TYPE)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT_TYPE)
        self.assertEqual(new_nodes, [
                            TextNode("This is ", TextType.NORMAL_TEXT_TYPE),
                            TextNode("text", TextType.ITALIC_TEXT_TYPE),
                            TextNode(" with a ", TextType.NORMAL_TEXT_TYPE),
                            TextNode("more italic phrases", TextType.ITALIC_TEXT_TYPE),
                            TextNode(" in the middle", TextType.NORMAL_TEXT_TYPE),
                        ])
        
    def test_not_matching_delimiters(self):
        node = TextNode("This is text with a `code block word", TextType.NORMAL_TEXT_TYPE)
        with self.assertRaises(Exception):
            _ = split_nodes_delimiter([node], "`", TextType.CODE_TEXT_TYPE)

    def test_multiple_old_nodes(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.NORMAL_TEXT_TYPE)
        another_node = TextNode("This is another text with a **bolded phrase**", TextType.NORMAL_TEXT_TYPE)
        new_nodes = split_nodes_delimiter([node, another_node], "**", TextType.BOLD_TEXT_TYPE)
        self.assertEqual(new_nodes, [
                            TextNode("This is text with a ", TextType.NORMAL_TEXT_TYPE),
                            TextNode("bolded phrase", TextType.BOLD_TEXT_TYPE),
                            TextNode(" in the middle", TextType.NORMAL_TEXT_TYPE),
                            TextNode("This is another text with a ", TextType.NORMAL_TEXT_TYPE),
                            TextNode("bolded phrase", TextType.BOLD_TEXT_TYPE),
                        ])
        
class TestExtractMarkdownImages(unittest.TestCase):
    def test_two_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [
                            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
                            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
                        ])
        
    def test_one_image(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        self.assertEqual(extract_markdown_images(text), [
                            ("image", "https://i.imgur.com/zjjcJKZ.png")
                        ])
        
class TestExtractMarkdownLinks(unittest.TestCase):
    def test_two_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [
                            ("to boot dev", "https://www.boot.dev"), 
                            ("to youtube", "https://www.youtube.com/@bootdotdev")
                        ])
        
class TestSplitNodesImage(unittest.TestCase):
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ",
            TextType.NORMAL_TEXT_TYPE,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT_TYPE),
                TextNode("image", TextType.IMAGE_TEXT_TYPE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TEXT_TYPE),
            ],
            new_nodes,
        )
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT_TYPE,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT_TYPE),
                TextNode("image", TextType.IMAGE_TEXT_TYPE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TEXT_TYPE),
                TextNode(
                    "second image", TextType.IMAGE_TEXT_TYPE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_only_images(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT_TYPE,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE_TEXT_TYPE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE_TEXT_TYPE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

class TestSplitNodesLink(unittest.TestCase):
    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and ",
            TextType.NORMAL_TEXT_TYPE,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.NORMAL_TEXT_TYPE),
                TextNode("to boot dev", TextType.LINK_TEXT_TYPE, "https://www.boot.dev"),
                TextNode(" and ", TextType.NORMAL_TEXT_TYPE),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL_TEXT_TYPE,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.NORMAL_TEXT_TYPE),
                TextNode("to boot dev", TextType.LINK_TEXT_TYPE, "https://www.boot.dev"),
                TextNode(" and ", TextType.NORMAL_TEXT_TYPE),
                TextNode(
                    "to youtube", TextType.LINK_TEXT_TYPE, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_only_links(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL_TEXT_TYPE,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK_TEXT_TYPE, "https://www.boot.dev"),
                TextNode(
                    "to youtube", TextType.LINK_TEXT_TYPE, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

class TestTextToTextnodes(unittest.TestCase):
    def test_text(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL_TEXT_TYPE),
                TextNode("text", TextType.BOLD_TEXT_TYPE),
                TextNode(" with an ", TextType.NORMAL_TEXT_TYPE),
                TextNode("italic", TextType.ITALIC_TEXT_TYPE),
                TextNode(" word and a ", TextType.NORMAL_TEXT_TYPE),
                TextNode("code block", TextType.CODE_TEXT_TYPE),
                TextNode(" and an ", TextType.NORMAL_TEXT_TYPE),
                TextNode("obi wan image", TextType.IMAGE_TEXT_TYPE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL_TEXT_TYPE),
                TextNode("link", TextType.LINK_TEXT_TYPE, "https://boot.dev"),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()