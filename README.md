# Lucina

NLP analysis programs for exploratory data analysis of data from social media.

# Configuration

See config.txt for an example of a config file.

# Usage

Tested on Linux only. For usage run the individual programs with no arguments.

Examples of usage:

> ./reddit_fetch.py "#MY_COMPANY"

This will download reddit posts that mention #MY_COMPANY and save them to json file, which will be ready to be analysized by the other programs in the suite.

> ./reddit_collocations MY_COMPANY_somedate.json MIN_OCCURANCES MAX_NUMBER_PER_LENTH_OF_COLLOCATION
e.g. ./reddit_collocations.py MY_COMPANY_somedate.json 4 10


This will return the most common phrases (or collocations) that occur a minimum of 4 times and for each lenth of collcation (bigrams, trugrams, quadgrams) up to 10 will be shown, for a mximum total of 30. 

> ./reddit_context.py MY_COMPANY_somedate.json "hello world"

This will show examples of the context in which the phrase hello world was used.

> ./reddit_sentiment.py MY_COMPANY_somedate.json LIMIT

This will show up to LIMIT number of top posts and their sentiment value (negative or positive)

> ./reddit_words.py MY_COMPANY_somedate.json LIMIT

This will show the top words used, without regard to how they are conjugated.

> ./twitter_sentiment.py QUERY LIMIT

This will show the top tweets that match the query along with absolute sentiment scores (how emotional the post is, irrespective of negative or positive emotion)

The default time frame for all requests is 1 week.

# API keys
These programs require API keys from Reddit and Twitter to be able to request data from those services, please set the API keys in the config.py file.


