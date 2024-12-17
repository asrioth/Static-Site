import unittest
from textnode import TextNode, TextType
from textnodeparser import TextNodeParser

class TestTextNodeParser(unittest.TestCase):
    image_text = "This is text with a image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    link_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    
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

    def test_extract_markdown_images(self):
        images = TextNodeParser.extract_markdown_images(self.image_text)
        expected_images = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(images, expected_images)
        images = TextNodeParser.extract_markdown_images("test")
        expected_images = []
        self.assertEqual(images, expected_images)
        images = TextNodeParser.extract_markdown_images(self.link_text)
        expected_images = []
        self.assertEqual(images, expected_images)

    def test_extract_markdown_links(self):
        links = TextNodeParser.extract_markdown_links(self.link_text)
        expected_links = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(links, expected_links)
        links = TextNodeParser.extract_markdown_links("test")
        expected_links = []
        self.assertEqual(links, expected_links)
        links = TextNodeParser.extract_markdown_links(self.image_text)
        expected_links = []
        self.assertEqual(links, expected_links)

    def test_split_nodes_image(self):
        image_nodes = TextNodeParser.split_nodes_image([TextNode(self.image_text, TextType.TEXT)])
        expected_nodes = [
            TextNode("This is text with a image ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertEqual(image_nodes, expected_nodes)
        image_nodes = TextNodeParser.split_nodes_image([TextNode(self.image_text, TextType.TEXT), TextNode(self.image_text, TextType.TEXT)])
        expected_nodes = [
            TextNode("This is text with a image ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        expected_nodes += expected_nodes
        self.assertEqual(image_nodes, expected_nodes)
        image_nodes = TextNodeParser.split_nodes_image([TextNode("test", TextType.TEXT)])
        expected_nodes = [TextNode("test", TextType.TEXT)]
        self.assertEqual(image_nodes, expected_nodes)
        image_nodes = TextNodeParser.split_nodes_image([TextNode(self.link_text, TextType.TEXT)])
        expected_nodes = [TextNode(self.link_text, TextType.TEXT)]
        self.assertEqual(image_nodes, expected_nodes)
        image_nodes = TextNodeParser.split_nodes_image([TextNode(self.image_text, TextType.IMAGE)])
        expected_nodes = [TextNode(self.image_text, TextType.IMAGE)]
        self.assertEqual(image_nodes, expected_nodes)
        image_nodes = TextNodeParser.split_nodes_image([TextNode(self.link_text, TextType.TEXT), TextNode(self.link_text, TextType.TEXT)])
        expected_nodes = [TextNode(self.link_text, TextType.TEXT), TextNode(self.link_text, TextType.TEXT)]
        self.assertEqual(image_nodes, expected_nodes)

    def test_split_nodes_link(self):
        image_nodes = TextNodeParser.split_nodes_link([TextNode(self.link_text, TextType.TEXT)])
        expected_nodes = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(image_nodes, expected_nodes)
        image_nodes = TextNodeParser.split_nodes_link([TextNode(self.link_text, TextType.TEXT), TextNode(self.link_text, TextType.TEXT)])
        expected_nodes = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
        ]
        expected_nodes += expected_nodes
        self.assertEqual(image_nodes, expected_nodes)
        image_nodes = TextNodeParser.split_nodes_link([TextNode("test", TextType.TEXT)])
        expected_nodes = [TextNode("test", TextType.TEXT)]
        self.assertEqual(image_nodes, expected_nodes)
        image_nodes = TextNodeParser.split_nodes_link([TextNode(self.image_text, TextType.TEXT)])
        expected_nodes = [TextNode(self.image_text, TextType.TEXT)]
        self.assertEqual(image_nodes, expected_nodes)
        image_nodes = TextNodeParser.split_nodes_link([TextNode(self.link_text, TextType.IMAGE)])
        expected_nodes = [TextNode(self.link_text, TextType.IMAGE)]
        self.assertEqual(image_nodes, expected_nodes)
        image_nodes = TextNodeParser.split_nodes_link([TextNode(self.image_text, TextType.TEXT), TextNode(self.image_text, TextType.TEXT)])
        expected_nodes = [TextNode(self.image_text, TextType.TEXT), TextNode(self.image_text, TextType.TEXT)]
        self.assertEqual(image_nodes, expected_nodes)


    
    def get_expected_nodes(self, text_node):
        return [
            TextNode("This is text with a ", TextType.TEXT),
            text_node,
            TextNode(" word", TextType.TEXT)
        ]
    
    def get_text_node_text(self, to_parse):
        return f"This is text with a {to_parse} word"