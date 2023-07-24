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

# regexes_empty = [ r"'",
#             ]

string_dictionary = {}  # string -> file
file_dictionary = {}    # file   -> string

# Notes
# Don't Let Notes Link to themselves
# After Every replacement, the note must be purged from the hashmap, hashing must be redone, and it must be restored 



def repl_ws(m):
    return ' ' * len(m.group())

def repl_nothing(m):
    return ''


def clean(file_str, lowercase=True):
    for regex in regexes_ws:   
        file_str = re.sub(regex, repl_ws, file_str, count=0, flags=0)

    if lowercase:
        return file_str.lower()
    return file_str

def save(folder, max_len, string_dict_loc, file_dict_loc):
    string_dictionary = {}  # string -> file
    file_dictionary = {}    # file   -> string

    directory_path = os.path.join(folder)
    files = sorted(os.listdir(directory_path), key=len, reverse=True)
    for filename in files:
        file_path = os.path.join(folder, filename)
        with open(file_path, "r") as f:
            file_str = clean(f.read())
            word_array = re.split(r"\s+", file_str.strip())
            for length in range(max_len):
                for count, _ in enumerate(word_array):
                    sentence = ""
                    if count > len(word_array) - length - 1:
                        continue
                    for word_inc in range(length + 1):
                        sentence = sentence + word_array[count + word_inc] + " "
                    string_dictionary[sentence.strip()] = (filename, count, count + word_inc)
                    file_dictionary[filename] = sentence.strip()


    str_dict_ser = pickle.dumps(string_dictionary)
    with open(string_dict_loc, 'wb') as f:
        f.write(str_dict_ser)

    file_dict_ser = pickle.dumps(file_dictionary)
    with open(file_dict_loc, 'wb') as f:
        f.write(file_dict_ser)

def load(string_dict_loc, file_dict_loc):
    string_dict = {}
    file_dict = {}
    with open(string_dict_loc, 'rb') as f:
        string_dict = pickle.loads(f.read())
    with open(file_dict_loc, 'rb') as f:
        file_dict = pickle.loads(f.read())
    return string_dict, file_dict