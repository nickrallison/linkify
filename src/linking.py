import os
import re

from get_keys import get_keys
from saving import clean

def link(key, key_file, file_tuple, folder, write_folder):
    file_path, start, end = file_tuple
    file_keys = get_keys(folder, [file_path])

    for file_key in file_keys:
        if clean(key) == clean(file_key[0]):
            return
        
    regex_key = r"(?<=[\s\(])"
    for count, word in enumerate(key.split(' ')):
        regex_key = regex_key + repr(word)[1:-1]
        if count == len(key.split(' ')) - 1:
            regex_key = regex_key + r"s?"
        else:
            regex_key = regex_key + r".?"
    regex_key = regex_key + r"(?=[\s,\.\):;])(?!\.md)"

    file_path_read = os.path.join(folder, file_path)
    file_path_write = os.path.join(write_folder, file_path)
    file_str = ""

    with open(file_path_read, "r", encoding="utf8") as f:
        file_str = f.read()

    yaml_pattern = re.compile(r'---[\s\S]*?---', re.IGNORECASE)
    yaml_blocks = re.findall(yaml_pattern, file_str)

    link_pattern = re.compile(r'\[\[[\s\S]*?\]\]', re.IGNORECASE)
    link_blocks = re.findall(link_pattern, file_str)

    yaml_blocks = yaml_blocks + link_blocks

    if file_path == "Church-Turing Thesis.md":
        print(file_str, regex_key)

    for yaml_block in yaml_blocks:
        placeholder = f'<ZZZZ_BLOCK_{yaml_blocks.index(yaml_block)}>'
        file_str = file_str.replace(yaml_block, placeholder)

    pattern = re.compile(regex_key, re.IGNORECASE)
    file_str = re.sub(pattern, r'[['+key_file+r'|\g<0>]]', file_str)

    for yaml_block, placeholder in zip(yaml_blocks, map(lambda i: f'<ZZZZ_BLOCK_{i}>', range(len(yaml_blocks)))):
        file_str = file_str.replace(placeholder, yaml_block)

    with open(file_path_write, "w", encoding="utf8") as f:
        f.write(file_str)

    