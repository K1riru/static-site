from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    
class TextNode:
    def __init__(self,text,text_type,url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self,other):
        if not isinstance(other,TextNode):
            return False
        return (
            self.text == other.text and 
            self.text_type == other.text_type and
             self.url == other.url
        ) 
    def __repr__(self):
        return f"TextNode({self.text!r}, {self.text_type.value}, {self.url!r})"
    

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img","", {"src": text_node.url, "alt": text_node.text})
    elif text_node.text_type != TextType.TEXT and text_node.text_type != TextType.BOLD and text_node.text_type != TextType.ITALIC and text_node.text_type != TextType.CODE and text_node.text_type != TextType.LINK and text_node.text_type != TextType.IMAGE:
        raise Exception(f"Unsupported text type: {text_node.text_type}")
    else:
        return LeafNode(None, text_node.text)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
                raise Exception("Invalid markdown: unmatched delimiter")


        for i, part in enumerate(parts):
            if part == "":
                continue
            
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes
