import os

from saving import save, load, clean
from get_keys import get_keys
from linking import link
from cleaning import remove_links

# Notes
# Don't Let Notes Link to themselves
# After Every replacement, the note must be purged from the hashmap, hashing must be redone, and it must be restored 

folder = "notes"
test_folder = "notes_out"
string_dict_loc = "assets/string_dict"
file_dict_loc = "assets/file_dict"
saving_max_len = 5

def main():
    remove_links(folder, test_folder)

    save(folder, saving_max_len, string_dict_loc, file_dict_loc)
    string_dict, file_dict = load(string_dict_loc, file_dict_loc)
    directory_path = os.path.join(folder)
    files = os.listdir(directory_path)

    file_tuples = get_keys(folder, files)
    ordered_tuples = sorted(file_tuples, key=lambda x: len(x[0]), reverse=True)

    for file_tuple in ordered_tuples:
        key, filename = file_tuple
        key = clean(key)
        if key in string_dict:
            link(key, filename, string_dict[key], folder, test_folder)


main()