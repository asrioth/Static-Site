import unittest
from textblockparser import TextBlockParser, TextBlockType

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