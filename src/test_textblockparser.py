import unittest
from textblockparser import TextBlockParser, TextBlockType
from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode

class TestTextBlockParser(unittest.TestCase):
    three_block_test_case = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
    block1 = "# This is a heading"
    block2 = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
    block3 = """* This is the first list item in a list block
* This is a list item
* This is another list item"""
    block4 = "```this is code```"
    block5 = """>This is the first quote item in a quote block
>This is a quote item
>This is another quote item"""
    block6 = """1. This is the first ordered item in a ordered block
2. This is an ordered item
3. This is another ordered item"""


    def test_markdown_to_blocks(self):
        blocks = TextBlockParser.markdown_to_blocks(self.three_block_test_case)
        expected_blocks = [self.block1, self.block2, self.block3]
        self.assertEqual(blocks, expected_blocks)
        blocks = TextBlockParser.markdown_to_blocks(self.block1)
        expected_blocks = [self.block1]
        self.assertEqual(blocks, expected_blocks)
        blocks = TextBlockParser.markdown_to_blocks("")
        expected_blocks = []
        self.assertEqual(blocks, expected_blocks)
        blocks = TextBlockParser.markdown_to_blocks(self.build_test_block([self.block1, self.block2]))
        expected_blocks = [self.block1, self.block2]
        self.assertEqual(blocks, expected_blocks)
        blocks = TextBlockParser.markdown_to_blocks(self.build_test_block([self.block1, self.block2, self.block3], 2))
        expected_blocks = [self.block1, self.block2, self.block3]
        self.assertEqual(blocks, expected_blocks)
        blocks = TextBlockParser.markdown_to_blocks(self.build_test_block([self.block1, self.block2, self.block3], 2, 2))
        expected_blocks = [self.block1, self.block2, self.block3]
        self.assertEqual(blocks, expected_blocks)
        blocks = TextBlockParser.markdown_to_blocks(self.build_test_block([self.block1, self.block2, self.block3], 0, 0))
        expected_blocks = [self.block1 + self.block2 + self.block3]
        self.assertEqual(blocks, expected_blocks)

    def test_block_to_block_type(self):
        block_type = TextBlockParser.block_to_block_type(self.block1)
        expected_block_type = TextBlockType.HEADING
        self.assertEqual(block_type, expected_block_type)
        block_type = TextBlockParser.block_to_block_type(self.block2)
        expected_block_type = TextBlockType.PARAGRAPH
        self.assertEqual(block_type, expected_block_type)
        block_type = TextBlockParser.block_to_block_type(self.block3)
        expected_block_type = TextBlockType.UNORDERED_LIST
        self.assertEqual(block_type, expected_block_type)
        block_type = TextBlockParser.block_to_block_type(self.block4)
        expected_block_type = TextBlockType.CODE
        self.assertEqual(block_type, expected_block_type)
        block_type = TextBlockParser.block_to_block_type(self.block5)
        expected_block_type = TextBlockType.QUOTE
        self.assertEqual(block_type, expected_block_type)
        block_type = TextBlockParser.block_to_block_type(self.block6)
        expected_block_type = TextBlockType.ORDERED_LIST
        self.assertEqual(block_type, expected_block_type)
        block_type = TextBlockParser.block_to_block_type("#####" + self.block1)
        expected_block_type = TextBlockType.HEADING
        self.assertEqual(block_type, expected_block_type)
        block_type = TextBlockParser.block_to_block_type("######" + self.block1)
        expected_block_type = TextBlockType.PARAGRAPH
        self.assertEqual(block_type, expected_block_type)
        block_type = TextBlockParser.block_to_block_type("`" + self.block4)
        expected_block_type = TextBlockType.PARAGRAPH
        self.assertEqual(block_type, expected_block_type)
        block_type = TextBlockParser.block_to_block_type(self.block4 + "`")
        expected_block_type = TextBlockType.PARAGRAPH
        self.assertEqual(block_type, expected_block_type)
        block_type = TextBlockParser.block_to_block_type(self.mess_up_list(self.block3, "2. ", 2))
        expected_block_type = TextBlockType.PARAGRAPH
        self.assertEqual(block_type, expected_block_type)
        block_type = TextBlockParser.block_to_block_type(self.mess_up_list(self.block5, "* ", 1))
        expected_block_type = TextBlockType.PARAGRAPH
        self.assertEqual(block_type, expected_block_type)
        block_type = TextBlockParser.block_to_block_type(self.mess_up_list(self.block6, ">", 3))
        expected_block_type = TextBlockType.PARAGRAPH
        self.assertEqual(block_type, expected_block_type)
        block_type = TextBlockParser.block_to_block_type(self.mess_up_list(self.block6, "1. ", 3))
        expected_block_type = TextBlockType.PARAGRAPH
        self.assertEqual(block_type, expected_block_type)
        block_type = TextBlockParser.block_to_block_type(self.mess_up_list(self.block6, "", 3))
        expected_block_type = TextBlockType.PARAGRAPH
        self.assertEqual(block_type, expected_block_type)

    def test_get_block_type_html_tag(self):
        block_tag = TextBlockParser.get_block_type_html_tag(TextBlockType.CODE, "")
        expected_block_tag = "code"
        self.assertEqual(block_tag, expected_block_tag)
        block_tag = TextBlockParser.get_block_type_html_tag(TextBlockType.HEADING, "# ")
        expected_block_tag = "h1"
        self.assertEqual(block_tag, expected_block_tag)
        block_tag = TextBlockParser.get_block_type_html_tag(TextBlockType.HEADING, "###### ")
        expected_block_tag = "h6"
        self.assertEqual(block_tag, expected_block_tag)
        block_tag = TextBlockParser.get_block_type_html_tag(TextBlockType.ORDERED_LIST, "")
        expected_block_tag = "ol"
        self.assertEqual(block_tag, expected_block_tag)
        block_tag = TextBlockParser.get_block_type_html_tag(TextBlockType.PARAGRAPH, "")
        expected_block_tag = "p"
        self.assertEqual(block_tag, expected_block_tag)
        block_tag = TextBlockParser.get_block_type_html_tag(TextBlockType.QUOTE, "")
        expected_block_tag = "blockquote"
        self.assertEqual(block_tag, expected_block_tag)
        block_tag = TextBlockParser.get_block_type_html_tag(TextBlockType.UNORDERED_LIST, "")
        expected_block_tag = "ul"
        self.assertEqual(block_tag, expected_block_tag)
        with self.assertRaises(Exception):
            block_tag = TextBlockParser.get_block_type_html_tag("", "")
    
    def test_get_block_type_text_node(self):
        block = TextBlockParser.get_block_type_text_node(TextBlockType.CODE, "```a```")
        expected_block = "a"
        self.assertEqual(block, expected_block)
        block = TextBlockParser.get_block_type_text_node(TextBlockType.HEADING, "# a")
        self.assertEqual(block, expected_block)
        block = TextBlockParser.get_block_type_text_node(TextBlockType.HEADING, "###### a")
        self.assertEqual(block, expected_block)
        block = TextBlockParser.get_block_type_text_node(TextBlockType.ORDERED_LIST, "1. a")
        self.assertEqual(block, expected_block)
        block = TextBlockParser.get_block_type_text_node(TextBlockType.PARAGRAPH, "a")
        self.assertEqual(block, expected_block)
        block = TextBlockParser.get_block_type_text_node(TextBlockType.QUOTE, ">a")
        self.assertEqual(block, expected_block)
        block = TextBlockParser.get_block_type_text_node(TextBlockType.UNORDERED_LIST, "* a")
        self.assertEqual(block, expected_block)
        
    def test_block_to_children_nodes(self):
        children = TextBlockParser.block_to_children_nodes(self.block4, TextBlockType.CODE)
        expected_children = [LeafNode(None, self.block4[3:-3])]
        self.assertEqual(children, expected_children)
        children = TextBlockParser.block_to_children_nodes(self.block1, TextBlockType.HEADING)
        expected_children = [LeafNode(None, self.block1[2:])]
        self.assertEqual(children, expected_children)
        children = TextBlockParser.block_to_children_nodes("#####" + self.block1, TextBlockType.HEADING)
        expected_children = [LeafNode(None, self.block1[2:])]
        self.assertEqual(children, expected_children)
        children = TextBlockParser.block_to_children_nodes(self.block6.split("\n")[0], TextBlockType.ORDERED_LIST)
        expected_children = [LeafNode(None, self.block6.split("\n")[0][3:])]
        self.assertEqual(children, expected_children)
        children = TextBlockParser.block_to_children_nodes(self.block2, TextBlockType.PARAGRAPH)
        block2_part1, block2_part2, block2_part3, block2_part4, block2_part5 = "This is a paragraph of text. It has some ", "bold", " and ", "italic", " words inside of it."
        expected_children = [LeafNode(None, block2_part1), LeafNode("b", block2_part2), LeafNode(None, block2_part3), LeafNode("i", block2_part4), LeafNode(None, block2_part5)]
        self.assertEqual(children, expected_children)
        children = TextBlockParser.block_to_children_nodes(self.block5.split("\n")[0], TextBlockType.QUOTE)
        expected_children = [LeafNode(None, self.block5.split("\n")[0][1:])]
        self.assertEqual(children, expected_children)
        children = TextBlockParser.block_to_children_nodes(self.block3.split("\n")[0], TextBlockType.UNORDERED_LIST)
        expected_children = [LeafNode(None, self.block3.split("\n")[0][2:])]
        self.assertEqual(children, expected_children)

    def test_block_to_html_node(self):
        parent_node = TextBlockParser.block_to_html_node(self.block1)
        expected_parent_node = ParentNode("h1", [LeafNode(None, self.block1[2:])])
        self.assertEqual(repr(parent_node), repr(expected_parent_node))
        parent_node = TextBlockParser.block_to_html_node(self.block2)
        block2_part1, block2_part2, block2_part3, block2_part4, block2_part5 = "This is a paragraph of text. It has some ", "bold", " and ", "italic", " words inside of it."
        expected_parent_node = ParentNode("p", [LeafNode(None, block2_part1), LeafNode("b", block2_part2), LeafNode(None, block2_part3), LeafNode("i", block2_part4), LeafNode(None, block2_part5)])
        self.assertEqual(repr(parent_node), repr(expected_parent_node))
        parent_node = TextBlockParser.block_to_html_node(self.block3)
        line1, line2, line3 = self.block3.split("\n")
        expected_parent_node = ParentNode("ul", [ParentNode("li", [LeafNode(None, line1[2:])]), ParentNode("li", [LeafNode(None, line2[2:])]), ParentNode("li", [LeafNode(None, line3[2:])])])
        self.assertEqual(repr(parent_node), repr(expected_parent_node))
        parent_node = TextBlockParser.block_to_html_node(self.block4)
        expected_parent_node = ParentNode("pre", [ParentNode("code", [LeafNode(None, self.block4[3:-3])])])
        self.assertEqual(repr(parent_node), repr(expected_parent_node))
        parent_node = TextBlockParser.block_to_html_node(self.block5)
        line1, line2, line3 = self.block5.split("\n")
        expected_parent_node = ParentNode("blockquote", [LeafNode(None, line1[1:]), LeafNode(None, line2[1:]), LeafNode(None, line3[1:])])
        self.assertEqual(repr(parent_node), repr(expected_parent_node))
        parent_node = TextBlockParser.block_to_html_node(self.block6)
        line1, line2, line3 = self.block6.split("\n")
        expected_parent_node = ParentNode("ol", [ParentNode("li", [LeafNode(None, line1[3:])]), ParentNode("li", [LeafNode(None, line2[3:])]), ParentNode("li", [LeafNode(None, line3[3:])])])
        self.assertEqual(repr(parent_node), repr(expected_parent_node))

    def test_markdown_to_html_nodes(self):
        markdown = self.build_test_block([self.block1, self.block2, self.block3, self.block4, self.block5, self.block6])
        div_node = TextBlockParser.markdown_to_html_nodes(markdown)
        expected_div_node = self.build_full_html_structure()
        self.assertEqual(div_node, expected_div_node)
    
    def build_full_html_structure(self):
        div_node = ParentNode("div", [])
        block1_node = ParentNode("h1", [LeafNode(None, self.block1[2:])])
        block2_part1, block2_part2, block2_part3, block2_part4, block2_part5 = "This is a paragraph of text. It has some ", "bold", " and ", "italic", " words inside of it."
        block2_node = ParentNode("p", [LeafNode(None, block2_part1), LeafNode("b", block2_part2), LeafNode(None, block2_part3), LeafNode("i", block2_part4), LeafNode(None, block2_part5)])
        line1, line2, line3 = self.block3.split("\n")
        block3_node = ParentNode("ul", [ParentNode("li", [LeafNode(None, line1[2:])]), ParentNode("li", [LeafNode(None, line2[2:])]), ParentNode("li", [LeafNode(None, line3[2:])])])
        block4_node = ParentNode("pre", [ParentNode("code", [LeafNode(None, self.block4[3:-3])])])
        line1, line2, line3 = self.block5.split("\n")
        block5_node = ParentNode("blockquote", [LeafNode(None, line1[1:]), LeafNode(None, line2[1:]), LeafNode(None, line3[1:])])
        line1, line2, line3 = self.block6.split("\n")
        block6_node = ParentNode("ol", [ParentNode("li", [LeafNode(None, line1[3:])]), ParentNode("li", [LeafNode(None, line2[3:])]), ParentNode("li", [LeafNode(None, line3[3:])])])
        div_node.children.extend([block1_node, block2_node, block3_node, block4_node, block5_node, block6_node])
        return div_node

    def mess_up_list(self, block, replacement, start, line_to_change = 1):
        lines = block.split("\n")
        lines[line_to_change] = replacement + lines[line_to_change][start:]
        return "\n".join(lines)

    def build_test_block(self, blocks, multi_new_line = 2, lead_trail_new_line = 0):
        block_case = "\n" * lead_trail_new_line + blocks.pop(0)
        for block in blocks:
            block_case += "\n" * multi_new_line + block
        block_case += "\n" * lead_trail_new_line
        return block_case