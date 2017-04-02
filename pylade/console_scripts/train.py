#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys

from pylade import utils
from pylade import allowed_classes
from pylade.console_scripts import train_script_args_parser

def start_training(arguments):
    training_data_file = arguments['training-data']
    corpus_reader_class = allowed_classes.find_corpus_reader(arguments['corpus_reader_class'])
    training_corpus = corpus_reader_class(training_data_file)

    # languages =  training_corpus.available_languages()
    logging.info("Retrieving all documents from training corpus...")
    labeled_tweets = training_corpus.all_instances()

    output_file = arguments['model_output_file']

    implementation = allowed_classes.find_implementation(arguments['implementation'])
    logging.info("Training the model. This could take some time...")

    training_arguments = utils.convert_unknown_arguments(arguments['train_args']) or {}
    model = implementation().train(labeled_tweets, **training_arguments)
    utils.save_file(model, output_file)

def main():
    arguments = train_script_args_parser.parse_arguments(sys.argv[1:])
    utils._configure_logger(arguments['loglevel'])
    start_training(arguments)

if __name__ == '__main__':
    main()
