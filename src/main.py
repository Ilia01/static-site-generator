from textnode import TextNode, TextType


def main():
    node_image = TextNode(
        text="Alt text for an image",
        url="/path/to/my-image.jpg",
        text_type=TextType.IMAGE,
    )

    print(repr(node_image))


if __name__ == "__main__":
    main()
