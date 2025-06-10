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
            if not os.path.exists(dst):
                os.mkdir(dst)
            print(f"cp {src_path} to {dst}")
            shutil.copy(src_path, dst)
        else:
            cp_dir(os.path.join(src, item), os.path.join(dst, item))

def extract_title(markdown):
    title = re.findall(r"^# (.+)", markdown, re.MULTILINE)
    if len(title) == 0:
        raise ValueError("No title")
    return title[0].strip()

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    if not os.path.exists(os.path.split(dest_path)[0]):
        os.makedirs(os.path.split(dest_path)[0])
    with open(dest_path, "w") as f:
        f.write(template)