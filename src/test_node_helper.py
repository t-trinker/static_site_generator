import unittest
from textnode import TextNode, TextType
from node_helper import text_node_to_html_node, split_nodes_delimiter, return_markdown_images, return_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks

class test_text_node_to_html_node(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, TextType.BOLD.value)
        self.assertEqual(html_node.value, "This is a bold text node")
        
    def test_a_href(self):
        node = TextNode("This is a a href text node", TextType.LINK, url="www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, TextType.LINK.value)
        self.assertEqual(html_node.value, "This is a a href text node")
        self.assertEqual(html_node.props, {"href": "www.google.com"})
        
    def test_image(self):
        node = TextNode("This is a img text node", TextType.IMAGE, url="www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, TextType.IMAGE.value)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "www.google.com", "alt": "This is a img text node"})        
        
class test_split_nodes_delimiter(unittest.TestCase):
    def test_split_nodes_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertIsNotNone(new_nodes)
        self.assertEqual(len(new_nodes), 3)
        
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)

        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_bold(self):
        node = TextNode("This is **text** with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertIsNotNone(new_nodes)
        self.assertEqual(len(new_nodes), 5)
        
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[1].text, "text")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        
        self.assertEqual(new_nodes[2].text, " with a ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        
        self.assertEqual(new_nodes[3].text, "bold")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)

        self.assertEqual(new_nodes[4].text, " word")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)
        
    def test_split_nodes_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        
        self.assertIsNotNone(new_nodes)
        self.assertEqual(len(new_nodes), 3)
        
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)

        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)        
        
class test_return_markdown_images(unittest.TestCase):
    def test_no_matches(self):
        text = ""
        result = return_markdown_images(text)
        
        self.assertEqual(result, [])
        
    def test_no_matches_with_text(self):
        text = "This is text with no images."
        result = return_markdown_images(text)
        
        self.assertEqual(result, [])
        
    def test_one_match(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)."
        result = return_markdown_images(text)
        
        self.assertEqual(result, [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])
        
    def test_multiple_matches(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)."
        result = return_markdown_images(text)
        
        self.assertEqual(result, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
        
class test_return_markdown_links(unittest.TestCase):
    def test_no_matches(self):
        text = ""
        result = return_markdown_links(text)
        
        self.assertEqual(result, [])

    def test_one_match(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)."
        result = return_markdown_links(text)
        
        self.assertEqual(result, [("to boot dev", "https://www.boot.dev")])
        
    def test_multiple_matches(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)."
        result = return_markdown_links(text)
        
        self.assertEqual(result, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
        
class test_split_nodes_images(unittest.TestCase):   
    def test_split_images_none(self):
        node = TextNode(
            "This is text with no image.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no image.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_one(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(".", TextType.TEXT),                
            ],
            new_nodes,
        )

    def test_split_images_oneB(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_multiple(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
                
class test_split_links(unittest.TestCase):   
    def test_split_links_none(self):
    
        node = TextNode(
            "This is text with no link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        
        self.assertListEqual(
            [
                TextNode("This is text with no link", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_one(self):
    
        node = TextNode(
            "This is text with a [link to google](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link to google", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )

    def test_split_links_oneB(self):
    
        node = TextNode(
            "This is text with a [link to google](https://www.google.com).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link to google", TextType.LINK, "https://www.google.com"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):    
        node = TextNode(
            "This is text with a [link to google](https://www.google.com) and another [to alta vista](https://www.altavista.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link to google", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("to alta vista", TextType.LINK, "https://www.altavista.com"),
            ],
            new_nodes,
        )
        
    def test_split_images_website_testcase(self):
        node = TextNode(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is **text** with an _italic_ word and a `code block` and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a [link](https://boot.dev)", TextType.TEXT),                
            ],
            new_nodes,
        )

class test_text_to_textnodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        
        new_nodes = text_to_textnodes(text)
        
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )
        
    def test_text_to_textnodesB(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) and no. 2: This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        
        new_nodes = text_to_textnodes(text)
        
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and no. 2: This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )
        
class test_markdown_to_blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_too_many_newlines(self):
        md = """


This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_markdown_to_blocks_strip_whitespaces(self):
        md = """
    This is **bolded** paragraph   

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items   
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
        
def main():
    suite = unittest.TestSuite()
    suite.addTest(test_split_links("test_split_links_none"))
    suite.addTest(test_split_links("test_split_links_one"))
    suite.addTest(test_split_links("test_split_links_oneB"))
    suite.addTest(test_split_links("test_split_links_multiple"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
    
if __name__ == "__main__":
    main()