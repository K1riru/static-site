from textnode import TextNode,TextType
import os
import shutil
import sys
from textnode import markdown_to_html_node, extract_title

def main():
    # basepath is the first CLI arg (e.g. "/my-repo/"), default '/'
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    dest_dir = "docs"

    clear_public_dir(dest_dir)
    copy_dir("static", dest_dir)
    # generate pages for all markdown files in content/ using template.html -> dest_dir
    try:
        generate_pages_recursive("content", "template.html", dest_dir, basepath)
    except Exception as e:
        print(f"Error generating pages: {e}")


def clear_public_dir(dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)


def copy_dir(static, public):
    for item in os.listdir(static):
        src_path = os.path.join(static, item)
        dst_path = os.path.join(public, item)
        if os.path.isfile(src_path):
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)
            print(f"Copied file: {src_path} to {dst_path}")
        elif os.path.isdir(src_path):
            os.makedirs(dst_path, exist_ok=True)
            copy_dir(src_path, dst_path)


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # read markdown
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    # read template
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # convert markdown to html string
    node = markdown_to_html_node(markdown)
    html = node.to_html()

    # extract title
    title = extract_title(markdown)

    # replace placeholders
    output = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    # adjust absolute root links to use the provided basepath
    if basepath is None:
        basepath = "/"
    # ensure basepath ends with a slash
    if not basepath.endswith("/"):
        basepath = basepath + "/"
    output = output.replace('href="/', f'href="{basepath}')
    output = output.replace("src=\"/", f'src="{basepath}')

    # ensure dest directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"Wrote generated page to {dest_path}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    """Recursively crawl `dir_path_content` and generate an HTML page for
    each markdown file found, writing them into `dest_dir_path` preserving
    directory structure. Uses `generate_page` for each file.
    """
    import os

    for root, dirs, files in os.walk(dir_path_content):
        for fname in files:
            if not fname.lower().endswith(".md"):
                continue
            src_path = os.path.join(root, fname)
            # compute relative path from content dir
            rel = os.path.relpath(src_path, dir_path_content)
            # change extension to .html
            rel_html = os.path.splitext(rel)[0] + ".html"
            dest_path = os.path.join(dest_dir_path, rel_html)
            # ensure destination directory exists
            dest_dir = os.path.dirname(dest_path)
            if dest_dir and not os.path.exists(dest_dir):
                os.makedirs(dest_dir, exist_ok=True)
            generate_page(src_path, template_path, dest_path, basepath)



if __name__ == "__main__":
    main()
    