class HTMLNode():
    def __init__(self, tag=None, value=None, childen=None, props=None):
        self.tag = tag
        self.value = value
        self.children = childen
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return_str = ""
        for prop in self.props:
            return_str += f' {prop}="{self.props[prop]}"'
        return return_str
    
    def __repr__(self):
        return (f"HTMLNode({self.tag}, {self.value}, "
                f"{self.children}, {self.props})")
    
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