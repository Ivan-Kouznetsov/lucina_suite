from typing_extensions import Final
import nltk
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder, QuadgramCollocationFinder
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from typing import List
import re
from string import punctuation
from model.counted_collocation import CountedCollocation

def remove_stopwords(words: List[str]):
    stops = set(stopwords.words("english"))
    return [word for word in words if word.lower() not in stops
            and word not in punctuation
            and "=" not in word]


def remove_punctuation(words: List[str]):
    for i in range(len(words)):
        words[i] = re.sub("[^\w]*", "", words[i])

    return words


def is_word(s: str):
    return re.match("\w{1,}$", s)


def is_split_word(c: tuple):
    if (c == ("ca", "nt")):
        return True
    if (c == ("wo", "nt")):
        return True
    if (c == ("gon", "na")):
        return True

    return False


def filter_collocations(collocations: List[tuple]):
    return [c for c in collocations if is_word(c[0]) and is_word(c[1]) and not is_split_word(c)]

def count_collocations(text: str, collocations: List[tuple]) -> List[CountedCollocation]:
    result: Final[List[CountedCollocation]] = []
    for collocation in collocations:
        result.append(CountedCollocation(collocation, text.count(" ".join(collocation))))

    return result

def get_collocations(collocation_length: int, text: str, min_freq: int = 3, limit: int = 10):
    "Gets the top *limit* collocations from text that occur a minimum of *min_freq* number of times"
    
    bigram_measures: Final = nltk.collocations.BigramAssocMeasures()
    trigram_measures: Final = nltk.collocations.TrigramAssocMeasures()
    quadgram_measures: Final = nltk.collocations.QuadgramAssocMeasures()

    text = text.replace("--", "").lower()
    words: Final[List[str]] = remove_punctuation(remove_stopwords(word_tokenize(text)))

    if (collocation_length == 2):
        finder = BigramCollocationFinder.from_words(words)
        finder.apply_freq_filter(min_freq) 
        collocations = finder.nbest(bigram_measures.pmi, limit)
        filtered_collocation = filter_collocations(collocations)
    elif (collocation_length == 3):
        finder = TrigramCollocationFinder.from_words(words)
        finder.apply_freq_filter(min_freq) 
        collocations = finder.nbest(trigram_measures.pmi, limit)
        filtered_collocation = filter_collocations(collocations)
    elif (collocation_length == 4):
        finder = QuadgramCollocationFinder.from_words(words)
        finder.apply_freq_filter(min_freq) 
        collocations = finder.nbest(quadgram_measures.pmi, limit)
        filtered_collocation = filter_collocations(collocations)

    return count_collocations(text, filtered_collocation)

def remove_special_chars(s: str) -> str:
    return re.sub(r'[^\x00-\x7f]','',s)

def remove_hashtags_mentions(s: str) -> str:
    return re.sub(r"(#|@)\w+",r"",s)

def remove_links(s: str) -> str:
    return re.sub(r"https?://(\w|\.|/)+", "",s)
