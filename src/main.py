import shutil

from main_functions import cp_dir, generate_page

source_path = "./content/index.md"
destination_path = "./public/index.html"
template_path = "./template.html"
static_path = "./static"

shutil.rmtree("./public")
cp_dir("./static", "./public")

generate_page("./content/index.md", "./template.html", "./public/index.html")