import shutil
import sys

from main_functions import cp_dir, generate_page, generate_pages_recursive

if len(sys.argv) == 2:
    basepath = sys.argv[1]
else:
    basepath = "/"

static_dir_path = "./static"
content_dir_path = "./content"
template_path = "./template.html"
destination_dir_path = "./docs"

shutil.rmtree(destination_dir_path)
cp_dir(static_dir_path, destination_dir_path)

generate_pages_recursive(content_dir_path, template_path, destination_dir_path, basepath)