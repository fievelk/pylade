from __future__ import division # Safety measure in case we extend to py2.7

from collections import defaultdict
import logging
import sys

from nltk.tokenize import wordpunct_tokenize
from nltk.util import ngrams

import utils

# TODO: Do I need a class? It seems that it does not have any state/variable to store.
class CavnarTrenkleImpl(object):
    def __init__(self):
        pass

    # TODO: rename this method?
    def train(self, labeled_instances, limit=None):
        """
        A profile is a list of ngrams sorted in reverse order (from the most
        frequent to the less frequent). Each language has its own list (profile).
        This method returns a dictionary in which each key is a language whose
        value is a list of ngrams (the language profile).

        """
        language_profiles = dict()
        lang_ngram_freqs = self._language_ngram_frequencies(labeled_instances)
        print("Sorting language profiles in lists")
        for language in lang_ngram_freqs:
            #TODO: This part is almost duplicated in compute_text_profile(). Should use the latter.
            # Sort by value first, and then also by key (alphabetic order) if values are equal
            language_profiles[language] = [ngram[0] for ngram in sorted(lang_ngram_freqs[language].items(), key= lambda x: (x[1], x[0]), reverse=True)[:limit]]
        return language_profiles

    def _language_ngram_frequencies(self, labeled_tweets):
        """
        Compute ngram frequencies for each language in the corpus.

        >>> tweets = [{'language': 'it', 'id_str': '12', 'text': 'Ciao'}, {'language': 'en', 'id_str': '15', 'text': 'Hello'}]
        >>> lang_ngram_freqs = _language_ngram_frequencies(tweets)
        >>> lang_ngram_freqs == {\
            'it': {'c':1, 'i': 1, 'a': 1, 'o': 1, 'ci': 1, \
                'ia': 1, 'ao': 1, 'cia': 1, 'iao': 1, 'ciao': 1}, \
            'en': {'h':1, 'e': 1, 'l': 2, 'o': 1, 'he': 1, 'el': 1, 'll': 1, 'lo': 1, \
                'hel': 1, 'ell': 1, 'llo': 1, 'hell': 1, 'ello': 1, 'hello': 1}}
        True

        """
        # freqs = defaultdict(lambda : defaultdict(int))
        freqs = defaultdict(utils._nested_defaultdict)
        for tweet in labeled_tweets:
              lang = tweet['language']
              tweet_ngram_freqs = self._extract_text_ngram_freqs(tweet['text'])
              utils._merge_dictionaries_summing(freqs[lang], tweet_ngram_freqs)

        return freqs

    def _extract_text_ngram_freqs(self, text):
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

    def evaluate(self, model, test_instances, only_language=None, error_value=1000):
        """
        Evaluate model on test data and gather results.
        `model` is a list of training profiles for languages (see paper).

        """

        print("Evaluating...")
        correct = 0
        incorrect = 0
        total = 0

        for labeled_tweet in test_instances:
            # TODO: this only works with instances which have 'label' and 'text' keys. How could we make it more flexible for other corpora?
            if only_language and labeled_tweet['language'] != only_language:
                continue
            predicted_language = self._predict_language(labeled_tweet['text'], model, error_value=error_value)
            if predicted_language == labeled_tweet['language']:
                correct += 1
            else:
                incorrect += 1
            total += 1
            print("Label: {}, Guess: {}, Correct: {}, Incorrect: {}, Total: {}".format(labeled_tweet['language'], predicted_language, correct, incorrect, total), end='\r')
        print()
        accuracy = correct / total
        print("Accuracy: ", accuracy )

        return accuracy # TODO: this should be a dictionary: {'accuracy': accuracy}

    def _predict_language(self, text, training_profiles, error_value):
        """
        >>> text = 'hello'
        >>> training_profiles = {\
            'en': ['l', 'o', 'lo', 'llo', 'll', 'hello', 'hell', 'hel', 'he', 'h', \
                'ello', 'ell', 'el', 'e'],\
            'it': ['o', 'iao', 'ia', 'i', 'ciao', 'cia', 'ci', 'c', 'ao', 'a']}
        >>> predict_language(text, training_profiles)
        'en'

        """
        min_distance = sys.maxsize # Set it to a high number before iterating
        predicted_language = ''

        text_profile = self._compute_text_profile(text)

        for language in training_profiles:
            distance = self._distance(text_profile, training_profiles[language], error_value=error_value)
            if distance < min_distance:
                min_distance = distance
                predicted_language = language

        return predicted_language

    def _compute_text_profile(self, text, limit=None):
        """
        >>> text = 'Hello'
        >>> compute_text_profile(text)
        ['l', 'o', 'lo', 'llo', 'll', 'hello', 'hell', 'hel', 'he', 'h', 'ello', 'ell', 'el', 'e']
        >>> compute_text_profile(text, limit=2)
        ['l', 'o']

        """
        text_ngram_freqs = self._extract_text_ngram_freqs(text)
        # Sort by value first, and then also by key (inverse alphabetic order) if values are equal
        return [ngram[0] for ngram in sorted(text_ngram_freqs.items(), key=lambda x: (x[1], x[0]), reverse=True)[:limit]]

    def _distance(self, text_profile, training_profile, error_value=1000):
        """
        This method compares two profiles and returns a number which represents the
        distance between them. A high distance means that the language of the texts
        that have been used to generate the profiles is not the same. This distance
        is called "out-of-place" metric in the paper.
        We usually compare a language profile (generated from a training set) to the
        profile generated from a single text (e.g. a tweet or a facebook post).
        Note: If a ngram is not present in the training profile, we penalize the
        text profile using an arbitrary `error_value`. This value should be decided
        based on tuning on the test set.

        >>> text_profile = ['h', 'e', 'l', 'o', 'he']
        >>> training_profile = ['h', 'e', 'l', 'o', 'he']
        >>> _distance(text_profile, training_profile)
        0
        >>> training_profile = ['l', 'o', 'h', 'e', 'he']
        >>> _distance(text_profile, training_profile)
        8

        """
        total_distance = 0
        for index, text_ngram in enumerate(text_profile):
            if text_ngram in training_profile:
                distance = abs(index - training_profile.index(text_ngram))
            else:
                distance = error_value
            total_distance += distance

        return total_distance
