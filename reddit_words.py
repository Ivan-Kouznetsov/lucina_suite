#!/usr/bin/env python3
from typing_extensions import Final

import sys
import nltk
import re
import string
import json
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from service.text_analysis import remove_stopwords, remove_punctuation
from types import SimpleNamespace
from model.post import Post
from colorama import Fore, Style

def lemmatize_words(text: str):
    non_words: Final = ["nt"]
    words = remove_punctuation(remove_stopwords(word_tokenize(text)))
    lemma = WordNetLemmatizer()
    
    for i in range(len(words)):
        words[i] = lemma.lemmatize(words[i])

    return [word for word in words if len(word) > 1 and word not in non_words]


if (__name__ == "__main__"):
    if (len(sys.argv) != 3):
        print("Usage: python3 reddit_words.py posts_file.json limit")
        exit(1)
    
    file_name: Final = sys.argv[1]
    limit: Final = int(sys.argv[2])

    try:
        with open(file_name, "r") as posts_file:
            all_text = ""
            posts: Final[list] = json.loads(posts_file.read(), object_hook=lambda d: SimpleNamespace(**d))

            for post in posts:
                 all_text += str(Post.from_object(post))

            lemmatized_words = lemmatize_words(all_text.lower())
            frequencies = Counter(word for word in lemmatized_words)
            for word, frequency in frequencies.most_common(limit):  
                print(Fore.CYAN + str(frequency) + Style.RESET_ALL + " " + word)

    except IOError as err:
        print("Could not read {} because {}".format(file_name, str(err)))
        exit(1)


