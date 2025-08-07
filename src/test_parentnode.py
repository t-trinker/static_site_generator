import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class test_parentnode(unittest.TestCase):
    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchild(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_to_html_with_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("div", "child2")
        child_node3 = LeafNode("i", "child3")
        child_node4 = LeafNode("b", "child4")
        
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3, child_node4])
        
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><div>child2</div><i>child3</i><b>child4</b></div>")
        
    def test_to_html_with_grandchildre(self):
        grandchild_node1 = LeafNode("b", "grandchild1")
        grandchild_node2 = LeafNode("i", "grandchild2")
        grandchild_node3 = LeafNode("span", "grandchild3")
        grandchild_node4 = LeafNode("div", "grandchild4")
        child_node1 = ParentNode("span", [grandchild_node1, grandchild_node2])
        child_node2 = ParentNode("span", [grandchild_node3, grandchild_node4])
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild1</b><i>grandchild2</i></span><span><span>grandchild3</span><div>grandchild4</div></span></div>",
        )        

if __name__ == "__main__":
    unittest.main()