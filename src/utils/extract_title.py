def extract_title(markdown):
    """
    Extract a title from markdown supporting two strategies, in order:
    1) YAML frontmatter: a block delimited by lines with '---' at the top.
       If present, a 'title:' key inside the block is used.
    2) The first ATX heading level-1 line that starts with '# '.

    Raises an Exception if no title can be found.
    """
    lines = markdown.split("\n")

    title_from_frontmatter = None
    if lines and lines[0].strip() == "---":
        for line in lines[1:]:
            if line.strip() == "---":
                break
            if line.lower().startswith("title:"):
                value = line.split(":", 1)[1].strip().strip('"').strip("'")
                title_from_frontmatter = value
        if title_from_frontmatter:
            return title_from_frontmatter

    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("There's no header in markdown")
