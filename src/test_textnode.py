import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text Node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_fields(self):
        node = TextNode("one", TextType.CODE, "url")
        self.assertEqual(node.text, "one")
        self.assertEqual(node.text_type, TextType.CODE)
        self.assertEqual(node.url, "url")


if __name__ == "__main__":
    unittest.main()