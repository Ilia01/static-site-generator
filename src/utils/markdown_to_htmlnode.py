from utils.markdown_to_blocks import markdown_to_blocks
from utils.block_to_block_type import block_to_block_type
from blocktype import BlockType
from utils.text_textnodes import text_to_textnodes
from parentnode import ParentNode
from leafnode import LeafNode
from utils.node_to_html import text_node_to_html_node
import re


def markdown_to_html_node(markdown):
    """
    Converts a full markdown document into a single parent HTMLNode,
    using helper functions for each block type.
    """
    blocks = markdown_to_blocks(markdown)
    child_nodes = []

    block_handlers = {
        BlockType.PARAGRAPH: _paragraph_to_html,
        BlockType.HEADING: _heading_to_html,
        BlockType.CODE: _code_to_html,
        BlockType.QUOTE: _quote_to_html,
        BlockType.UNORDERED_LIST: _unordered_list_to_html,
        BlockType.ORDERED_LIST: _ordered_list_to_html,
    }

    for block in blocks:
        block_type = block_to_block_type(block)
        handler = block_handlers.get(block_type)
        if handler:
            child_nodes.append(handler(block))

    return ParentNode("div", child_nodes)


def _paragraph_to_html(block):
    block = block.strip().replace("\n", " ")
    block = re.sub(r"\s+", " ", block)
    text_nodes = text_to_textnodes(block)
    html_children = [text_node_to_html_node(node) for node in text_nodes]
    return ParentNode("p", html_children)


def _heading_to_html(block):
    num_hashes = 0
    for char in block:
        if char == "#":
            num_hashes += 1
        else:
            break
    text = block[num_hashes:].lstrip()
    text_nodes = text_to_textnodes(text)
    html_children = [text_node_to_html_node(node) for node in text_nodes]
    return ParentNode(f"h{num_hashes}", html_children)


def _code_to_html(block):
    text = block.strip("`")
    if text.startswith("\n"):
        text = text[1:]
    if text.endswith("\n"):
        text = text[:-1]

    children = [LeafNode(tag=None, value=text)]
    return ParentNode("pre", [ParentNode("code", children)])


def _quote_to_html(block):
    lines = [line[1:].strip() for line in block.split("\n")]
    text = "\n".join(lines)
    text_nodes = text_to_textnodes(text)
    html_children = [text_node_to_html_node(node) for node in text_nodes]
    return ParentNode("blockquote", html_children)


def _unordered_list_to_html(block):
    lines = block.split("\n")
    list_children = []
    for line in lines:
        if line.startswith("- "):
            item_text = line[2:].strip()
        elif line.startswith("* "):
            item_text = line[2:].strip()
        else:
            item_text = line.strip()

        html_children = [
            text_node_to_html_node(node) for node in text_to_textnodes(item_text)
        ]
        list_children.append(ParentNode("li", html_children))

    return ParentNode("ul", list_children)


def _ordered_list_to_html(block):
    items = []
    for line in block.split("\n"):
        p = line.find(".")
        if p != -1:
            item = line[p + 1 :].lstrip()
        else:
            item = line.lstrip()

        html_children = [text_node_to_html_node(n) for n in text_to_textnodes(item)]
        items.append(ParentNode("li", html_children))
    return ParentNode("ol", items)
