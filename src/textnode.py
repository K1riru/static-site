from enum import Enum
from htmlnode import LeafNode
from typing import List

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


def markdown_to_blocks(markdown):
    """Split a markdown document into block strings.

    Blocks are separated by a double newline (`\n\n`). Leading/trailing
    whitespace for each block is stripped and empty blocks are removed.
    """
    if markdown is None:
        return []

    parts = markdown.split("\n\n")
    blocks = []
    for part in parts:
        s = part.strip()
        if s:
            blocks.append(s)
    return blocks


class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    """Determine the BlockType for a single markdown block.

    Assumes `block` has had leading/trailing whitespace stripped.
    """
    # Heading: starts with 1-6 # followed by a space
    if block.startswith("#"):
        import re

        m = re.match(r"^(#{1,6})\s+.+", block)
        if m:
            return BlockType.heading

    # Code block: starts with ``` and ends with ```
    if block.startswith("```") and block.endswith("```"):
        return BlockType.code

    # Quote: every line starts with > optionally followed by space
    lines = block.split("\n")
    if all(line.lstrip().startswith(">") for line in lines):
        return BlockType.quote

    # Unordered list: every line starts with "- "
    if all(line.startswith("- ") for line in lines):
        return BlockType.unordered_list

    # Ordered list: lines start with 1.,2.,3.,... sequentially
    import re

    ordered = True
    expected = 1
    for line in lines:
        m = re.match(r"^(\d+)\.\s+.+", line)
        if not m:
            ordered = False
            break
        num = int(m.group(1))
        if num != expected:
            ordered = False
            break
        expected += 1
    if ordered and len(lines) > 0:
        return BlockType.ordered_list

    return BlockType.paragraph


def markdown_to_html_node(markdown):
    """Convert a full markdown document into a single ParentNode (`div`).

    Splits into blocks, classifies each block, converts to appropriate
    HTML nodes, and returns a ParentNode('div', children=...).
    """
    from htmlnode import ParentNode

    blocks = markdown_to_blocks(markdown)

    def text_to_children(text):
        # Convert inline markdown text into a list of HTML nodes
        nodes = []
        for tn in text_to_textnodes(text):
            nodes.append(text_node_to_html_node(tn))
        return nodes

    children = []
    for block in blocks:
        btype = block_to_block_type(block)

        if btype == BlockType.heading:
            import re

            m = re.match(r"^(#{1,6})\s+(.*)$", block, re.S)
            if m:
                level = len(m.group(1))
                text = m.group(2).strip()
                kids = text_to_children(text)
                children.append(ParentNode(f"h{level}", kids))
            else:
                # fallback to paragraph
                kids = text_to_children(block.replace("\n", " "))
                children.append(ParentNode("p", kids))

        elif btype == BlockType.code:
            # extract content between the triple backticks
            content = block
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            # remove a single leading newline if present
            if content.startswith("\n"):
                content = content[1:]
            # keep trailing newlines intact
            from htmlnode import LeafNode

            code_leaf = LeafNode(None, content)
            code_node = ParentNode("code", [code_leaf])
            pre_node = ParentNode("pre", [code_node])
            children.append(pre_node)

        elif btype == BlockType.quote:
            # remove leading > and optional space from each line
            lines = [line.lstrip()[1:].lstrip() if line.lstrip().startswith(">") else line for line in block.split("\n")]
            text = " ".join(lines)
            kids = text_to_children(text)
            children.append(ParentNode("blockquote", [ParentNode("p", kids)]))

        elif btype == BlockType.unordered_list:
            items = []
            for line in block.split("\n"):
                assert line.startswith("- ")
                item_text = line[2:]
                item_kids = text_to_children(item_text)
                items.append(ParentNode("li", item_kids))
            children.append(ParentNode("ul", items))

        elif btype == BlockType.ordered_list:
            items = []
            import re

            for line in block.split("\n"):
                m = re.match(r"^(\d+)\.\s+(.*)$", line)
                if not m:
                    # fallback: treat whole block as paragraph
                    items = None
                    break
                item_text = m.group(2)
                item_kids = text_to_children(item_text)
                items.append(ParentNode("li", item_kids))
            if items is None:
                kids = text_to_children(block.replace("\n", " "))
                children.append(ParentNode("p", kids))
            else:
                children.append(ParentNode("ol", items))

        else:
            # paragraph: replace newlines with spaces
            text = block.replace("\n", " ")
            kids = text_to_children(text)
            children.append(ParentNode("p", kids))

    return ParentNode("div", children)