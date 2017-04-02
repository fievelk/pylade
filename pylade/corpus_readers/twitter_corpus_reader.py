#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import sys

from .csv_corpus_reader import CSVCorpusReader

# AVAILABLE_LANGUAGES = set({
#     'ar', 'ar_LATN', 'az', 'bg', 'bn', 'bs', 'ca', 'cs', 'cy', 'da', 'de', 'dv',
#     'el', 'en', 'es', 'et', 'eu', 'fa', 'fi', 'fr', 'gl', 'ha', 'he', 'hi', 'hi-Latn',
#     'hr', 'ht', 'hu', 'hy', 'id', 'is', 'it', 'ja', 'ja_LATN', 'jv', 'km', 'ko',
#     'ko_LATN', 'la', 'lt', 'lv', 'mk', 'ml_LATN', 'mn', 'mn_LATN', 'mr', 'ms',
#     'ne', 'nl', 'no', 'pl', 'ps', 'ps_LATN', 'pt', 'ro', 'ru', 'si', 'sk', 'sl',
#     'sq', 'sr', 'su', 'sv', 'sw', 'ta', 'ta_LATN', 'th', 'tl', 'tn', 'tr', 'uk',
#     'und', 'ur', 'ur_LATN', 'vi', 'wo', 'xh', 'zh-CN', 'zh-TW', 'zu'
# })

class TwitterCorpusReader(CSVCorpusReader):
    """Corpus Reader for custom twitter corpus."""

    def __init__(self, corpus_path, delimiter='|'):
        super().__init__(corpus_path, delimiter)
        self._available_languages = None

    @property
    def available_languages(self):
        """
        Return a list of the available languages in the corpus.
        'und' is for 'undefined'.

        """
        # return AVAILABLE_LANGUAGES
        if not self._available_languages:
            self._available_languages = list(self.languages_tweets_stats().keys())

        return self._available_languages

    def tweets_with_language(self, languages, limit=0):
        """Read the corpus and return a generator for tweets in a specific
        language.

        """
        if not limit:
            limit = sys.maxsize

        i = 0
        for tweet in self.all_instances():
            if tweet['language'] in languages:
                i += 1
                yield tweet

            if i >= limit:
                return

    def languages_tweets_stats(self):
        """
        Return a defaultdict containing the number of tweets for each
        language in the corpus. E.g.:

            defaultdict(int, {'en': 200, 'it': 140})

        """
        languages_tweets_stats = defaultdict(int)
        for tweet in self.all_instances():
            lang = tweet['language']
            languages_tweets_stats[lang] += 1
        return languages_tweets_stats
