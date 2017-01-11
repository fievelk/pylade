#!/usr/bin/env python
#! -*- coding: utf-8 -*-

from collections import defaultdict

from nltk.util import ngrams
from nltk.tokenize import wordpunct_tokenize

def language_profiles(labeled_tweets, limit=None):
    """
    A profile is a list of ngrams sorted in reverse order (from the most
    frequent to the less frequent). Each language has its own list (profile).
    This method returns a dictionary in which each key is a language whose
    value is a list of ngrams (the language profile).

    """
    language_profiles = dict()
    lang_ngram_freqs = _language_ngram_frequencies(labeled_tweets)
    print("Sorting language profiles in lists")
    for language in lang_ngram_freqs:
        #TODO: This part is almost duplicated in compute_text_profile(). Should use the latter.
        # Sort by value first, and then also by key (alphabetic order) if values are equal
        language_profiles[language] = [ngram[0] for ngram in sorted(lang_ngram_freqs[language].items(), key= lambda x: (x[1], x[0]), reverse=True)[:limit]]
    return language_profiles

def compute_text_profile(text, limit=None):
    """
    >>> text = 'Hello'
    >>> compute_text_profile(text)
    ['l', 'o', 'lo', 'llo', 'll', 'hello', 'hell', 'hel', 'he', 'h', 'ello', 'ell', 'el', 'e']
    >>> compute_text_profile(text, limit=2)
    ['l', 'o']

    """
    text_ngram_freqs = _extract_text_ngram_freqs(text)
    # Sort by value first, and then also by key (inverse alphabetic order) if values are equal
    return [ngram[0] for ngram in sorted(text_ngram_freqs.items(), key=lambda x: (x[1], x[0]), reverse=True)[:limit]]

def _language_ngram_frequencies(labeled_tweets):
    """
    Return a profile of ngram frequencies for each language in the corpus.
    freqs = {'language': {'bla' : 43, 'blaw': 12, 'b': 500}}

    >>> tweets = [{'language': 'it', 'id_str': '12', 'text': 'Ciao'}, {'language': 'en', 'id_str': '15', 'text': 'Hello'}]
    >>> lang_ngram_freqs = _language_ngram_frequencies(tweets)
    >>> lang_ngram_freqs == {\
        'it': {'c':1, 'i': 1, 'a': 1, 'o': 1, 'ci': 1, \
            'ia': 1, 'ao': 1, 'cia': 1, 'iao': 1, 'ciao': 1}, \
        'en': {'h':1, 'e': 1, 'l': 2, 'o': 1, 'he': 1, 'el': 1, 'll': 1, 'lo': 1, \
            'hel': 1, 'ell': 1, 'llo': 1, 'hell': 1, 'ello': 1, 'hello': 1}}
    True
    """
    # print("Computing language profiles as ngram frequencies")

    # freqs = defaultdict(lambda : defaultdict(int))
    freqs = defaultdict(_nested_defaultdict)

    for tweet in labeled_tweets:
        lang = tweet['language']
        # freqs[lang] = aggiornarle con quelle del tweet
        tweet_ngram_freqs = _extract_text_ngram_freqs(tweet['text'])
        _merge_dictionaries(freqs[lang], tweet_ngram_freqs)

    return freqs

def _extract_text_ngram_freqs(text):
    """
    Tokenize the text. For each token in the text, extract ngrams of different
    length (from 1 to 5). Compute how many times each of these ngrams occur
    in the text. Then return a dictionary of { ngram: frequencies }.

    >>> ngrams = _extract_text_ngram_freqs("HeLLo")
    >>> ngrams == {'h':1, 'e': 1, 'l': 2, 'o': 1, 'he': 1, 'el': 1, 'll': 1, \
        'lo': 1, 'hel': 1, 'ell': 1, 'llo': 1, 'hell': 1, 'ello': 1, 'hello': 1}
    True
    >>> ngrams = _extract_text_ngram_freqs("CIAO")
    >>> ngrams == {'c':1, 'i': 1, 'a': 1, 'o': 1, 'ci': 1, 'ia': 1, 'ao': 1, \
        'cia': 1, 'iao': 1, 'ciao': 1}
    True
    """
    tokens = wordpunct_tokenize(text.lower()) # Force lower case
    #TODO: Eliminare numeri e punteggiatura
    #TODO: Usare il twitter tokenizer?

    ngram_freqs = defaultdict(int)
    for token in tokens:
        for n in range(1,6): # Use 1-grams to 5-grams
            for ngram in ngrams(token, n):
                ngram_string = ''.join(ngram)
                ngram_freqs[ngram_string] += 1
            # ngram_freqs[ngrams(token, n)] += 1

    return ngram_freqs

def _nested_defaultdict():
    """
    Note: this function is defined in order to avoid Pickle errors:
        AttributeError: Can't pickle local object
        'TwitterCorpusReader.ngram_frequencies.<locals>.<lambda>'
    Explanation:
        Functions are pickled by name, not by code. Unpickling will only work
        if a function with the same name is present in in the same module.
        This is why pickling a lambda won't work: they have no individual names.
    """
    return defaultdict(int)


def _merge_dictionaries(first_dict, second_dict):
    """
    Merge two dictionaries returning an enriched version of the first one.
    Note: this works only with defaultdict.

    """
    for k, v in second_dict.items():
        first_dict[k] += v
    return first_dict
