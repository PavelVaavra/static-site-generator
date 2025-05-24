from enum import Enum

class TextType(Enum):
    NORMAL_TEXT_TYPE = "normal"
    BOLD_TEXT_TYPE = "bold"
    ITALIC_TEXT_TYPE = "italic"
    CODE_TEXT_TYPE = "code"
    LINK_TEXT_TYPE = "link"
    IMAGE_TEXT_TYPE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and \
                self.text_type == other.text_type and \
                self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"