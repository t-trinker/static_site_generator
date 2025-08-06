class HtmlNode():
    def __init__(
            self, 
            tag: str | None = None, 
            value: str | None = None, 
            children: list['HtmlNode'] | None = None, 
            props: dict[str, str] | None = None
        ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"HtmlNode ({self.tag=}, {self.value=}, {self.children=}, {self.props=})"

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""

        result = ""
        for prop, value in self.props.items():
            result += f' {prop}="{value}"'
        return result