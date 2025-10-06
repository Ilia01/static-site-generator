from utils.markdown_to_htmlnode import markdown_to_html_node
from utils.extract_title import extract_title
import os


def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating a page from {from_path} to {dest_path} using {template_path} ")

    markdown = None
    template = None

    with open(from_path, "r") as m:
        markdown = m.read()

    with open(template_path, "r") as t:
        template = t.read()

    # Remove YAML frontmatter from the rendered content, but still allow title extraction
    def _strip_frontmatter(md: str) -> str:
        lines = md.split("\n")
        if lines and lines[0].strip() == "---":
            # find the next '---' line and drop everything up to and including it
            for i, line in enumerate(lines[1:], start=1):
                if line.strip() == "---":
                    return "\n".join(lines[i + 1 :])
        return md

    content_md = _strip_frontmatter(markdown)

    md_to_html = markdown_to_html_node(content_md).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", md_to_html)

    template.replace("href=/", f"href={basepath}")
    template.replace("src=/", f"src={basepath}")

    with open(dest_path, "w") as d:
        d.write(template)
