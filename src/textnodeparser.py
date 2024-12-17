from textnode import TextNode, TextType

class TextNodeParser():

    def split_nodes_delimiter(old_nodes, delimiter, text_type):
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type == TextType.TEXT:
                split_text = old_node.text.split(delimiter)
                if len(split_text) > 1 and len(split_text) % 2 != 0: 
                    for i in range(len(split_text)):
                        if i % 2 == 0:
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