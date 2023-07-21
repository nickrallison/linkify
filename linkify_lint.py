import os
import re
from ast import literal_eval

folder = "/home/nick/VaultNew/500 - Zettelkasten"
# Files to Lint
directory_path = os.path.join(folder)
files = sorted(os.listdir(directory_path), key=len, reverse=True)
files_sanitized = [f.split('.')[0] for f in files]

clean_tuples = []
for count, value in enumerate(files):
    clean_tuples.append((files_sanitized[count], files[count]))


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
                    clean_tuples.append((literal, filename))

clean_tuples = sorted(clean_tuples, key=lambda x: len(x[0]), reverse=True)

# state 0 = clear
# state 1 = ```
# state 2 = $$

for count, filename in enumerate(files):
    print(f"{count + 1} of {len(files)}")
    state = 0
    file_path = os.path.join(folder, filename)
    with open(file_path, 'r', encoding="utf8") as file:
        content = file.read()

    yaml_pattern = re.compile(r'---[\s\S]*?---', re.IGNORECASE)
    yaml_blocks = re.findall(yaml_pattern, content)

    for yaml_block in yaml_blocks:
        placeholder = f'<YAML_BLOCK_{yaml_blocks.index(yaml_block)}>'
        content = content.replace(yaml_block, placeholder)

        lines = content.split("\n")


        for count, line in enumerate(lines):
            if state == 0:
                if line.startswith("$$"):
                    state = 2
                    continue
                if line.startswith("`"):
                    state = 1
                    continue
            if state == 1:
                if line.startswith("`"):
                    state = 0
                    continue
                continue
            if state == 2:
                if line.startswith("$$"):
                    state = 0
                    continue
                continue


            
            for tuple_inst in clean_tuples:
                pattern = re.compile(r'(?<=[\s\(])' + re.escape(tuple_inst[0]) + r's?(?=[\s,\.\):;])(?!\.md)', re.IGNORECASE)
                lines[count] = re.sub(pattern, r'[['+tuple_inst[1]+r'|\g<0>]]', lines[count])
                pattern = re.compile(r'^' + re.escape(tuple_inst[0]) + r's?(?=[\s,\.\):;])(?!\.md)',
                                    re.IGNORECASE)
                lines[count] = re.sub(pattern, r'[[' + tuple_inst[1] + r'|\g<0>]]', lines[count])
                pattern = re.compile(r'(?<=[\s\(])' + re.escape(tuple_inst[0]) + r's?$',
                                    re.IGNORECASE)
                lines[count] = re.sub(pattern, r'[[' + tuple_inst[1] + r'|\g<0>]]', lines[count])
            
            content = "\n".join(lines)

        for yaml_block, placeholder in zip(yaml_blocks, map(lambda i: f'<YAML_BLOCK_{i}>', range(len(yaml_blocks)))):
            content = content.replace(placeholder, yaml_block)


    with open(file_path, 'w', encoding="utf8") as file:
        file.write(content)
