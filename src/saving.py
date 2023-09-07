import os
import re
import pickle

regexes_ws = [ r"---[\s\S]*?---", 
            r"\$\$[\s\S]*?\$\$", 
            r"\$[\s\S]*?\$",
            r"```[\s\S]*?```", 
            r"`[\s\S]*?`", 
            r"\[\[[\s\S]*?\]\]", 
            r"\[[\s\S]*?\]",
            r"#+",
            r",",
            r"\.",
            r"\)",
            r"\(",
            r"-",
            ]

regexes_empty = [ r"['|’]",
            r"\*",
            ]

string_dictionary = {}  # string -> file
file_dictionary = {}    # file   -> string

def find_files(folder_path, vault_root):
    file_paths = []
    for root, _, files in os.walk(os.path.join(vault_root, folder_path)):
        for file in files:
            file_paths.append(os.path.join(root, file))
    
    return file_paths


def repl_ws(m):
    return ' ' * len(m.group())

def repl_nothing(m):
    return ''


def clean(file_str, lowercase=True):
    for regex in regexes_ws:   
        file_str = re.sub(regex, repl_ws, file_str, count=0, flags=0)
    for regex in regexes_empty:   
        file_str = re.sub(regex, "", file_str, count=0, flags=0)
    if lowercase:
        return file_str.lower()
    return file_str

def save(folders, max_len, vault_root):
    string_dictionary = {}  # string -> file
    file_dictionary = {}    # file   -> string

    directory_path = folders
    files = []
    for folder in folders:
        files_new = find_files(folder, vault_root)
        files = files + files_new
    files = sorted(files, key=len, reverse=True)

    files = [x for x in files if x.endswith(".md")]

    test_files = [os.path.basename(x) for x in files]

    for file_path in files:
        filename = os.path.basename(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                file_str = clean(f.read())
            except:
                pass
            word_array = re.split(r"\s+", file_str.strip())
            for length in range(max_len):
                for count, _ in enumerate(word_array):
                    sentence = ""
                    if count > len(word_array) - length - 1:
                        continue
                    for word_inc in range(length + 1):
                        sentence = sentence + word_array[count + word_inc] + " "
                    if sentence.strip() not in string_dictionary:
                        string_dictionary[sentence.strip()] = []
                    if sentence.strip() + "s" not in string_dictionary:
                        string_dictionary[sentence.strip()+"s"] = []
                    string_dictionary[sentence.strip()].append((file_path, count, count + word_inc))
                    string_dictionary[sentence.strip()+"s"].append((file_path, count, count + word_inc))
                    #file_dictionary[filename] = sentence.strip()
    return string_dictionary, file_dictionary

    # str_dict_ser = pickle.dumps(string_dictionary)
    # with open(string_dict_loc, 'wb') as f:
    #     f.write(str_dict_ser)

    # file_dict_ser = pickle.dumps(file_dictionary)
    # with open(file_dict_loc, 'wb') as f:
    #     f.write(file_dict_ser)

def load(string_dict_loc, file_dict_loc):
    string_dict = {}
    file_dict = {}
    with open(string_dict_loc, 'rb') as f:
        string_dict = pickle.loads(f.read())
    with open(file_dict_loc, 'rb') as f:
        file_dict = pickle.loads(f.read())
    return string_dict, file_dict