import unittest
from textnode import TextNode, TextType
from leafnode import LeafNode

class TestTextNode(unittest.TestCase):
    test_text_one = "This is a text node"
    test_text_two = "This is not a text node"
    test_url = "https://www.google.com"

    test_prop_one = {
    "href": test_url
}
    test_prop_two = {
    "src": test_url,
    "alt": test_text_two
}
    
    def test_eq(self):    
        node = TextNode(self.test_text_one, TextType.BOLD)
        node2 = TextNode(self.test_text_one, TextType.BOLD)
        self.assertEqual(node, node2)
        node2 = TextNode(self.test_text_one, TextType.BOLD, None)
        self.assertEqual(node, node2)
        node2 = TextNode(self.test_text_two, TextType.BOLD)
        self.assertNotEqual(node, node2)
        node2 = TextNode(self.test_text_one, TextType.TEXT)
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node = TextNode(self.test_text_one, TextType.BOLD)
        test_one_repr = f"TextNode({self.test_text_one}, {TextType.BOLD.value[0]}, None)"
        self.assertEqual(repr(node), test_one_repr)
        node = TextNode(self.test_text_two, TextType.TEXT, self.test_url)
        test_two_repr = f"TextNode({self.test_text_two}, {TextType.TEXT.value[0]}, {self.test_url})"
        self.assertEqual(repr(node), test_two_repr)

    def test_text_nod_to_html_node(self):
        node = TextNode(self.test_text_one, TextType.TEXT)
        leaf = LeafNode(None, self.test_text_one)
        self.assertEqual(node.text_node_to_html_node().to_html(), leaf.to_html())
        node = TextNode(self.test_text_two, TextType.BOLD)
        leaf = LeafNode("b", self.test_text_two)
        self.assertEqual(node.text_node_to_html_node().to_html(), leaf.to_html())
        node = TextNode(self.test_text_one, TextType.ITALIC)
        leaf = LeafNode("i", self.test_text_one)
        self.assertEqual(node.text_node_to_html_node().to_html(), leaf.to_html())
        node = TextNode(self.test_text_two, TextType.CODE)
        leaf = LeafNode("code", self.test_text_two)
        self.assertEqual(node.text_node_to_html_node().to_html(), leaf.to_html())
        node = TextNode(self.test_text_one, TextType.LINK, self.test_url)
        leaf = LeafNode("a", self.test_text_one, self.test_prop_one)
        self.assertEqual(node.text_node_to_html_node().to_html(), leaf.to_html())
        node = TextNode(self.test_text_two, TextType.IMAGE, self.test_url)
        leaf = LeafNode("img", "", self.test_prop_two)
        self.assertEqual(node.text_node_to_html_node().to_html(), leaf.to_html())

if __name__ == "__main__":
    unittest.main()