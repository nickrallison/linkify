import os
import sys

from path_manipulate import flatten_files, get_files_as_dict, get_file_titles_and_aliases, add_link, \
    write_string_to_file, get_filename, unlink_file, get_file_as_str

args = sys.argv
VAULT_DIR = args[1]
save_folders = [os.path.join(VAULT_DIR, "500-Zettelkasten")]  # Files that will have links inserted
link_folders = [os.path.join(VAULT_DIR, "500-Zettelkasten")]  # Files whos aliases / titles are linked against

# save_folders = ["files"]  # Files that will have links inserted
# link_folders = ["files"]  # Files whos aliases / titles are linked against

max_save_len = 2
def main():

    files_to_save = flatten_files(save_folders, VAULT_DIR)  # path from root to allow folders
    for file in files_to_save:
        if file.endswith(".md"):

            abs_path = os.path.join(VAULT_DIR, file)
            file_string = get_file_as_str(abs_path)
            unlinked = unlink_file(file_string)
            write_string_to_file(unlinked, abs_path)

if __name__ == "__main__":
    main()
