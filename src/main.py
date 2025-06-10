import shutil
import os

from main_functions import cp_dir, generate_page, generate_pages_recursive

static_dir_path = "./static"
content_dir_path = "./content"
template_path = "./template.html"
destination_dir_path = "./public"

shutil.rmtree(destination_dir_path)
cp_dir(static_dir_path, destination_dir_path)

generate_pages_recursive(content_dir_path, template_path, destination_dir_path)