import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    test_prop_one = {
    "href": "https://www.google.com", 
    "target": "_blank",
}

    def test_prop_to_html(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
        node = HTMLNode(props = {})
        self.assertEqual(node.props_to_html(), "")
        node = HTMLNode(props= self.test_prop_one)
        test_prop_one_repr = "href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), test_prop_one_repr)
    
    def test_repr(self):
        tag, value, children, props = "Hi", "there", "I", "work"
        node = HTMLNode(tag, value, children, props)
        test_repr_one = f"HTMLNode({tag},{value},{children},{props})"
        self.assertEqual(repr(node), test_repr_one)
        node = HTMLNode()
        test_repr_two = f"HTMLNode({None},{None},{None},{None})"
        self.assertEqual(repr(node), test_repr_two)