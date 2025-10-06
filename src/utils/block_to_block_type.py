from blocktype import BlockType


def block_to_block_type(markdown_block):
    """
    Determines the BlockType of a markdown block by calling helper functions.
    The order of checks is important for correct precedence.
    """
    if is_heading(markdown_block):
        return BlockType.HEADING
    if is_code_block(markdown_block):
        return BlockType.CODE
    if is_quote(markdown_block):
        return BlockType.QUOTE
    if is_unordered_list(markdown_block):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(markdown_block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def is_heading(block):
    """
    Checks if a block is a heading.
    Headings start with 1-6 '#' characters, followed by a space.
    """
    if not block.startswith("#"):
        return False
    num_hashes = 0
    for char in block:
        if char == "#":
            num_hashes += 1
        else:
            break
    return 1 <= num_hashes <= 6 and block[num_hashes] == " "


def is_code_block(block):
    """
    Checks if a block is a code block.
    Code blocks must start and end with three backticks.
    """
    return block.startswith("```") and block.endswith("```")


def is_quote(block):
    """
    Checks if a block is a quote block.
    Every line must start with a '>' character.
    """
    lines = block.split("\n")
    for line in lines:
        if not line.startswith(">"):
            return False
    return True


def is_unordered_list(block):
    """
    Checks if a block is an unordered list.
    Every line must start with a '-' followed by a space.
    """
    lines = block.split("\n")
    for line in lines:
        s = line.lstrip()
        if not (s.startswith("- ") or s.startswith("* ")):
            return False
    return True


def is_ordered_list(block):
    """
    Checks if a block is an ordered list.
    Every line must start with a number followed by '. '
    and the number must increment sequentially from 1.
    """
    lines = block.split("\n")
    i = 1
    for line in lines:
        s = line.lstrip()
        if not s.startswith(f"{i}. "):
            return False
        i += 1
    return True
