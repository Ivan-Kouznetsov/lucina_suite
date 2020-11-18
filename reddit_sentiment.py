#!/usr/bin/env python3
from typing_extensions import Final
from typing import List

import sys
import json
from types import SimpleNamespace
from model.post import Post
import re
from util.text_helper import pre_process_text
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from colorama import Fore, Back, Style

analyzer: Final = SentimentIntensityAnalyzer()

# Helper functions

def display_post_sentiment(sentiment_scores:dict, votes:int, title:str, url: str):
    compound: Final[int] = int(round(sentiment_scores["compound"] * 100))
    sentiment_color: str = Fore.GREEN
    if (compound == 0):
        sentiment_color = Fore.YELLOW
    elif (compound < 0):
        sentiment_color = Fore.RED        

    print(sentiment_color + str(compound) + Style.RESET_ALL + "\t" +
          Fore.CYAN + str(votes) + Style.RESET_ALL + "\t" + title + "\n" +
          Fore.BLUE + "http://reddit.com" + url + Style.RESET_ALL)

# /Helper functions

if (len(sys.argv) < 2 or len(sys.argv) > 3):
     print("Usage: python3 reddit_sentiment.py posts_file.json [limit]")
     exit(1)

file_name: Final = sys.argv[1]
limit: Final = int(sys.argv[2]) if len(sys.argv) == 3 else None

try:
    with open(file_name, "r") as posts_file:
        posts: Final[list] = json.loads(posts_file.read(), object_hook=lambda d: SimpleNamespace(**d))
        
        count = 0
        for post in posts:
            if (limit is not None and limit < count):
                break
            
            count += 1
            all_comment_text = ""
            for comment in post.comments: 
                all_comment_text += " " + comment.text

            scores = analyzer.polarity_scores(pre_process_text(post.title + post.text + " " + all_comment_text))
            display_post_sentiment(scores, post.score, post.title, post.permalink)
            print("")
        
except IOError as err:
    print("Could not read {} because {}".format(file_name, str(err)))
    exit(1)
