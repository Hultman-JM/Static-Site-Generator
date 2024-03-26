import os
import shutil

from copystatic import copy_files_recursive
from markdown_blocks import markdown_to_html_node


dir_path_static = "./static"
dir_path_public = "./public"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    generate_page("./content/index.md", "template.html", "./public/index.html")

def extract_title(markdown):
    lines = markdown.split("\n")
    is_header = False
    for line in lines:
        if line.startswith("#"):
            is_header = True
            return line
    if is_header == False:
        raise Exception("no h1 header in this markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as file:
        markdown_contents = file.read()
    with open(template_path, 'r') as file:
        template_contents = file.read()

    title = extract_title(markdown_contents)
    converted_html_content = markdown_to_html_node(markdown_contents).to_html()

    print("Debugging - Final HTML content:")
    print(template_contents)


    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", converted_html_content)

    print("Debugging - Final HTML content:")
    print(template_contents)

    with open(dest_path, 'w') as file:
        file.write(template_contents)


main()