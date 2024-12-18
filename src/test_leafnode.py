import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):

    def test_tohtml(self):
        with self.assertRaises(TypeError):
            node = LeafNode()
        para_tag = "p"
        para_text = "This is a paragraph of text."
        node = LeafNode(para_tag, para_text)
        node_html = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node.to_html(), node_html)
        href_tag = "a"
        href_text = "Click me!"
        href_prop = {"href": "https://www.google.com"}
        node = LeafNode(href_tag, href_text, href_prop)
        node_html = "<a href=\"https://www.google.com\">Click me!</a>"
        self.assertEqual(node.to_html(), node_html)
        node = LeafNode(None, para_text)
        self.assertEqual(node.to_html(), para_text)