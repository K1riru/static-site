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



def extract_markdown_images(text):
    import re
    pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    images = []
    for alt, url in matches:
        images.append((alt, url))
    return images

def extract_markdown_links(text):
    import re
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    links = []
    for text, url in matches:
        links.append((text, url))
    return links


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for alt, url in images:
            parts = remaining_text.split(f"![{alt}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining_text = parts[1]
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes
        

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for text, url in links:
            parts = remaining_text.split(f"[{text}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            remaining_text = parts[1]
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes



def text_to_textnodes(text):
    raw_node = TextNode(text, TextType.TEXT)
    nodes_with_delimiter_bold = split_nodes_delimiter([raw_node], "**", TextType.BOLD)
    nodes_with_delimiter_italic = split_nodes_delimiter(nodes_with_delimiter_bold, "_", TextType.ITALIC)
    nodes_with_delimiter_code = split_nodes_delimiter(nodes_with_delimiter_italic, "`", TextType.CODE)
    nodes_with_images = split_nodes_image(nodes_with_delimiter_code)
    nodes_with_links = split_nodes_link(nodes_with_images)
    return nodes_with_links