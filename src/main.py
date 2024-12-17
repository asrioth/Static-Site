from enum import Enum
from textnode import TextNode

class FakeNum(Enum):
    FAKE = "fake"

def main():
    textnode = TextNode("hi", FakeNum.FAKE, "here.com")
    textnode2 = TextNode("hi", FakeNum.FAKE, "here.com")
    print (textnode)
    print (textnode == textnode2)

main()