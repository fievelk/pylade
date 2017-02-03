#/usr/bin/env python
#! -*- coding: utf-8 -*-

from __future__ import division
from collections import defaultdict
import argparse
import json
import logging
import sys

from language_detection import utils
from language_detection import allowed_classes

def _parse_arguments():
    """Parse arguments provided from command-line and return them as a dictionary."""
    description = "Train a language detection model using a training corpus."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '-d', '--debug',
        help="Activates debug mode",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        '-v', '--verbose',
        help="Activates verbose mode",
        action="store_const", dest="loglevel", const=logging.INFO,
    )
    parser.add_argument(
        '-i', '--implementation',
        help="Chosen method (e.g. CanvarTrenkle)",
        action="store", dest="implementation",
        default='CavnarTrenkleImpl'
    )
    parser.add_argument(
        'training-data',
        help="Path for training data file (e.g. training_tweets.csv)",
    )
    parser.add_argument(
        '-c', '--corpus-reader',
        help="Corpus Reader class (e.g. TwitterCorpusReader)",
        action="store", dest="corpus_reader_class",
        default='TwitterCorpusReader'
    )
    parser.add_argument(
        '-o', '--output',
        help="Output model",
        action="store", dest="model_output_file",
        default='model.json'
    )
    # This argument is a json object which will be mapped to dict
    parser.add_argument(
        '--train-args',
        help="Arguments for the training method (JSON format)",
        action="store", dest="train_args",
        type=json.loads
    )

    return vars(parser.parse_args())

def start_training(arguments):
    training_data_file = arguments['training-data']
    corpus_reader_class = allowed_classes.find_corpus_reader(arguments['corpus_reader_class'])
    training_corpus = corpus_reader_class(training_data_file)

    # languages =  training_corpus.available_languages()
    logging.info("Retrieving all documents from training corpus...")
    labeled_tweets = training_corpus.all_tweets() # TODO: rename this method into 'all_instances', 'all_rows' or similarly generic

    output_file = arguments['model_output_file']

    implementation = allowed_classes.find_implementation(arguments['implementation'])
    logging.info("Training the model. This could take some time...")

    training_arguments = utils.convert_unknown_arguments(arguments['train_args']) or {}
    model = implementation().train(labeled_tweets, **training_arguments)
    utils.save_file(model, output_file)

def main():
    arguments = _parse_arguments()
    utils._configure_logger(arguments['loglevel'])
    start_training(arguments)

if __name__ == '__main__':
    main()
