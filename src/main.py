from textnode import TextNode, TextType

def main():
    print(TextNode("This is some anchor text", TextType.LINK, "https://www.example.com"))

if __name__ == "__main__":
    main()