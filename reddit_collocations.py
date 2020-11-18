#!/usr/bin/env python3
from typing_extensions import Final
from typing import List

import sys
import json
from types import SimpleNamespace
from model.post import Post
from service.text_analysis import get_collocations
import re
import config
from util.text_helper import pre_process_text
from model.counted_collocation import CountedCollocation
from colorama import Fore, Back, Style

# Helper functions

def display_collocations(counted_collocations: List[CountedCollocation]):
    for c in counted_collocations:
        if (c.count > 0):
            print(" ".join(c.collocation))

# /Helper functions

if __name__ == "__main__":
    if (len(sys.argv) < 2 or len(sys.argv) > 4) :
        print("Usage: python3 reddit_collocations.py posts_file.json [min occurrence] [max results for each length]")
        exit(1)

    file_name: Final = sys.argv[1]
    min_occurrence = config.MIN_FREQ    
    max_results = config.RESULT_LIMIT

    if (len(sys.argv)>=3):
        min_occurrence = int(sys.argv[2])
    
    if (len(sys.argv)>=4):
        max_results = int(sys.argv[3])

    try:
        collocations: List[CountedCollocation] = []
        with open(file_name, "r") as posts_file:
            posts: Final[list] = json.loads(posts_file.read(), object_hook=lambda d: SimpleNamespace(**d))
            all_text = ""
            for post in posts:
                all_text += str(Post.from_object(post))

            for i in range(4,1,-1):    
                collocations += get_collocations(i, pre_process_text(all_text), min_occurrence, max_results)

        collocations.sort(key=lambda c: c.count, reverse=True)
        display_collocations(collocations)

    except IOError as err:
        print("Could not read {} because {}".format(file_name, str(err)))
        exit(1)
