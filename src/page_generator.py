import os
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("#").strip()
    raise Exception("No h1 header found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        md_file = f.read()
    with open(template_path, "r") as f:
        template_file = f.read()
    html = markdown_to_html_node(md_file).to_html()
    title = extract_title(md_file)
    full_html_page = template_file.replace("{{ Title }}", title).replace("{{ Content }}", html)
    directory_to_create = os.path.dirname(dest_path)
    if directory_to_create:
        os.makedirs(directory_to_create, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(full_html_page)