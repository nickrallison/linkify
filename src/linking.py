import os
import re

from get_keys import get_keys
from saving import clean

def link(key, key_file, file_tuple, folder, write_folder):
    file_path, start, end = file_tuple
    # if file_path.find("400-PDFs") != -1:
    filename_temp = os.path.basename(file_path)
    
    try:
        file_keys = get_keys(os.path.abspath(os.path.join(os.path.dirname(file_path))), [filename_temp])
    except:
        print(f"Bad File: {filename_temp}")
        return

    for file_key in file_keys:
        if clean(key) == clean(file_key[0]):
            return
        
    regex_key = r"([\s\(])("
    for count, word in enumerate(key.split(' ')):
        regex_key = regex_key + repr("['|’]?".join(word))[1:-1] + r"['|’]?"
        if count == len(key.split(' ')) - 1:
            regex_key = regex_key + r"s?"
        else:
            regex_key = regex_key + r".?"
    regex_key = regex_key + r")([,\):;\s]|(?:\.(?:(?:[^m][^d])|\s)))"
    
    file_path_read = os.path.join(folder, file_path)
    file_path_write = os.path.join(write_folder, file_path)
    file_str = ""


    with open(file_path_read, "r", encoding="utf8") as f:
        file_str = f.read()

    yaml_pattern = re.compile(r'---[\s\S]*?---', re.IGNORECASE)
    yaml_blocks = re.findall(yaml_pattern, file_str)

    link_pattern = re.compile(r'\[\[[\s\S]*?\]\]', re.IGNORECASE)
    link_blocks = re.findall(link_pattern, file_str)

    latex_pattern = re.compile(r'\$\$[\s\S]*?\$\$', re.IGNORECASE)
    latex_blocks = re.findall(latex_pattern, file_str)

    blocks = yaml_blocks + link_blocks + latex_blocks

    for block in blocks:
        placeholder = f'<ZZZZ_BLOCK_{blocks.index(block)}>'
        file_str = file_str.replace(block, placeholder)

    pattern = re.compile(regex_key, re.IGNORECASE)
    matches = pattern.findall(file_str)
    for match in matches:
        file_str = pattern.sub(r'\1[[' + key_file + r'|\2]]\3', file_str, count=1)

    for block, placeholder in zip(blocks, map(lambda i: f'<ZZZZ_BLOCK_{i}>', range(len(blocks)))):
        file_str = file_str.replace(placeholder, block)

    with open(file_path_write, "w", encoding="utf8") as f:
        f.write(file_str)

    