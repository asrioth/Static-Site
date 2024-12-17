import unittest
from textblockparser import TextBlockParser

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

    def build_test_block(self, blocks, multi_new_line = 2, lead_trail_new_line = 0):
        block_case = "\n" * lead_trail_new_line + blocks.pop(0)
        for block in blocks:
            block_case += "\n" * multi_new_line + block
        block_case += "\n" * lead_trail_new_line
        return block_case