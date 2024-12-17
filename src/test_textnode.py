import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    test_text_one = "This is a text node"
    test_text_two = "This is not a text node"
    test_url = "test.url"
    
    def test_eq(self):    
        node = TextNode(self.test_text_one, TextType.BOLD)
        node2 = TextNode(self.test_text_one, TextType.BOLD)
        self.assertEqual(node, node2)
        node2 = TextNode(self.test_text_one, TextType.BOLD, None)
        self.assertEqual(node, node2)
        node2 = TextNode(self.test_text_two, TextType.BOLD)
        self.assertNotEqual(node, node2)
        node2 = TextNode(self.test_text_one, TextType.NORMAL)
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node = TextNode(self.test_text_one, TextType.BOLD)
        test_one_repr = f"TextNode({self.test_text_one}, {TextType.BOLD.value[0]}, None)"
        self.assertEqual(repr(node), test_one_repr)
        node = TextNode(self.test_text_two, TextType.NORMAL, self.test_url)
        test_two_repr = f"TextNode({self.test_text_two}, {TextType.NORMAL.value[0]}, {self.test_url})"
        self.assertEqual(repr(node), test_two_repr)

        

if __name__ == "__main__":
    unittest.main()