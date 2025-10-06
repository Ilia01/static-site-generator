from utils.split_nodes import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
from textnode import TextNode, TextType


def text_to_textnodes(text):
    nodes = [TextNode(text=text, text_type=TextType.TEXT)]

    # Protect code spans first so inner content isn't parsed as links/images/formatting
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    return nodes
