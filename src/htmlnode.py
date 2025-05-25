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