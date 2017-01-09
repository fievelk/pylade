#/usr/bin/env python
#! -*- coding: utf-8 -*-

import pdb
import pickle
import sys

from twitter_corpus_reader import TwitterCorpusReader

def run_language_detector(training_set_file, test_set_file):
    training_corpus = TwitterCorpusReader(training_set_file)
    test_corpus = TwitterCorpusReader(test_set_file)

    training_profiles = _training_profiles(training_corpus)

    # profs = training_corpus.language_profiles()
    # pdb.set_trace()

def predict_language(text, training_profiles):
    min_distance = sys.maxsize # Set it to a high number before iterating
    for language in training_profiles:
        distance = _distance(text, training_profiles[language])
        if distance < min_distance:
            min_distance = distance
    return distance

def _distance(text_profile, training_profile):
    """
    This method compares two profiles and returns a number which represents the
    distance between them. A high distance means that the language of the texts
    that have been used to generate the profiles is not the same. This distance
    is called "out-of-place" metric in the paper.
    We usually compare a language profile (generated from a training set) to the
    profile generated from a single text (e.g. a tweet or a facebook post).

    """
    # TODO: for each ngram in text_profile, compare its index to the same token
    # in training_profile (if it exists). Then sum all the single distances to
    # get the final distance score.
    pass

def _load_or_compute_profiles(file_name, corpus):
    base_dir = '/home/fievelk/Code/datasets/twitter_lang_dataset/'
    full_path = base_dir + file_name
    try:
        profiles = pickle.load(open(full_path, "rb"))
        print("Pickle profiles loaded for {}...".format(file_name))
    except (OSError, IOError) as e:
        print("Computing profiles for {}...".format(file_name))
        profiles = corpus.language_profiles()
        print("Writing pickle file for {} profiles...".format(file_name))
        pickle.dump(profiles, open(full_path, "wb"))

    return profiles

def _training_profiles(corpus):
    return _load_or_compute_profiles('training_profiles.pickle', corpus)

def main():
    main_directory = '/home/fievelk/Code/datasets/twitter_lang_dataset/'
    training_file = main_directory + 'ppp_training_set.csv'
    test_file = main_directory + 'ppp_test_set.csv'

    run_language_detector(training_file, test_file)

if __name__ == '__main__':
    main()
