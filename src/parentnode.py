from htmlnode import HTMLNode, TagState

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent nodes must have a tag")
        if self.children == None:
            raise ValueError("Parent nodes must have children")
        node_html = self.tag_wrap()
        for child in self.children:
            node_html += child.to_html()
        node_html += self.tag_wrap(TagState.END)
        return node_html