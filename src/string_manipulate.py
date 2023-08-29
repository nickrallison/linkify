import re

def clean_string(dirty_string: str) -> str:
    lower_dirty_string = dirty_string.lower()
    no_fm_string = remove_frontmatter(lower_dirty_string)
    no_headers_string = remove_headers(no_fm_string)
    no_new_line = re.sub('\s+', ' ', no_headers_string)
    return re.sub('[^0-9a-zA-Z ]+', '', no_new_line).strip()

def remove_frontmatter(dirty_string: str) -> str:
    return re.sub('^\s*---[\s\S]*---\s*', '', dirty_string)

def remove_headers(dirty_string: str) -> str:
    return re.sub('#+\s+.*\n', '', dirty_string)


def get_regex_capture(regex_patterns: [str], search_string: str) -> [str]:
    matches_total = []
    for regex_pattern in regex_patterns:
        matches = re.search(regex_pattern, search_string)
        if matches != None:
            matches_total = matches_total + [x for x in matches.groups()]
    return matches_total


def replace_regex_capture(regex_patterns: [str], search_string: str, replace) -> str:
    operating_string = search_string
    for index, regex_pattern in enumerate(regex_patterns):
        operating_string = re.sub(regex_pattern, replace, operating_string, re.MULTILINE)
    return operating_string


def replace_with_previous_chars(text: str, search_words_str: str, replacement: str):
    search_words = search_words_str.split(" ")
    search_patterns = [re.escape(word) for word in search_words]
    pattern = r'(\W*)(' + r'[\W_]*'.join(search_patterns) + r"'?s?)(\W*)"
    print(pattern)
    result = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return result