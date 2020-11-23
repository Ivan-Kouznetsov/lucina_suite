#!/usr/bin/env python3
from typing_extensions import Final
from typing import List

import sys
import pandas
from nltk.tokenize import word_tokenize
from collections import Counter
from colorama import Fore, Style

if (len(sys.argv) != 5):
    print("Usage: python3 chat_trends.py chatlog1.csv chatlog2.csv text_col_name limit")
    exit(1)

filename1: Final = sys.argv[1]
filename2: Final = sys.argv[2]
text_colomn_name: Final = sys.argv[3]
limit: Final[int] = int(sys.argv[4])

def get_all_text(filename: str, col_name:str):
    return pandas.read_csv(filename)[[col_name]].to_csv(index=False, header=False) #todo: check for col name

def get_top_most_common(text:str, limit: int):
    tokens = word_tokenize(text.lower())
    frequencies = Counter(word for word in tokens if len(word) > 1)
    return frequencies.most_common(limit)

def print_top_words(top_words:list):
     for word, frequency in top_words:  
         print(Fore.CYAN + str(frequency) + Style.RESET_ALL + " " + word)

def print_difference(top_words_list1:list, top_words_list2:list):
    top_words_list1_dict = dict(top_words_list1)
    diff:dict ={}

    for word, frequency in top_words_list2:
        diff[word] = frequency - (top_words_list1_dict[word] if word in [t[0] for t in top_words_list1] else 0)
    
    sorted_diff = sorted(diff.items(), key=lambda item: item[1])
    sorted_diff.reverse()

    for word, frequency_change in sorted_diff:
        if (frequency_change >= 0):
            print(Fore.GREEN + "+" + str(frequency_change) + Style.RESET_ALL + " " + word)
        else:
            print(Fore.RED + str(frequency_change) + Style.RESET_ALL + " " + word)

print("Reading files")

all_text1 = get_all_text(filename1, text_colomn_name)
all_text2 = get_all_text(filename2, text_colomn_name)

top_words1 = get_top_most_common(all_text1, limit)
top_words2 = get_top_most_common(all_text2, limit)

print("First file:")
print_top_words(top_words1)


print("Second file:")
print_top_words(top_words2)

print("\n\nDifference:")
print_difference(top_words1, top_words2)



