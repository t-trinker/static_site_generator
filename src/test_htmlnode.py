import unittest

from htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
    def test_props_none(self):
        node = HtmlNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_props(self):
        node_child1 = HtmlNode()
        node_child2 = HtmlNode()
        children = [node_child1, node_child2]
        props = {"href": "http://google.de", "dummy": "dummyvalue"}

        node = HtmlNode("tag", "value", children, props)
        self.assertEqual(node.tag, "tag")
        self.assertEqual(node.value, "value")
        self.assertEqual(node.children, [node_child1, node_child2])
        self.assertEqual(node.props, {"href": "http://google.de", "dummy": "dummyvalue"})

    def test_props_to_html(self):
        properties = {"href": "http://google.de", "dummy": "dummyvalue"}
        node = HtmlNode(props=properties)
        self.assertEqual(node.props_to_html(), ' href="http://google.de" dummy="dummyvalue"')


if __name__ == "__main__":
    unittest.main()