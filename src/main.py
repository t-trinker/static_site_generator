from mardown_blocks import markdown_to_blocks, markdown_to_html_node
from htmlnode import HTMLNode

from os import path, listdir, mkdir, makedirs
from shutil import copy, rmtree

def delete(destdir: str) -> None:
    if not path.exists(destdir):
        return
    
    rmtree(destdir)
    
def copy_files(sourcedir: str, destdir: str) -> None:
    if not path.exists(sourcedir):
        return
    
    if not path.exists(destdir):
        mkdir(destdir)
      
    entries = listdir(sourcedir)  
    for entry in entries:
        abssource = path.join(sourcedir, entry)
        if path.isfile(abssource):
            print(f"copying {abssource} -> {path.join(destdir, entry)}")
            copy(abssource, destdir)
        else:
            absdestdir = path.join(destdir, entry)
            mkdir(absdestdir)
            copy_files(abssource, absdestdir)       
        
def extract_title(markdown: str):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:]
    raise Exception("no title found")
    
def generate_page(from_path: str , template_path: str , dest_path: str):
    if not path.isfile(from_path):
        return
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")
    
    with open(from_path, "r") as md:
        mdfile = md.read()
        
    with open(template_path, "r") as tmpl:
        templatefile = tmpl.read()

    htmlnode: HTMLNode = markdown_to_html_node(mdfile)
    content = htmlnode.to_html()
    
    title = extract_title(mdfile)
    
    full_html = templatefile.replace("{{ Title }}", title).replace("{{ Content }}", content)
    
    if not path.exists(path.dirname(dest_path)):
        makedirs(path.dirname(dest_path))
    
    with open(dest_path, "w") as dest:
        dest.write(full_html)
        

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    content_entries = listdir(dir_path_content)
    for entry in content_entries:
        abssource = path.join(dir_path_content, entry)
        if path.isfile(abssource):
            new_dest_dir = path.join(dest_dir_path, entry.replace(".md", ".html"))
            generate_page(abssource, template_path, new_dest_dir)
        else:
            absdestdir = path.join(dest_dir_path, entry)
            if not path.exists(absdestdir):
                mkdir(absdestdir)
            generate_pages_recursive(abssource, template_path, absdestdir)
            

def main():
    delete("public")
    copy_files("static", "public")
    generate_pages_recursive("content", "template.html", "public")    

if __name__ == "__main__":
    main()