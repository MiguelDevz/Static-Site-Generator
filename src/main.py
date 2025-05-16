from textnode import TextNode, TextType
import os
import shutil

from copystatic import copy_files_recursively
from page_generator import generate_page


dir_path_static = "./static"
dir_path_public = "./public"

content_index_md = "./content/index.md"
template_html = "./template.html"
public_index_html = "./public/index.html"

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursively(dir_path_static, dir_path_public)
    generate_page(content_index_md, template_html, public_index_html)

if __name__ == "__main__":
    main()