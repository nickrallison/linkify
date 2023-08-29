import os
import sys

from path_manipulate import flatten_files, get_files_as_dict, get_file_titles_and_aliases, add_link, \
    write_string_to_file, get_filename

args = sys.argv
VAULT_DIR = args[1]
save_folders = [os.path.join(VAULT_DIR, "500-Zettelkasten"), os.path.join(VAULT_DIR, "400-PDFs")]  # Files that will have links inserted
link_folders = [os.path.join(VAULT_DIR, "500-Zettelkasten")]  # Files whos aliases / titles are linked against

# save_folders = ["files"]  # Files that will have links inserted
# link_folders = ["files"]  # Files whos aliases / titles are linked against

max_save_len = 2
def main():

    files_to_save = flatten_files(save_folders, VAULT_DIR)  # path from root to allow folders
    files_to_link = flatten_files(link_folders, VAULT_DIR)  # path from root to allow folders

    search_set = get_files_as_dict(files_to_save, max_save_len, VAULT_DIR)
    for link_file_path in files_to_link:
        titles = get_file_titles_and_aliases(link_file_path, VAULT_DIR)
        sorted_titles = sorted(titles, key=lambda x: len(x), reverse=True)
        for title in sorted_titles:
            if title in search_set:
                files_containing_title = search_set[title]
                for file_containing_title in files_containing_title:
                    if not title in get_file_titles_and_aliases(file_containing_title, VAULT_DIR):
                        linked_file = add_link(file_containing_title, title, link_file_path, VAULT_DIR)
                        result_path = os.path.join(VAULT_DIR, file_containing_title)
                        write_string_to_file(linked_file, result_path)
    print("Done Linking")


if __name__ == "__main__":
    main()
