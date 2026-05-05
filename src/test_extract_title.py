import unittest
from textnode import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")

    def test_extract_title_with_whitespace(self):
        md = "   #   Hello World   \n\nSome content"
        self.assertEqual(extract_title(md), "Hello World")

    def test_no_h1_raises(self):
        md = "## Not a top header\n#Not a header either"
        with self.assertRaises(Exception):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()
