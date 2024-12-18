from enum import Enum
from textnode import TextNode, TextType
import shutil
import os

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

if __name__ == "__main__":
    main()