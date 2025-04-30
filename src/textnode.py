from enum import Enum

class TextType(Enum):
    normal_text = "Normal text"
    bold_text = "**Bold text**"
    italic_text = "_Italic text_"
    code_text = "`Code text`"
    link = "[anchor text](url)"
    images = "![alt text](url)"

class TextNode():
    def __init__(self, text:str, text_type:TextType, url):
        self.text = text
        self.text_type = text_type
        self.url = url if text_type in {TextType.link, TextType.images} else None

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type == other .text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"