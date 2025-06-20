import os
import shutil
import re

from blocks_functions import markdown_to_html_node

def cp_dir(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        if os.path.isfile(src_path):
            print(f"cp {src_path} to {dst}")
            shutil.copy(src_path, dst)
        else:
            cp_dir(os.path.join(src, item), os.path.join(dst, item))

def extract_title(markdown):
    title = re.findall(r"^# (.+)", markdown, re.MULTILINE)
    if len(title) == 0:
        raise ValueError("No title")
    return title[0].strip()

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    if not os.path.exists(os.path.split(dest_path)[0]):
        os.makedirs(os.path.split(dest_path)[0])
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(content_dir_path, template_path, destination_dir_path, basepath):
    if not os.path.exists(destination_dir_path):
        os.mkdir(destination_dir_path)

    for item in os.listdir(content_dir_path):
        src_path = os.path.join(content_dir_path, item)
        if os.path.isfile(src_path):
            _, file = os.path.split(src_path)
            _, extension = os.path.splitext(file)
            if extension == ".md":
                generate_page(src_path, template_path, os.path.join(destination_dir_path, "index.html"), basepath)
        else:
            generate_pages_recursive(src_path, template_path, os.path.join(destination_dir_path, item), basepath)