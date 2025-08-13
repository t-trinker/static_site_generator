from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
def block_is_quote(mdtext: str) -> bool:
    lines = mdtext.split("\n")
    result = True
    for line in lines:
        result = result and line.startswith(">")
    return result
    
def block_is_unordered_list(mdtext: str) -> bool:
    lines = mdtext.split("\n")
    result = True
    for line in lines:
        result = result and line.startswith("- ")
    return result    

def block_is_ordered_list(mdtext: str) -> bool:
    lines = mdtext.split("\n")
    number = 1
    result = True
    for line in lines:
        result = result and line.startswith(f"{number}. ")
        number += 1
    return result
    
def block_to_blocktype(mdtext: str) -> BlockType:
    if mdtext.startswith(("#", "##", "###", "####", "#####", "######")):
        return BlockType.HEADING
    elif mdtext.startswith("```") and mdtext.endswith("```"):
        return BlockType.CODE
    elif block_is_quote(mdtext):
        return BlockType.QUOTE    
    elif block_is_unordered_list(mdtext):
        return BlockType.UNORDERED_LIST
    elif block_is_ordered_list(mdtext):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH