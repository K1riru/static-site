import unittest
import tempfile
import os
from src.main import generate_page


class TestGeneratePage(unittest.TestCase):
    def test_generate_writes_file(self):
        with tempfile.TemporaryDirectory() as td:
            md_path = os.path.join(td, "index.md")
            tpl_path = os.path.join(td, "template.html")
            out_path = os.path.join(td, "out", "index.html")

            md_content = "# My Title\n\nThis is a paragraph."
            tpl_content = "<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>"

            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            with open(tpl_path, "w", encoding="utf-8") as f:
                f.write(tpl_content)

            generate_page(md_path, tpl_path, out_path)

            self.assertTrue(os.path.exists(out_path))
            with open(out_path, "r", encoding="utf-8") as f:
                out = f.read()
            self.assertIn("<title>My Title</title>", out)
            self.assertIn("This is a paragraph.", out)


if __name__ == "__main__":
    unittest.main()
