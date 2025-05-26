from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag in ParentNode")
        if self.children is None:
            raise ValueError("No children in ParentNode")
        html_str = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_str += child.to_html()
        html_str += f"</{self.tag}>"   
        return html_str
    
    def __repr__(self):
        return (f"ParentNode({self.tag}, {self.children}, {self.props})")