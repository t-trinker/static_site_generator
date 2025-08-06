from htmlnode import HtmlNode

class LeafNode(HtmlNode):
    def __init__(
            self, 
            tag: str | None, 
            value: str, 
            props: dict[str, str] | None = None
        ) -> None:

        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNodes must have a value")
        
        if not self.tag:
            return self.value
        
        html = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

        return html