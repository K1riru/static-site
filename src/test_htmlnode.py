import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="a", props={"href": "https://google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com" target="_blank"')

    def test_props_to_html_empty(self):
        node = HTMLNode(tag="p")
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        child = HTMLNode(tag="span", value="Hello")
        node = HTMLNode(tag="div", children=[child], props={"class": "container"})
        expected = ("HTMLNode(tag='div', value=None, children=[HTMLNode(tag='span', "
                    "value='Hello', children=None, props=None)], props={'class': 'container'})")
        self.assertEqual(repr(node), expected)

if __name__ == "__main__":
    unittest.main()


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_no_tag_returns_raw(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_children_none_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_tag_none_raises(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p", "x")]).to_html()

    def test_empty_children(self):
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>")