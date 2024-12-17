from enum import Enum
import re

class TextBlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

class TextBlockParser():

    def markdown_to_blocks(markdown):
        lines = markdown.split('\n')
        blocks = []
        block = ""
        for line in lines:
            if line == "" and block == "":
                continue
            elif line == "" and block != "":
                blocks.append(block.strip())
                block = ""
            elif block != "":
                block += "\n" + line
            else:
                block = line
        if block != "":
            blocks.append(block)
        return blocks
    
    def block_to_block_type(block):
        if re.match(r"^#{1,6} .*", block) != None:
            return TextBlockType.HEADING
        elif re.match(r"^```[^`]*```$", block) != None:
            return TextBlockType.CODE
        else:
            lines = block.split("\n")
            quote_match, unordered_match, ordered_match = False, False, False
            order_count = 1
            for line in lines:
                if line[0] == ">":
                    quote_match = True
                elif line[:2] == "* " or line[0] == "- ":
                    unordered_match = True
                elif line[:3] == str(order_count) + ". ":
                    order_count += 1
                    ordered_match = True
                else:
                    return TextBlockType.PARAGRAPH
            if quote_match and not unordered_match and not ordered_match:
                return TextBlockType.QUOTE
            elif unordered_match and not quote_match and not ordered_match:
                return TextBlockType.UNORDERED_LIST
            elif ordered_match and not unordered_match and not quote_match:
                return TextBlockType.ORDERED_LIST
            return TextBlockType.PARAGRAPH
                