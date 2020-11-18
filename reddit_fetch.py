#!/usr/bin/env python3
from typing_extensions import Final

import service.reddit_reader as reddit_reader
import jsons
from datetime import date
import sys
from enum import Enum
from util.filename_helper import get_unique_filename
import config

class Mode(Enum):
    Search = 1
    Sub = 2


date_format: Final = "%d-%m-%Y"

# validation and reading of arguments
if (len(sys.argv) != 3):
    print("Usage: python3 reddit_fetch.py -search keyword")
    print("Usage: python3 reddit_fetch.py -sub subreddit_name")
    exit(1)

keyword: Final = sys.argv[2]

if (sys.argv[1] == "-search"):
    mode = Mode.Search
elif (sys.argv[1] == "-sub"):
    mode = Mode.Sub
else:
    print("First argument must be -search or -sub")
    exit(1)

# /validation of arguments

if (mode == Mode.Search):
    print("Searching all of reddit for: " + keyword)
elif (mode == Mode.Sub):
    print("Getting top posts from r/" + keyword)


file_name: Final = get_unique_filename(keyword.replace(
    " ", "_") + "_" + date.today().strftime(date_format), "json")

results: Final = reddit_reader.search(keyword, config.MAX_POSTS, config.MAX_COMMENTS, config.TIME_RANGE, config.EXCLUDED_SUBREDDIT_KEYWORDS) if mode == Mode.Search else reddit_reader.fetch_top_posts(
    keyword, config.MAX_POSTS, config.MAX_COMMENTS, config.TIME_RANGE)

with open(file_name, "w") as json_file:
    json_file.write(jsons.dumps(results))

print("Saved to " + file_name)
