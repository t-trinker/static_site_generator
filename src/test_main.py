import unittest

from main import extract_title

class test_main(unittest.TestCase):
    def test_extract_title(self):
        md = "# hello"
        result = extract_title(md)
        self.assertEqual(result, "hello")
        
    def test_extract_title_no_title(self):
        md = "hello"
        with self.assertRaises(Exception):
            result = extract_title(md)
            
    def test_extract_title_multiple_headings(self):
        md = """
# heading

## 2nd heading

### 3rd heading

        """
        result = extract_title(md)
        self.assertEqual(result, "heading")
