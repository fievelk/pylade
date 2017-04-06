#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Corpus reader for twitter datasets.

The corpus has been obtained using the original Twitter dataset with language
labels (see URL below). Tweet IDs have been subsequently hydrated using Twitter
APIs and NLTK. The result is a new dataset (CSV format) with the following
structure:

    language|id_str|text

where `language` is the label, `id_str` is the tweet ID, and `text` is the
content of the tweet.

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
    """Corpus Reader for custom Twitter corpus.

    Attributes:
        corpus_path (str): A path leading to a CSV corpus file.
        delimiter (str): The character that separates the CSV corpus columns.

    """

    def __init__(self, corpus_path, delimiter='|'):
        super().__init__(corpus_path, delimiter)
        self._available_languages = None

    @property
    def available_languages(self):
        """A list of the available languages in the corpus.

        `und` is for 'undefined'.

        """
        # return AVAILABLE_LANGUAGES
        if not self._available_languages:
            self._available_languages = list(self.languages_tweets_stats().keys())

        return self._available_languages

    def tweets_with_language(self, languages, limit=0):
        """Retrieve tweets with specific languages from the corpus.

        Args:
            languages (list): A list of language labels used to filter tweets.
            limit (int): The maximum number of tweets to return.

        Yields:
            A generator of tweets with specific language labels.

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
