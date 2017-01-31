from __future__ import division # Safety measure in case we extend to py2.7

from collections import defaultdict
import sys

from nltk.tokenize import wordpunct_tokenize
from nltk.util import ngrams

from language_detection import utils

# TODO: Store instance variables (e.g. model)
class CavnarTrenkleImpl(object):
    def __init__(self):
        pass

    # TODO: rename this method?
    def train(self, labeled_instances, limit=None, verbose=False):
        """
        A profile is a list of ngrams sorted in reverse order (from the most
        frequent to the less frequent). Each language has its own list (profile).
        This method returns a dictionary in which each key is a language whose
        value is a list of ngrams (the language profile).

        `limit`: the number of entries in the training language profiles. Less
        entries make training faster, but it's better to keep a balance between
        speed and accuracy.

        """
        if verbose:
            print("Training. Limit: {}".format(limit))

        language_profiles = dict()
        languages_ngram_freqs = self._languages_ngram_frequencies(labeled_instances)
        print("Sorting language profiles in lists")
        for language in languages_ngram_freqs:
            language_profiles[language] = self._compute_profile_from_frequencies(languages_ngram_freqs[language], limit)
        return language_profiles

    def _compute_profile_from_frequencies(self, frequencies_dict, limit):
        # Sort by value first, and then also by key (alphabetic order) if values are equal
        return [ngram[0] for ngram in sorted(frequencies_dict.items(), key= lambda x: (x[1], x[0]), reverse=True)[:limit]]

    def _compute_text_profile(self, text, limit=None):
        """
        >>> implementation = CavnarTrenkleImpl()
        >>> text = 'Hello'
        >>> implementation._compute_text_profile(text)
        ['l', 'o', 'lo', 'llo', 'll', 'hello', 'hell', 'hel', 'he', 'h', 'ello', 'ell', 'el', 'e']
        >>> implementation._compute_text_profile(text, limit=2)
        ['l', 'o']

        """
        text_ngram_freqs = self._extract_text_ngram_freqs(text)
        return self._compute_profile_from_frequencies(text_ngram_freqs, limit)

    def _languages_ngram_frequencies(self, labeled_tweets):
        """
        Compute ngram frequencies for each language in the corpus.

        >>> implementation = CavnarTrenkleImpl()
        >>> tweets = [{'language': 'it', 'id_str': '12', 'text': 'Ciao'}, {'language': 'en', 'id_str': '15', 'text': 'Hello'}]
        >>> lang_ngram_freqs = implementation._languages_ngram_frequencies(tweets)
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
              utils.merge_dictionaries_summing(freqs[lang], tweet_ngram_freqs)

        return freqs

    def _extract_text_ngram_freqs(self, text):
        """
        Tokenize the text. For each token in the text, extract ngrams of different
        length (from 1 to 5). Compute how many times each of these ngrams occur
        in the text. Then return a dictionary of { ngram: frequencies }.

        >>> implementation = CavnarTrenkleImpl()
        >>> ngrams = implementation._extract_text_ngram_freqs("HeLLo")
        >>> ngrams == {'h':1, 'e': 1, 'l': 2, 'o': 1, 'he': 1, 'el': 1, 'll': 1, \
            'lo': 1, 'hel': 1, 'ell': 1, 'llo': 1, 'hell': 1, 'ello': 1, 'hello': 1}
        True
        >>> ngrams = implementation._extract_text_ngram_freqs("CIAO")
        >>> ngrams == {'c':1, 'i': 1, 'a': 1, 'o': 1, 'ci': 1, 'ia': 1, 'ao': 1, \
            'cia': 1, 'iao': 1, 'ciao': 1}
        True

        """
        tokens = wordpunct_tokenize(text.lower()) # Force lower case
        #TODO: Delete numbers and punctuation
        #TODO: Should we use nltk twitter tokenizer?

        ngram_freqs = defaultdict(int)
        for token in tokens:
            for n in range(1,6): # Use 1-grams to 5-grams
                for ngram in ngrams(token, n):
                    ngram_string = ''.join(ngram)
                    ngram_freqs[ngram_string] += 1
                # ngram_freqs[ngrams(token, n)] += 1

        return ngram_freqs

    # def evaluate(self, model, test_instances, languages=None, error_values=None, split_languages=False, output_file=None):
    def evaluate(self, model, test_instances, languages=None, error_values=None, split_languages=False):
        """
        Evaluate model on test data and gather results.
        `model` is a list of training profiles for languages (see paper).

        `languages`: when specified, the model is only evaluated on test
        instances with these labels (e.g. 'it').
        `split_languages`: if True, each language in `languages` is evaluated
        separately and results will be split by language. If False (default)
        results are computed over all instances belonging to `languages`.

        NOTE: if you want to use test_instances multiple times, they need to be
        stored in a list. Since they are a generator object, they would be
        exhausted after the first iteration.

        """
        if error_values is None:
            error_values = [8000]

        # Make sure it is a list of integers:
        if isinstance(error_values, (int, float, str)):
            error_values = [int(val) for val in [error_values]]

        # Make sure that test_instances is a list when we need multiple iterations
        if len(error_values) > 1 or split_languages is True:
            test_instances = list(test_instances)

        print("Evaluating...")
        results = defaultdict(lambda: defaultdict(float))

        if languages and split_languages is True:
            for lang in languages: # TODO: Refactor duplicated code below
                for err_val in error_values:
                    print("Evaluating results for LANG: {}, ERR_VAL: {}".format(lang, err_val))
                    accuracy = self._evaluate_for_languages(test_instances, model, err_val, [lang])
                    results[lang][str(err_val)] = accuracy
                    single_result = {lang: {str(err_val): accuracy}}
                    yield single_result
        else:
            tested_langs = ' '.join(languages) if languages else 'ALL'
            for err_val in error_values:
                print("Evaluating results for [{}], ERR_VAL: {}".format(tested_langs, err_val, languages))
                accuracy = self._evaluate_for_languages(test_instances, model, err_val)
                results[tested_langs][str(err_val)] = accuracy
                single_result = {tested_langs: {str(err_val): accuracy}}
                yield single_result

    def _evaluate_for_languages(self, test_instances, model, error_value, languages=None):
        correct = 0
        incorrect = 0
        total = 0
        for labeled_tweet in test_instances:
            # Skip instances with different languages
            # TODO: This would not be necessary if we could use only instances
            # with specific labels (a subset of test_instances). To be fixed.
            if languages and labeled_tweet['language'] not in languages:
                continue
            predicted_language = self.predict_language(labeled_tweet['text'], model, error_value=error_value)
            if predicted_language == labeled_tweet['language']:
                correct += 1
            else:
                incorrect += 1
            total += 1

            print("Label: {}, Guess: {}, Correct: {}, Incorrect: {}, Total: {}   ".format(labeled_tweet['language'], predicted_language, correct, incorrect, total), end='\r', flush=True)
        print()
        accuracy = correct / total
        # single_result = {languages: {str(err_val): accuracy}}
        return accuracy # TODO: this should be a dictionary: {'accuracy': accuracy}

    def predict_language(self, text, training_profiles, error_value=8000):
        """
        >>> implementation = CavnarTrenkleImpl()
        >>> text = 'hello'
        >>> training_profiles = {\
            'en': ['l', 'o', 'lo', 'llo', 'll', 'hello', 'hell', 'hel', 'he', 'h', \
                'ello', 'ell', 'el', 'e'],\
            'it': ['o', 'iao', 'ia', 'i', 'ciao', 'cia', 'ci', 'c', 'ao', 'a']}
        >>> implementation.predict_language(text, training_profiles)
        'en'

        NOTE: This method could be improved by simply iterating over distances and
        discarding them when they are smaller than the previous one. This would
        not allow us to reuse `predict_language_scores` here.

        NOTE: This is the same as:
            lang_distances = self.predict_language_scores(text, training_profiles, error_value)
            min(lang_distances, key=lang_distances.get)

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
        >>> implementation = CavnarTrenkleImpl()
        >>> implementation._distance(text_profile, training_profile)
        0
        >>> training_profile = ['l', 'o', 'h', 'e', 'he']
        >>> implementation._distance(text_profile, training_profile)
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
