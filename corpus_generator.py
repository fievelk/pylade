#/usr/bin/env python
#! -*- coding: utf-8 -*-

from collections import defaultdict
import csv

from twitter_corpus_reader import TwitterCorpusReader

def _compute_partitions(corpus):
    partitions = defaultdict(int)
    for lang, freq in corpus.languages_tweets_stats().items():
        # We only use a subset of languages. In particular, we only use those languages
        # for which we have at least 200 labeled tweets. This is done so that we will
        # have enough data for both training and testing.
        if freq >= 200:
            training_examples = int(freq * 0.7) # use 2/3 of tweets for the training set
            test_examples = freq - training_examples # use remaining tweets for the test set
            partitions[lang] = {'training_limit': training_examples, 'test_limit': test_examples}
    return partitions

def generate_training_and_test_datasets(all_labeled_data, training_output, test_output):
    corpus = TwitterCorpusReader(all_labeled_data)
    # useful_languages = (lang for lang, freq in corpus.languages_tweets_stats().items() if freq >= 200)

    partitions = _compute_partitions(corpus)
    # import pdb
    # pdb.set_trace()
    with open(training_output, 'w') as output_train_file, open(test_output, 'w') as output_test_file:
        field_names = ['language', 'id_str', 'text']
        train_writer = csv.DictWriter(output_train_file, fieldnames=field_names, delimiter='|')
        test_writer = csv.DictWriter(output_test_file, fieldnames=field_names, delimiter='|')
        train_writer.writeheader()
        test_writer.writeheader()

        # Count the number of tweets that we already stored in the training dataset
        already_written_in_training = defaultdict(int)

        for tweet in corpus.all_tweets():
            if tweet['language'] in partitions:
                lang = tweet['language']
                if already_written_in_training[lang] <= partitions[lang]['training_limit']:
                    print('Save in training')
                    train_writer.writerow({'language': lang, 'id_str': tweet['id_str'], 'text': tweet['text']})
                    already_written_in_training[lang] += 1
                else:
                    print('Save in test')
                    # If we already stored the max of training file, store the rest in the test data file
                    test_writer.writerow({'language': lang, 'id_str': tweet['id_str'], 'text': tweet['text']})

def main():
    main_directory = '/home/fievelk/Code/datasets/twitter_lang_dataset/'
    corpus_file = main_directory + 'ppp_tweets_labeled_data.csv'
    training_file = main_directory + 'ppp_training_set.csv'
    test_file = main_directory + 'ppp_test_set.csv'

    generate_training_and_test_datasets(corpus_file, training_file, test_file)

if __name__ == '__main__':
    Print("Are you sure? Then uncomment main() in the file!")
    # main()
