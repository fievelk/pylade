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

import utils

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
