from leafnode import LeafNode
from textnode import TextType, TextNode

CONVERSION_MAP = {
    TextType.TEXT: lambda node: LeafNode(tag=None, value=node.text),
    TextType.BOLD: lambda node: LeafNode(tag="b", value=node.text),
    TextType.ITALIC: lambda node: LeafNode(tag="i", value=node.text),
    TextType.CODE: lambda node: LeafNode(tag="code", value=node.text),
    TextType.LINK: lambda node: LeafNode(
        tag="a", value=node.text, props={"href": node.url}
    ),
    TextType.IMAGE: lambda node: LeafNode(
        tag="img", value="", props={"src": node.url, "alt": node.text}
    ),
}


def text_node_to_html_node(text_node):
    conversion_func = CONVERSION_MAP.get(text_node.text_type)
    if conversion_func:
        return conversion_func(text_node)
    raise ValueError(f"Unknown text type: {text_node.text_type}")
