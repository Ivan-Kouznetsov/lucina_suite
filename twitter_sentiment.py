#!/usr/bin/env python3
from typing_extensions import Final
from typing import List

import sys
from TwitterAPI import TwitterAPI
import config
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from colorama import Fore, Back, Style
from enum import Enum
import re
from service.text_analysis import remove_special_chars, remove_hashtags_mentions, remove_links
from model.tweet import Tweet

analyzer: Final = SentimentIntensityAnalyzer()
twitter: Final = TwitterAPI(config.TWITTER_API_KEY, config.TWITTER_API_SECRET_KEY,
                            config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)
min_tweet_length: Final = 20

# Helper functions

def display_post_sentiment(tweet: Tweet) -> None:
    print(Fore.RED + str(tweet.votes) + Style.RESET_ALL + "\t" + Fore.CYAN + str(tweet.score) + Style.RESET_ALL + "\t"
          + tweet.text + "\n" + Fore.BLUE + tweet.url + Style.RESET_ALL)

def get_score(s: str) -> int:
    s = remove_special_chars(s)
    s = remove_links(s)
    s = remove_hashtags_mentions(s)
    s = s.strip()

    if (len(s)<min_tweet_length):
        return 0

    scores: Final[dict] = analyzer.polarity_scores(s)
    
    return round(abs(scores["compound"])*100)

# /Helper functions


if (len(sys.argv) != 3):
    print("Usage: python3 twitter_sentiment.py query limit")
    exit(1)

query: Final = sys.argv[1]
limit: Final = int(sys.argv[2])

response: Final = twitter.request(
    'search/tweets',
    {'q': query + " -filter:retweets", 'tweet_mode': 'extended', 'count': limit, "lang": "en"})

tweets: Final[List[Tweet]] = []

for item in response:  

    if (len(tweets) >= limit):
        break

    spam = False

    for term in config.TWITTER_SPAM_TERMS:
        if (term.lower() in item["full_text"].lower()):
            spam = True

    if (spam):
        continue

    clean_text = remove_special_chars(item["full_text"])
    score = get_score(clean_text)
    votes = item['retweet_count'] + item['favorite_count']
    
    if (score > 0 and votes > 0):
        tweets.append(Tweet(clean_text, score, "https://twitter.com/i/web/status/" + item["id_str"], votes))

    # sort tweets
    tweets.sort(key=lambda t: t.votes, reverse=True)

for tweet in tweets:
    display_post_sentiment(tweet)