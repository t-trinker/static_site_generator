from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "a"
    IMAGE = "img"

class TextNode():
    def __init__(self, text:str, text_type:TextType, url = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            raise NotImplementedError
        
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self) -> str:
        return(f"TextNode('{self.text}', TYPE: {self.text_type.value}, URL: {self.url})")