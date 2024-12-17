from enum import Enum
from textnode import TextNode, TextType

def main():
    textnode = TextNode("hi", TextType.BOLD, "here.com")
    textnode2 = TextNode("hi", TextType.BOLD, "here.com")
    print(textnode)
    print(textnode == textnode2)

    print("a\na\nb\n b".split('\n'))

if __name__ == "__main__":
    main()