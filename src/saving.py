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

def save(folder, max_len):
    string_dictionary = {}  # string -> file
    file_dictionary = {}    # file   -> string

    directory_path = os.path.join(folder)
    files = sorted(os.listdir(directory_path), key=len, reverse=True)
    for filename in files:
        file_path = os.path.join(folder, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            #print(file_path)
            file_str = clean(f.read())
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
                    string_dictionary[sentence.strip()].append((filename, count, count + word_inc))
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