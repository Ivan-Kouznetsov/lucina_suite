#!/usr/bin/env python3
from typing_extensions import Final

import re
from typing import List, Any
import sys
import json
from types import SimpleNamespace
from model.post import Post
from model.context_example import ContextExample
from service.text_analysis import get_collocations
import config
from colorama import Fore, Back, Style

# Helper functions


def is_match(regex: str, s: str):
    is_in_url = False
    match:Any = re.search(regex, s, re.IGNORECASE) # :Any is a workaround for mypy bug
    if (match != None):
        url_match:Any = re.search("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", s)
        if (url_match!=None):
            is_in_url = match.group(0) in url_match.group(0)

    return match!=None and not is_in_url


def hightlight(regex: str, s: str, colour=Back.GREEN):
    for match in re.finditer(regex, s, re.IGNORECASE):
        s = s.replace(match.group(0), colour + match.group(0) + Style.RESET_ALL)

    return s


def create_example(regex: str, text: str, desc: str, url: str, score: int):
    return ContextExample(hightlight(regex, text),
                          Style.BRIGHT + desc + Style.RESET_ALL,
                          Fore.BLUE + "https://www.reddit.com" + url + Style.RESET_ALL,
                          Fore.GREEN + str(score) + Style.RESET_ALL)

# /Helper functions


if (len(sys.argv) != 3):
    print("Usage: python3 reddit_context.py posts_file.json string")
    exit(1)

file_name: Final = sys.argv[1]
pattern: Final = r"\b" + sys.argv[2].replace(" ", ".{1," + str(config.MAX_MIDDLE_CHARS) + "}") + r"\b"

examples: List[ContextExample] = []

try:
    with open(file_name, "r") as posts_file:
        posts: Final[list] = json.loads(posts_file.read(), object_hook=lambda d: SimpleNamespace(**d))

        for post in posts:
            if (is_match(pattern, post.title)):
                examples.append(create_example(pattern, post.title, "Post", post.permalink, post.score))
            if (is_match(pattern, post.text)):
                examples.append(create_example(pattern, post.text, "Post",  post.permalink, post.score))
            for comment in post.comments:
                if (is_match(pattern, comment.text)):
                    examples.append(create_example(pattern, comment.text, "Comment", comment.permalink, comment.score))

        for example in examples:
            print(example)

except IOError as err:
    print("Could not read {} because {}".format(file_name, str(err)))
    exit(1)
