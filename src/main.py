import os
import sys

from saving import save, load, clean
from get_keys import get_keys
from linking import link
from cleaning import remove_links
from test import test

args = []
args = sys.argv
# if len(args) > 1:
#     os.chdir(args[1])
run_folder = os.path.abspath(os.path.join("..", "..", "..", "..", "500-Zettelkasten"))

folder = ""
out_folder = ""
if "test" in args:
    folder = "notes"
    out_folder = "notes_out"
    test_folder = "test"
else:    
    folder = run_folder
    out_folder = run_folder
    test_folder = run_folder


string_dict_loc = "assets/string_dict"
file_dict_loc = "assets/file_dict"
saving_max_len = 5




def main():
    remove_links(folder, folder)

    if "clean" in args:
        return
    string_dict, file_dict = save(folder, saving_max_len)
    string_dict, file_dict
    directory_path = os.path.join(folder)
    files = os.listdir(directory_path)
    file_tuples = get_keys(folder, files)
    ordered_tuples = sorted(file_tuples, key=lambda x: len(x[0]), reverse=True)

    files_changed = {}

    for file_tuple in ordered_tuples:
        key, filename = file_tuple
        key = clean(key)
        if key in string_dict:
            for dict_entry in string_dict[key]:
                link(key, filename, dict_entry, folder, out_folder)
    if "test" in args:
        test(test_folder, out_folder)
    print("Linking Successful")

main()
