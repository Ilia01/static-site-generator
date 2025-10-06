from textnode import TextType, TextNode
from .extract_markdown import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)

        # If we don't have paired delimiters, leave the node unchanged for robustness
        if len(split_text) % 2 == 0:
            new_nodes.append(node)
            continue

        for i, word in enumerate(split_text):
            if i % 2 == 0:
                if word:
                    new_nodes.append(TextNode(word, TextType.TEXT))
            else:
                new_nodes.append(TextNode(word, text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:

        image_attributes = extract_markdown_images(node.text)

        if len(image_attributes) == 0:
            new_nodes.append(node)
            continue

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        remainder = node.text

        for alt, link in image_attributes:
            left, right = remainder.split(f"![{alt}]({link})", 1)

            if left:
                new_nodes.append(TextNode(left, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, link))

            remainder = right

        if remainder:
            new_nodes.append(TextNode(remainder, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:

        link_attributes = extract_markdown_links(node.text)

        if len(link_attributes) == 0:
            new_nodes.append(node)
            continue

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        remainder = node.text

        for text, link in link_attributes:
            left, right = remainder.split(f"[{text}]({link})", 1)

            if left:
                new_nodes.append(TextNode(left, TextType.TEXT))

            new_nodes.append(TextNode(text, TextType.LINK, link))

            remainder = right

        if remainder:
            new_nodes.append(TextNode(remainder, TextType.TEXT))

    return new_nodes
