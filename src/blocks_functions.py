import re
from enum import Enum

from inline_functions import text_to_textnodes, text_node_to_html_node
from htmlnode import ParentNode, LeafNode

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

def text_to_html_nodes(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

def list_block_to_html(block, tag):
    lines = block.split("\n")
    # remove numbers or dashes from the beginning of a line
    lines = [line.split(" ", 1)[-1] for line in lines]
    # enclose every line into <li></li> tag
    li_nodes = [ParentNode("li", text_to_html_nodes(line)) for line in lines]
    return ParentNode(tag, li_nodes)

def prepare_text_quote(block):
    lines = block.split("\n")
    # remove > from the beginning and add <br> tag to the end
    lines = [line.split(">", 1)[-1].strip() + "<br>" for line in lines]
    # remove <br> tag from the last line
    lines[-1] = lines[-1][:-4]
    # put together all lines into one text
    text = ""
    for line in lines:
        text += line
    return text

def markdown_to_html_node(markdown):
    """
    blocks:
        - paragraph
        - heading
        - code
        - quote
        - unordered_list
        - ordered_list
    inline:
        - normal text
        - bold text
        - italic text
        - code text
        - link
        - image
    """
    blocks = markdown_to_blocks(markdown)
    blocks_html = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH_BLOCK_TYPE:
                block = block.replace("\n", " ")
                blocks_html.append(ParentNode("p", text_to_html_nodes(block)))
            case BlockType.HEADING_BLOCK_TYPE:
                # split hashtags and text
                tag, text = block.split(" ", 1)
                blocks_html.append(ParentNode(f"h{len(tag)}", text_to_html_nodes(text)))
            case BlockType.CODE_BLOCK_TYPE:
                # strip ``` at the beginning and end
                blocks_html.append(ParentNode("pre", [LeafNode("code", block[3:-3].lstrip())]))
            case BlockType.QUOTE_BLOCK_TYPE:
                text = prepare_text_quote(block)
                blocks_html.append(ParentNode("blockquote", text_to_html_nodes(text)))
            case BlockType.UNORDERED_LIST_BLOCK_TYPE:
                blocks_html.append(list_block_to_html(block, "ul"))
            case BlockType.ORDERED_LIST_BLOCK_TYPE:
                blocks_html.append(list_block_to_html(block, "ol"))
            case _:
                raise ValueError("Not valid block type")
    return ParentNode("div", blocks_html)
    