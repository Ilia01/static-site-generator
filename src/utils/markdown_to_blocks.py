def markdown_to_blocks(markdown):
    if not markdown:
        return []

    markdown = markdown.strip()
    text_lines = markdown.split("\n\n")
    new_blocks = []

    for line in text_lines:
        line = line.strip()

        if not line:
            continue

        new_blocks.append(line.strip())

    return new_blocks
