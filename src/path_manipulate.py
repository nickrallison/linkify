import os
from re import Match

from string_manipulate import clean_string, get_regex_capture, replace_regex_capture, replace_with_previous_chars

important_regex = [
    r"```[\s\S]*?```",
    r"`[\s\S]*?`",
    r"---[\s\S]*?---",
    r"\$\$[\s\S]*?\$\$",
    r"\$[\s\S]*?\$",
    r"\[\[[\s\S]*?\]\]",
    r"#+\s+.*\n",
    r"\[.*?\]\(.*?\)",
]

link_regex_with_path = r'\[\[.*?\|(.*?)\]\]'
link_regex_without_path = r'\[\[(.*?)\]\]'

count = 0
saved = {}


def flatten_files(root_folders: [str], vault_root: str) -> [str]:
    files = []
    for root_folder in root_folders:
        for walk_root, _, walk_files in os.walk(root_folder):
            for file in walk_files:
                files.append(os.path.relpath(os.path.join(walk_root, file), vault_root))
    return files

def get_files_as_dict(files_to_save: [str], max_save_len: int, vault_root: str) -> dict:
    file_dict = {}
    for file_to_save in files_to_save:
        file_to_save_abs = os.path.join(vault_root, file_to_save)
        filename, file_extension = os.path.splitext(file_to_save_abs)
        if file_extension == ".md":
            with open(file_to_save_abs, "r", encoding="utf-8") as f:
                clean_file = clean_string(f.read())
            clean_file_array = clean_file.split(" ")
            for save_len in range(0, max_save_len):
                for index in range(len(clean_file_array) - save_len + 1):
                    key = " ".join(clean_file_array[index:index+save_len+1])
                    if not key in file_dict:
                        file_dict[key] = []
                    if not file_to_save in file_dict[key]:
                        file_dict[key].append(file_to_save)
    return file_dict


def get_file_titles_and_aliases(link_file_path: str, vault_root: str) -> [str]:
    titles = []
    abs_link_file_path = os.path.join(vault_root, link_file_path)
    with open(abs_link_file_path, "r", encoding="utf-8") as f:
        link_file_string = f.read()
    link_file_name = get_filename(abs_link_file_path)
    titles.append(clean_string(link_file_name).strip())
    frontmatter_regex = r'---[\s\S]*?aliases: \[?(.*?)\]?\n[\s\S]*?---'
    aliases = [clean_string(x) for x in get_regex_capture([frontmatter_regex], link_file_string)]
    keys = titles + aliases
    return [x for x in keys if x.strip() != ""]



def add_link(file_containing_title: str, key: str, key_file: str, vault_root: str) -> str:
    global saved, count
    file_containing_title_abs = os.path.join(vault_root, file_containing_title)
    file_string = get_file_as_str(os.path.join(file_containing_title_abs))
    #unlinked_string = unlink_file(file_string)
    important_parts_cleaned_string = replace_regex_capture(important_regex, file_string, save_important_func)
    linked_string = replace_with_previous_chars(important_parts_cleaned_string, key, f"\\1[[{get_filename(os.path.join(vault_root, key_file))}.md|\\2]]\\3")
    returned_saved_string = replace_saved_regex(linked_string)
    saved = {}
    count = 0
    return returned_saved_string



def get_filename(abs_link_file_path: str, extension=False) -> str:
    filename, file_extension = os.path.splitext(os.path.basename(abs_link_file_path))
    if extension:
        return filename + file_extension
    return filename

def get_file_as_str(abs_link_file_path: str) -> str:
    with open(abs_link_file_path, "r", encoding="utf-8") as f:
        return f.read()


def write_string_to_file(file_str: str, abs_link_file_path: str) -> None:
    with open(abs_link_file_path, "w", encoding="utf-8") as f:
        f.write(file_str)
    return None

def save_important_func(string_to_save: Match) -> str:
    global count, saved
    result = f"<SAVED_VALUE_{str(count)}>"
    count = count + 1
    saved[result] = string_to_save.group(0)
    return result

def unlink_file(string_to_unlink: str) -> str:
    # temp = replace_regex_capture([link_regex_with_path], string_to_unlink, r'\1')
    # return replace_regex_capture([link_regex_without_path], temp, r'\1')
    return replace_regex_capture([link_regex_with_path], string_to_unlink, r'\1')

def replace_saved_regex(linked_string: str) -> str:
    working_string = linked_string
    for key in saved:
        working_string = working_string.replace(key, saved[key])
    return working_string