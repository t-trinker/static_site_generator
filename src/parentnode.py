from htmlnode import HtmlNode
from leafnode import LeafNode

class ParentNode(HtmlNode):
    def __init__(
        self, 
        tag: str, 
        children: list[HtmlNode], 
        props: dict[str, str] | None = None
    ) -> None:
        
        super().__init__(tag, children=children, props=props)
        
    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNodes require a tag")
        
        if not self.children:
            raise ValueError("ParentNodes require at least one child")
        
        result = f"<{self.tag}>"
        
        if self.children:
            for child in self.children:
                child_html = child.to_html()
                if child_html:
                    result += child_html
                
        result += f"</{self.tag}>"
        
        return result