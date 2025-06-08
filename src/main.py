from main_functions import cp_dir, generate_page

cp_dir("./static", "./public")

generate_page("./content/index.md", "./template.html", "./public/index.html")