from static_to_public import static_to_public
from utils.generate_page_recursive import generate_pages_recursive
import os
import sys


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    docs_dir = os.path.join(repo_root, "docs")
    static_dir = os.path.join(repo_root, "static")
    content_dir = os.path.join(repo_root, "content")
    template_path = os.path.join(repo_root, "template.html")

    static_to_public(public_path=docs_dir, static_path=static_dir)
    generate_pages_recursive(basepath, content_dir, template_path, docs_dir)


if __name__ == "__main__":
    main()
