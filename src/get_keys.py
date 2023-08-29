
import os
import re
from ast import literal_eval

def get_keys(folder, file_list):
    directory_path = os.path.join(folder)
    files = sorted(file_list, key=len, reverse=True)
    files_sanitized = [f.split('.')[0] for f in files]
    keys = []
    for count, value in enumerate(files):
        keys.append((files_sanitized[count], value))
    for filename in files:
        file_path = os.path.join(folder, filename)
        with open(file_path, 'r', encoding="utf8") as file:
            content = file.read()
            alias_pattern = re.compile(r'---[\s\S]*?aliases: (?P<aliases>\[[\s\S]*?\])[\s\S]*?---', re.IGNORECASE)
            alias_blocks = re.findall(alias_pattern, content)
            array_pattern = r'(?<=\[).+?(?=\])'  # Regex pattern to match the array inside []
            for alias_block in alias_blocks:
                array_matches = re.findall(array_pattern, alias_block, re.DOTALL)
                if array_matches:
                    array_values = array_matches[0].split(', ')  # Splitting the matched string by comma and space
                    quoted_values = [f'"{val.strip()}"' if not val.startswith('"') else val for val in array_values]  # Adding quotes if necessary
                    updated_string = re.sub(array_pattern, ', '.join(quoted_values), alias_block, re.DOTALL)  # Replacing the old array with the new one
                    for literal in literal_eval(updated_string):
                        keys.append((literal, filename))
                        keys.append((literal + "s", filename))
    return keys

