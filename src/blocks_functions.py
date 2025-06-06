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
    lines = block.split("\n")
    if len(re.findall(r"^>", block, re.MULTILINE)) == len(lines):
        return BlockType.QUOTE_BLOCK_TYPE
    if len(re.findall(r"- ", block, re.MULTILINE)) == len(lines):
        return BlockType.UNORDERED_LIST_BLOCK_TYPE
    ordered_list_matches = re.findall(r"^\d+\. ", block, re.MULTILINE)
    # every line must start with number, "." and space
    if len(ordered_list_matches) == len(lines):
        # the first number in the first line must be 1
        if int(ordered_list_matches[0][0]) == 1:
            # split to only numbers
            numbers = [ordered_list_match.split(".")[0] for ordered_list_match in ordered_list_matches]
            is_ordered_list = True
            # numbers must increment by one for each line
            for i in range(1, len(ordered_list_matches) + 1):
                if i != int(numbers[i - 1]):
                    is_ordered_list = False
                    break
            if is_ordered_list:
                return BlockType.ORDERED_LIST_BLOCK_TYPE
    return BlockType.PARAGRAPH_BLOCK_TYPE