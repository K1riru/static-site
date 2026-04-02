class HTMLNode:
    def __init__(self, tag =None, value =None, children = None, props =None):
        self.tag = tag
        self.value = value
        self.children = children 
        self.props = props 
    

    def to_html(self):
        raise NotImplementedError("Child classes must implement to_html()")
    
    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join(f'{k}="{v}"' for k,v in self.props.items())



    def __repr__(self):
        return (f"HTMLNode(tag={self.tag!r}, value={self.value!r}, "
        f"children={self.children!r}, props={self.props!r})")


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        # Leaf nodes do not accept children; tag and value are required
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return (f"LeafNode(tag={self.tag!r}, value={self.value!r}, "
                f"props={self.props!r})")