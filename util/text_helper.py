import re

def delete_all(pattern: str, s: str):
    for match in re.finditer(pattern, s):
        s = s.replace(match.group(0), "")

    return s

def pre_process_text(s: str):
    s = delete_all(r"\[.+\]", s)
    s = delete_all(r"\(http.+\)", s)

    return s
    