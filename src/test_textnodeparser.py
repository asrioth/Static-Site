import unittest
from textnode import TextNode, TextType
from textnodeparser import TextNodeParser

class TestTextNodeParser(unittest.TestCase):
    def test_split_node_delimiter(self):
        node = TextNode(self.get_text_node_text("`code block`"), TextType.TEXT)
        new_nodes = TextNodeParser.split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = self.get_expected_nodes(TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes, expected_nodes)
        node = TextNode(self.get_text_node_text("**bold block**"), TextType.TEXT)
        new_nodes = TextNodeParser.split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = self.get_expected_nodes(TextNode("bold block", TextType.BOLD))
        self.assertEqual(new_nodes, expected_nodes)
        node = TextNode(self.get_text_node_text("*italics block*"), TextType.TEXT)
        new_nodes = TextNodeParser.split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected_nodes = self.get_expected_nodes(TextNode("italics block", TextType.ITALIC))
        self.assertEqual(new_nodes, expected_nodes)
        node = TextNode(self.get_text_node_text("`code block`")*2, TextType.TEXT)
        new_nodes = TextNodeParser.split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = self.get_expected_nodes(TextNode("code block", TextType.CODE))
        expected_nodes.pop()
        expected_nodes += [TextNode(" wordThis is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes, expected_nodes)
        node = TextNode("nothing special", TextType.TEXT)
        new_nodes = TextNodeParser.split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [node]
        self.assertEqual(new_nodes, expected_nodes)
        node = TextNode("nothing special", TextType.CODE)
        new_nodes = TextNodeParser.split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [node]
        self.assertEqual(new_nodes, expected_nodes)
        node = TextNode("not quite right**", TextType.CODE)
        with self.assertRaises(Exception):
            new_nodes = TextNodeParser.split_nodes_delimiter([node], "**")
        node1 = TextNode(self.get_text_node_text("`code block`"), TextType.TEXT)
        node2 = TextNode(self.get_text_node_text("`code block`"), TextType.TEXT)
        new_nodes = TextNodeParser.split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        expected_nodes = self.get_expected_nodes(TextNode("code block", TextType.CODE))
        expected_nodes.extend(expected_nodes)
        self.assertEqual(new_nodes, expected_nodes)
    
    def get_expected_nodes(self, text_node):
        return [
            TextNode("This is text with a ", TextType.TEXT),
            text_node,
            TextNode(" word", TextType.TEXT)
        ]
    
    def get_text_node_text(self, to_parse):
        return f"This is text with a {to_parse} word"