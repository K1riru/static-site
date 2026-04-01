import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq_text(self):
        node = TextNode("Hello",TextType.TEXT)
        node2 = TextNode("Hello world", TextType.TEXT)
        self.assertNotEqual(node,node2)

    def test_noteq_url(self):
        node = TextNode("Link",TextType.LINK,"https://a.com")
        node2 = TextNode("Link", TextType.LINK, "https://b.com")
        self.assertNotEqual(node,node2)

    def test_default_url(self):
        node = TextNode("No url",TextType.TEXT)
        node2 = TextNode("No url", TextType.TEXT, None)
        self.assertEqual(node,node2)

if __name__ == "__main__":
    unittest.main()