from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("No value in LeafNode")
        if self.tag is None:
            return self.value
        html_str = f"<{self.tag}"
        html_str += self.props_to_html()
        html_str += ">"
        html_str += f"{self.value}"
        if self.tag != "img":
            html_str += f"</{self.tag}>"
        return html_str
    
    def __repr__(self):
        return (f"LeafNode({self.tag}, {self.value}, {self.props})")