import unittest

from blocks_functions import (
    markdown_to_blocks,
    BlockType,
    block_to_block_type
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
    # def test_paragraph(self):
    #     block = "Here's the deal, **I like Tolkien**."
    #     self.assertEqual(
    #         block_to_block_type(block),
    #         BlockType.PARAGRAPH_BLOCK_TYPE
    #     )
    
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

#     def test_quote(self):
#         block = """> "I am in fact a Hobbit in all but size."
# >
# > -- J.R.R. Tolkien
# """
#         self.assertEqual(
#             block_to_block_type(block),
#             BlockType.QUOTE_BLOCK_TYPE
#         )
# 
#     def test_unordered_list(self):
#         block = """- You can spend years studying the legendarium and still not understand its depths
# - It can be enjoyed by children and adults alike
# - Disney _didn't ruin it_ (okay, but Amazon might have)
# - It created an entirely new genre of fantasy
# """
#         self.assertEqual(
#             block_to_block_type(block),
#             BlockType.UNORDERED_LIST_BLOCK_TYPE
#         )

#     def test_ordered_list(self):
#         block = """1. Gandalf
# 2. Bilbo
# 3. Sam
# 4. Glorfindel
# 5. Galadriel
# """
#         self.assertEqual(
#             block_to_block_type(block),
#             BlockType.ORDERED_LIST_BLOCK_TYPE
#         ) 

if __name__ == "__main__":
    unittest.main()