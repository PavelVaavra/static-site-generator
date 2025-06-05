import re

from enum import Enum

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if len(block) != 0]

class BlockType(Enum):
    PARAGRAPH_BLOCK_TYPE = "paragraph"
    HEADING_BLOCK_TYPE = "heading"
    CODE_BLOCK_TYPE = "code"
    QUOTE_BLOCK_TYPE = "quote"
    UNORDERED_LIST_BLOCK_TYPE = "unordered_list"
    ORDERED_LIST_BLOCK_TYPE = "ordered_list"

def block_to_block_type(block):
    if re.search(r"^#{1,6} .+", block):
        return BlockType.HEADING_BLOCK_TYPE
    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE_BLOCK_TYPE
    quote, unordered = True, True
    for line in block.split("\n"):
        print(line[0])
        if line[0] != ">":
            quote = False
    if quote:
        return BlockType.QUOTE_BLOCK_TYPE