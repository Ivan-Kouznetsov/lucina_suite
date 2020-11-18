#!/usr/bin/env python3
import sys
import spacy
from spacy.lang.en import English
from spacy.matcher import Matcher
import config

if (len(sys.argv) != 2):
    print("Usage: python3 pos_patterns.py \"string\"")
    exit(1)

nlp = spacy.load('en_core_web_lg')

def find_rule_matches(text: str):
    doc = nlp(text)
    matcher = Matcher(nlp.vocab, True)
    result = []

    for rule in config.PATTERN_RULES:
     
        matcher.add(rule["name"], None, rule["pattern"])
        matches = matcher(doc)

        # uncomment to print parts of speech of all tokens in text

        # for token in doc:
        #    print(token.text, token.pos_)

        for match in [doc[start:end] for match_id, start, end in matches]:

            for token in match:
                assert isinstance(rule["lemmas_to_look_for"], list)
                if (token.pos_== rule["pos_to_look_for"] and token.lemma_ in rule["lemmas_to_look_for"]):
                    result.append(match.text)
    
    return result

print(find_rule_matches(sys.argv[1]))