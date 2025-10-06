import os
from utils.generate_page import generate_page


def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):

    for f in os.listdir(dir_path_content):
        relative_path = os.path.join(dir_path_content, f)
        relative_content_path = os.path.join(dest_dir_path, f)

        if not os.path.isfile(relative_path):
            if not os.path.exists(relative_content_path):
                os.mkdir(relative_content_path)
            generate_pages_recursive(
                basepath,
                template_path=template_path,
                dest_dir_path=relative_content_path,
                dir_path_content=relative_path,
            )
            continue
        if not relative_path.endswith(".md"):
            raise Exception("the file is not of .md")

        generate_page(
            basepath,
            relative_path,
            template_path,
            relative_content_path.replace(".md", ".html"),
        )
