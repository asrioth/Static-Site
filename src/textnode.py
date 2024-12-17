from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    NORMAL = "normal",
    BOLD = "bold",
    ITALIC = "italic",
    CODE = "code",
    LINK = "link",
    IMAGE = "image",
    TEXT = "text"

class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, textNode):
        return self.text == textNode.text and self.text_type == textNode.text_type and self.url == textNode.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value[0]}, {self.url})"

    def url_to_prop(self, prop_name):
        return {prop_name : self.url}
    
    def text_to_prop(self, prop_name):
        return {prop_name : self.text}

    def text_node_to_html_node(self):
        html_node = None
        match self.text_type:
            case TextType.NORMAL:
                html_node = LeafNode(None, self.text)
            case TextType.BOLD:
                html_node = LeafNode("b", self.text)
            case TextType.ITALIC:
                html_node = LeafNode("i", self.text)
            case TextType.CODE:
                html_node = LeafNode("code", self.text)
            case TextType.LINK:
                html_node = LeafNode("a", self.text, self.url_to_prop("href"))
            case TextType.IMAGE:
                props = self.url_to_prop("src")
                props.update(self.text_to_prop("alt"))
                html_node = LeafNode("img", "", props)
        return html_node
