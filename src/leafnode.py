from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        html_str = f"<{self.tag}"
        if self.props is not None:
            html_str += self.props_to_html()
        html_str += ">"
        html_str += f"{self.value}"
        if self.tag != "img":
            html_str += f"</{self.tag}>"
        return html_str