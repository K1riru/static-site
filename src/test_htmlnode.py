import unittest

from src.htmlnode import HTMLNode


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