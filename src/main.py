from enum import Enum
from textnode import TextNode, TextType
import shutil
import os
import re
from textblockparser import TextBlockParser

def extract_title(markdown):
        for line in markdown.split("\n"):
            if re.match(r"^# ", line):
                return line[1:].strip()
        raise Exception("no h1 header '# ...")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as markdown_file:
        markdown = markdown_file.read()
    with open(template_path) as template_file:
        template = template_file.read()
    html_string = TextBlockParser.markdown_to_html_nodes(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    with open(dest_path, 'x') as index:
        index.write(template)
    
def copy_folder_to_public(folder_path):
    contents = os.listdir(folder_path)
    for content in contents:
        file_path = f"{folder_path}{content}"
        if os.path.isfile(file_path):
            shutil.copy(file_path, f"public{file_path[6:]}")
        else:
            os.mkdir(f"public{file_path[6:]}")
            copy_folder_to_public(file_path + "/")

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    copy_folder_to_public("static/")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()