from textnode import TextNode, TextType
import re

class TextNodeParser():

    def split_nodes_delimiter(old_nodes, delimiter, text_type):
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type == TextType.TEXT:
                split_text = old_node.text.split(delimiter)
                if len(split_text) > 1 and len(split_text) % 2 != 0: 
                    for i in range(len(split_text)):
                        if i % 2 == 0:
                            if split_text[i] != "":
                                new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                        else:
                            new_nodes.append(TextNode(split_text[i], text_type))
                elif len(split_text) > 1 and len(split_text) % 2 == 0:
                    raise Exception("Invalid markdown, unclosed special charachter")
                else:
                    new_nodes.append(old_node)
            else:
                new_nodes.append(old_node)
        return new_nodes
    
    def extract_markdown_images(text):
        matches = re.findall(r"!\[[^\[\]]*\]\([^\(\)]*\)", text)
        pieces = list(map(lambda match: match.split("]"), matches))
        images = []
        for piece in pieces:
            images.append((piece[0][2:], piece[1][1:-1]))
        return images
    
    def extract_markdown_links(text):
        matches = re.findall(r"(?<!!)\[[^\[\]]*\]\([^\(\)]*\)", text)
        pieces = list(map(lambda match: match.split("]"), matches))
        links = []
        for piece in pieces:
            links.append((piece[0][1:], piece[1][1:-1]))
        return links
    
    def split_nodes_image(old_nodes):
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type == TextType.TEXT:
                node_text = old_node.text
                images = TextNodeParser.extract_markdown_images(node_text)
                for image in images:
                    part1, part2 = node_text.split(f"![{image[0]}]({image[1]})", 1)
                    new_nodes.append(TextNode(part1, TextType.TEXT))
                    new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    node_text = part2
                if node_text != "":
                    new_nodes.append(TextNode(node_text, TextType.TEXT))
            else:
                new_nodes.append(old_node)
        return new_nodes
    
    def split_nodes_link(old_nodes):
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type == TextType.TEXT:
                node_text = old_node.text
                links = TextNodeParser.extract_markdown_links(node_text)
                for link in links:
                    part1, part2 = node_text.split(f"[{link[0]}]({link[1]})", 1)
                    if part1 != "":
                        new_nodes.append(TextNode(part1, TextType.TEXT))
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    node_text = part2
                if node_text != "":
                    new_nodes.append(TextNode(node_text, TextType.TEXT))
            else:
                new_nodes.append(old_node)
        return new_nodes
    
    def text_to_textnodes(text):
        node_list = [TextNode(text.strip(), TextType.TEXT)]
        node_list = TextNodeParser.split_nodes_image(node_list)
        node_list = TextNodeParser.split_nodes_link(node_list)
        node_list = TextNodeParser.split_nodes_delimiter(node_list, "**", TextType.BOLD)
        node_list = TextNodeParser.split_nodes_delimiter(node_list, "*", TextType.ITALIC)
        node_list = TextNodeParser.split_nodes_delimiter(node_list, "`", TextType.CODE)
        return node_list