#/usr/bin/env python
#! -*- coding: utf-8 -*-

from __future__ import division

from collections import defaultdict
import pdb
import pickle
import sys

from twitter_corpus_reader import TwitterCorpusReader

import utils

def run_language_detector(training_set_file, test_set_file, only_language=None, error_value=1000):
    training_corpus = TwitterCorpusReader(training_set_file)
    test_corpus = TwitterCorpusReader(test_set_file)

    # Get profiles of training languages using training corpus labeled tweets
    training_profiles = _training_profiles(training_corpus.all_tweets())
    # Get profiles of labeled tweets in the test corpus
    # test_profiles = _test_profiles(test_corpus.all_tweets())

    print("Evaluating...")
    correct = 0
    incorrect = 0
    total = 0

    for labeled_tweet in test_corpus.all_tweets():
        if only_language and labeled_tweet['language'] != only_language:
            continue
        # if labeled_tweet['language'] == 'ar':
        #     continue # Skip arabic just for test (arabic is fine)
        predicted_language = predict_language(labeled_tweet['text'], training_profiles, error_value=error_value)
        if predicted_language == labeled_tweet['language']:
            correct += 1
        else:
            incorrect += 1
        total += 1
        print("Label: {}, Guess: {}, Correct: {}, Incorrect: {}, Total: {}".format(labeled_tweet['language'], predicted_language, correct, incorrect, total), end='\r')
    print()
    # print("Correct: ", correct)
    # print("Incorrect: ", incorrect)
    # print("Total: ", total)
    accuracy = correct / total
    print("Accuracy: ", accuracy )
    # profs = training_corpus.language_profiles()
    return accuracy

def predict_language(text, training_profiles, error_value):
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

    # text_profile = utils.extract_tweet_ngram_freqs(text)
    text_profile = utils.compute_text_profile(text)

    # error_value = max(training_profiles.values(), key=len)
    # pdb.set_trace()
    for language in training_profiles:
        # distance = _distance(text_profile, training_profiles[language], error_value=error_value)
        distance = _distance(text_profile, training_profiles[language], error_value=error_value)
        # print("Distance: ", distance)
        # print("language: ", language)
        # if language == 'ar':
            # pdb.set_trace()
        if distance < min_distance:
            min_distance = distance
            predicted_language = language

    return predicted_language

def _distance(text_profile, training_profile, error_value=1000):
    """
    This method compares two profiles and returns a number which represents the
    distance between them. A high distance means that the language of the texts
    that have been used to generate the profiles is not the same. This distance
    is called "out-of-place" metric in the paper.
    We usually compare a language profile (generated from a training set) to the
    profile generated from a single text (e.g. a tweet or a facebook post).

    >>> text_profile = ['h', 'e', 'l', 'o', 'he']
    >>> training_profile = ['h', 'e', 'l', 'o', 'he']
    >>> _distance(text_profile, training_profile)
    0
    >>> training_profile = ['l', 'o', 'h', 'e', 'he']
    >>> _distance(text_profile, training_profile)
    8

    """
    # TODO: for each ngram in text_profile, compare its index to the same token
    # in training_profile (if it exists). Then sum all the single distances to
    # get the final distance score.
    total_distance = 0
    for index, text_ngram in enumerate(text_profile):
        if text_ngram in training_profile:
            distance = abs(index - training_profile.index(text_ngram))
        else:
            distance = error_value
        total_distance += distance

    return total_distance

def _load_or_compute_profiles(file_name, labeled_tweets):
    # base_dir = '/home/fievelk/Code/datasets/twitter_lang_dataset/'
    base_dir = '/home/fievelk/Code/language_detection/impl_canvar_trenkle/'
    full_path = base_dir + file_name
    try:
        profiles = pickle.load(open(full_path, "rb"))
        print("Pickle profiles loaded for {}...".format(file_name))
    except (OSError, IOError) as e:
        print("Computing profiles for {}...".format(file_name))
        profiles = utils.language_profiles(labeled_tweets, limit=5000)
        print("Writing pickle file for {} profiles...".format(file_name))
        pickle.dump(profiles, open(full_path, "wb"))

    return profiles

def _training_profiles(labeled_tweets):
    return _load_or_compute_profiles('training_profiles.pickle', labeled_tweets)

def save_results(output_file, results):
    with open(output_file, 'a') as output:
        for lang in results:
            for err_value in sorted(results[lang], key=lambda x: results[lang][x]):
                output.write("[{}] [{}] [{}]\n".format(lang, err_value, results[lang][err_value]))
            output.write('\n')
        # for res in sorted(results.items(), key=lambda x: x[1], reverse=True):
        #     output.write("[{}]".format())
        #     print("Err value: {} ---> {}".format(res[0], res[1]))

def main():
    main_directory = '/home/fievelk/Code/datasets/twitter_lang_dataset/'
    training_file = main_directory + 'ppp_training_set.csv'
    test_file = main_directory + 'ppp_test_set.csv'

    # run_language_detector(training_file, test_file)
    results = defaultdict(lambda: defaultdict(float))
    for lang in ['it']:
        for err_val in [100, 200, 300, 400, 600, 1000, 1500, 2000, 3000, 4000]:
            acc = run_language_detector(training_file, test_file, only_language='it', error_value=err_val)
            print('ERR_VAL: {}, accuracy: {}'.format(err_val, acc))
            results[lang][err_val] = acc

    save_results('results.txt', results)

    # with open('results.txt', 'a') as output:
    #     for res in sorted(results.items(), key=lambda x: x[1], reverse=True):
    #         output.write("[{}]".format())
    #         print("Err value: {} ---> {}".format(res[0], res[1]))

if __name__ == '__main__':
    main()
