#!/usr/bin/env python
#! -*- coding: utf-8 -*-

"""
Corpus reader for twitter dataset.
The corpus has been obtained using the original twitter dataset with language
labels (see URL below). Tweet ids have been subsequently hydrated using Twitter
APIs and NLTK. The result is a new dataset (CSV format) with the following structure:

    language|id_str|text

where `language` is the label, `id_str` is the tweet ID, and `text` is the content
of the tweet.

Original Twitter data:
- https://blog.twitter.com/2015/evaluating-language-identification-performance

"""

from collections import defaultdict

import csv
import sys
import pdb

from nltk.tokenize import wordpunct_tokenize
from nltk.util import ngrams

# AVAILABLE_LANGUAGES = set({
#     'ar', 'ar_LATN', 'az', 'bg', 'bn', 'bs', 'ca', 'cs', 'cy', 'da', 'de', 'dv',
#     'el', 'en', 'es', 'et', 'eu', 'fa', 'fi', 'fr', 'gl', 'ha', 'he', 'hi', 'hi-Latn',
#     'hr', 'ht', 'hu', 'hy', 'id', 'is', 'it', 'ja', 'ja_LATN', 'jv', 'km', 'ko',
#     'ko_LATN', 'la', 'lt', 'lv', 'mk', 'ml_LATN', 'mn', 'mn_LATN', 'mr', 'ms',
#     'ne', 'nl', 'no', 'pl', 'ps', 'ps_LATN', 'pt', 'ro', 'ru', 'si', 'sk', 'sl',
#     'sq', 'sr', 'su', 'sv', 'sw', 'ta', 'ta_LATN', 'th', 'tl', 'tn', 'tr', 'uk',
#     'und', 'ur', 'ur_LATN', 'vi', 'wo', 'xh', 'zh-CN', 'zh-TW', 'zu'
# })

class TwitterCorpusReader(object):
    """Corpus Reader for custom twitter corpus."""

    def __init__(self, corpus_path=None):
        self.corpus_path = corpus_path

    def all_tweets(self, limit=0):
        """
        Read the corpus and returns a generator for all tweets. Each tweet is a
        dictionary with the following structure:
        {
           'id_str': '484026168300273857',
           'language': 'en',
           'text': 'Some text'
        }

        """
        if not limit:
            limit = sys.maxsize
        with open(self.corpus_path, 'r') as input_file:
            # Find out if the file has a header
            sniffer = csv.Sniffer()
            has_header = sniffer.has_header(input_file.readline())
            input_file.seek(0) # Go back to beginning of file

            # input_data = csv.reader(input_file, delimiter='|')
            input_data = csv.DictReader(input_file, delimiter='|')
            # Skip header
            if has_header:
                next(input_data)
            for i, row in enumerate(input_data):
                if i >= limit:
                    return
                yield row

    def tweets_with_language(self, languages, limit=0):
        """Read the corpus and returns a generator for tweets in a specific
        language.

        """
        # for tweet in self.all_tweets(limit=limit):
        if not limit:
            limit = sys.maxsize

        i = 0
        for tweet in self.all_tweets():
            if tweet['language'] in languages:
                i += 1
                yield tweet

            if i >= limit:
                return

    def available_languages(self):
        # return AVAILABLE_LANGUAGES
        return self.languages_tweets_stats().keys()

    def languages_tweets_stats(self):
        languages_tweets_stats = defaultdict(int)
        for tweet in self.all_tweets():
            lang = tweet['language']
            languages_tweets_stats[lang] += 1
        return languages_tweets_stats

    # --------------------------------------------------------------------------
    # Put following methods in another class (something like Detector) or outside
    # this class. This is needed because we have to use these two methods also to
    # compute the language profile of a single text, not only of a corpus!

    def language_profiles(self):
        """
        A profile is a list of ngrams sorted in reverse order (from the most
        frequent to the less frequent). Each language has its own list (profile).
        This method returns a dictionary in which each key is a language whose
        value is a list of ngrams (the language profile).

        """
        language_profiles = dict()
        ngram_freqs = self.ngram_frequencies()
        print("Sorting language profiles in lists")
        for language in ngram_freqs:
            language_profiles[language] = [ngram[0] for ngram in sorted(ngram_freqs[language].items(), key= lambda x: x[1], reverse=True)]
        return language_profiles

    def ngram_frequencies(self):
        """
        Return a profile of ngram frequencies for each language in the corpus.
        freqs = {'language': {'bla' : 43, 'blaw': 12, 'b': 500}}
        """
        print("Computing language profiles as ngram frequencies")

        # freqs = defaultdict(lambda : defaultdict(int))
        freqs = defaultdict(self._nested_defaultdict)

        for tweet in self.all_tweets():
            lang = tweet['language']
            # freqs[lang] = aggiornarle con quelle del tweet
            tweet_ngram_freqs = self._extract_tweet_ngram_freqs(tweet['text'])
            self._merge_dictionaries(freqs[lang], tweet_ngram_freqs)

        return freqs

    def _nested_defaultdict(self):
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

    def _merge_dictionaries(self, first_dict, second_dict):
        """
        Merge two dictionaries returning an enriched version of the first one.
        Note: this works only with defaultdict.

        """
        for k, v in second_dict.items():
            first_dict[k] += v
        return first_dict

    def _extract_tweet_ngram_freqs(self, text):
        """
        Tokenize the text. For each token in the text, extract ngrams of different
        length (from 1 to 5). Compute how many times each of these ngrams occur
        in the text. Then return a dictionary of { ngram: frequencies }.

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

    # --------------------------------------------------------------------------
