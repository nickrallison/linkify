import os
import re

def remove_links(folder, write_folder):
    directory_path = os.path.join(folder)
    files = os.listdir(directory_path)
    regex = r"\[\[(?:[\s\S]*?\|)??([^\|]*?)\]\]"
    subst = r"\g<1>"
    for filename in files:
        file_path = os.path.join(folder, filename)
        file_str = ""
        with open(file_path, "r", encoding="utf8") as f:
            file_str = re.sub(regex, subst, f.read(), 0, re.MULTILINE | re.IGNORECASE)
        file_path = os.path.join(write_folder, filename)
        with open(file_path, "w", encoding="utf8") as f:
            f.write(file_str)

