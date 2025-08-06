from textnode import TextNode, TextType

def main():
    node = TextNode('Text des Nodes', TextType.BOLD, 'www.google.com')
    print(node)

if __name__ == "__main__":
    main()