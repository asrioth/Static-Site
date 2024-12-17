import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    
    def test_tohtml(self):
        with self.assertRaises(TypeError):
            node = ParentNode()
        node = ParentNode(None, [])
        with self.assertRaises(ValueError):
            node.to_html()
        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
        node = ParentNode("p", [])
        p_empty_children = "<p></p>"
        self.assertEqual(node.to_html(), p_empty_children)
        node_with_children = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")])
        p_with_children = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node_with_children.to_html(), p_with_children)
        node = ParentNode("body", [node_with_children])
        body_with_parent_child = "<body><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></body>"
        self.assertEqual(node.to_html(), body_with_parent_child)
        node = ParentNode("p", [])
        node = ParentNode("body", [node_with_children, node])
        body_with_child_parent_child = "<body><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p></p></body>"
        self.assertEqual(node.to_html(), body_with_child_parent_child)