from enum import Enum
import re
from parentnode import ParentNode
from textnode import TextNode, TextType
from textnodeparser import TextNodeParser

class TextBlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

class TextBlockParser():
    CODE_REG_EX = r"^```[^`]*```$"
    HEADER_REG_EX = r"^#{1,6} .*"


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
        if re.match(TextBlockParser.HEADER_REG_EX, block) != None:
            return TextBlockType.HEADING
        elif re.match(TextBlockParser.CODE_REG_EX, block) != None:
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
    
    def get_block_type_html_tag(block_type, header_block):
        match block_type:
            case TextBlockType.QUOTE:
                return "blockquote"
            case TextBlockType.UNORDERED_LIST:
                return "ul"
            case TextBlockType.ORDERED_LIST:
                return "ol"
            case TextBlockType.CODE:
                return "code"
            case TextBlockType.PARAGRAPH:
                return "p"
            case TextBlockType.HEADING:
                return f"h{len(re.match(r"^#{1,6}", header_block)[0])}"
            case _:
                raise Exception("Unrecognised block type")
    
    def get_block_type_text_node(block_type, block):
        match block_type:
            case TextBlockType.QUOTE:
                return block[1:]
            case TextBlockType.UNORDERED_LIST:
                return block[2:]
            case TextBlockType.ORDERED_LIST:
                return block[3:]
            case TextBlockType.CODE:
                return block[3:-3]
            case TextBlockType.PARAGRAPH:
                return block
            case TextBlockType.HEADING:
                num_hashes = len(re.match(r"^#{1,6} ", block)[0])
                return block[num_hashes:]
            case _:
                raise Exception("Unrecognised block type")

    def block_to_children_nodes(block, block_type):
        children_nodes = []
        block = TextBlockParser.get_block_type_text_node(block_type, block)
        children_nodes.extend(TextNodeParser.text_to_textnodes(block))
        children_nodes = list(map(lambda node: node.text_node_to_html_node(), children_nodes))
        return children_nodes

    def block_to_html_node(block):
        block_type = TextBlockParser.block_to_block_type(block)
        block_tag = TextBlockParser.get_block_type_html_tag(block_type, block)
        block_node = ParentNode(block_tag, [])
        if block_type == TextBlockType.UNORDERED_LIST or block_type == TextBlockType.ORDERED_LIST:
            for line in block.split("\n"):
                li_node = ParentNode("li", TextBlockParser.block_to_children_nodes(line, block_type))
                block_node.children.append(li_node)
        elif block_type == TextBlockType.QUOTE:
            for line in block.split("\n"):
                quote_node = TextBlockParser.block_to_children_nodes(line, block_type)
                block_node.children.extend(quote_node)
        elif block_type == TextBlockType.CODE:
            block_node.children = TextBlockParser.block_to_children_nodes(block, block_type)
            block_node = ParentNode("pre", [block_node])
        else:
            block_node.children = TextBlockParser.block_to_children_nodes(block, block_type)
        return block_node
    
    def markdown_to_html_nodes(markdown):
        blocks = TextBlockParser.markdown_to_blocks(markdown)
        div_node = ParentNode("div", [])
        for block in blocks:
            div_node.children.append(TextBlockParser.block_to_html_node(block))
        return div_node