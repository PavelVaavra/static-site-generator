import unittest

from blocks_functions import (
    markdown_to_blocks,
    BlockType,
    block_to_block_type,
    markdown_to_html_node
)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "Here's the deal, **I like Tolkien**."
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH_BLOCK_TYPE
        )
    
    def test_heading(self):
        block = "## Reasons I like Tolkien"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING_BLOCK_TYPE
        )

    def test_code(self):
        block = """```
func main(){
    fmt.Println("Aiya, Ambar!")
}
```"""
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE_BLOCK_TYPE
        )

    def test_quote(self):
        block = """> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien"""
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE_BLOCK_TYPE
        )

    def test_unordered_list(self):
        block = """- You can spend years studying the legendarium and still not understand its depths
- It can be enjoyed by children and adults alike
- Disney _didn't ruin it_ (okay, but Amazon might have)
- It created an entirely new genre of fantasy"""
        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST_BLOCK_TYPE
        )

    def test_ordered_list(self):
        block = """1. Gandalf
2. Bilbo
3. Sam
4. Glorfindel
5. Galadriel
6. Bilbo
7. Sam
8. Glorfindel
9. Galadriel
10. Bilbo
11. Sam
12. Glorfindel
13. Galadriel"""
        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST_BLOCK_TYPE
        )

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_ordered_list(self):
        md = """
1. Gandalf [boot.dev](https://boot.dev)
2. Bilbo **bold**
3. Sam
4. Glorfindel
5. Galadriel
6. Elrond
7. Thorin _italic_ ahoj
8. Sauron
9. ![Aragorn](src/images/img.png)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ol><li>Gandalf <a href="https://boot.dev">boot.dev</a></li><li>Bilbo <b>bold</b></li><li>Sam</li><li>Glorfindel</li><li>Galadriel</li>'
            '<li>Elrond</li><li>Thorin <i>italic</i> ahoj</li><li>Sauron</li><li><img src="src/images/img.png" alt="Aragorn"></li></ol></div>',
        )

    def test_unordered_list(self):
        md = """
- You can spend years studying the legendarium and still not understand its depths
- It can be enjoyed by children and adults alike
- Disney _didn't ruin it_ (okay, but Amazon might have)
- It created an entirely new genre of fantasy
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ul><li>You can spend years studying the legendarium and still not understand its depths</li>'
            '<li>It can be enjoyed by children and adults alike</li>'
            '<li>Disney <i>didn\'t ruin it</i> (okay, but Amazon might have)</li>'
            '<li>It created an entirely new genre of fantasy</li></ul></div>',
        )

if __name__ == "__main__":
    unittest.main()