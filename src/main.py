from textnode import TextNode,TextType
import os
import shutil

def main():
    clear_public_dir()
    copy_dir("static","public")


def clear_public_dir():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
def copy_dir(static,public):
    for item in os.listdir(static):
        src_path = os.path.join(static,item)
        dst_path = os.path.join(public,item)
        if os.path.isfile(src_path):
            shutil.copy2(src_path,dst_path)
            print(f"Copied file: {src_path} to {dst_path}")
        elif os.path.isdir(src_path):
            os.makedirs(dst_path, exist_ok=True)
            copy_dir(src_path, dst_path)



if __name__ == "__main__":
    main()
    