from textnode import TextNode, TextType
from leafnode import LeafNode
import re

def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, value = text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(TextType.BOLD.value, text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(TextType.ITALIC.value, text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(TextType.CODE.value, text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(TextType.LINK.value, text_node.text, {"href": f"{text_node.url}"})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(TextType.IMAGE.value, "", {"src": f"{text_node.url}", "alt": f"{text_node.text}"})
    else:
        raise Exception(f"text_node has unknown type: {text_node}")
    
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:        
            node_new_nodes = node.text.split(delimiter)
            type = TextType.TEXT
            for text_part in node_new_nodes:
                new_node = TextNode(text_part, type)
                new_nodes.append(new_node)
                
                if type == TextType.TEXT:
                    type = text_type
                else:
                    type = TextType.TEXT
    
    return new_nodes

def return_markdown_images(text) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
    return matches

def return_markdown_links(text) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
    mat = re.split
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    all_new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            all_new_nodes.append(node)
        else:
            imgs = return_markdown_images(node.text)
            node_text = node.text
            for img in imgs:
                alt_text = img[0]
                url = img[1]
                splits = node_text.split(f"![{alt_text}]({url})", 1)
                all_new_nodes.append(TextNode(splits[0], TextType.TEXT))
                all_new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                node_text = splits[1]
            if node_text != "":
                all_new_nodes.append(TextNode(node_text, TextType.TEXT))
    
    return all_new_nodes

def split_nodes_link(old_nodes: list[TextNode]):
    all_new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            all_new_nodes.append(node)
        else:
            links = return_markdown_links(node.text)
            node_text = node.text
            for img in links:
                src_text = img[0]
                url = img[1]
                splits = node_text.split(f"[{src_text}]({url})", 1)
                all_new_nodes.append(TextNode(splits[0], TextType.TEXT))
                all_new_nodes.append(TextNode(src_text, TextType.LINK, url))
                node_text = splits[1]
            if node_text != "":
                all_new_nodes.append(TextNode(node_text, TextType.TEXT))
                
    return all_new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    new_blocks = [b.strip() for b in blocks if b != ""]
    return new_blocks