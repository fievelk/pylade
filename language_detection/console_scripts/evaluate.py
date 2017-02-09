# #/usr/bin/env python
# #! -*- coding: utf-8 -*-

import logging
import sys

from language_detection import utils
from language_detection import allowed_classes
from language_detection.console_scripts import evaluate_script_args_parser

def start_evaluation(arguments):
    model_file          = arguments['model']
    test_data_file      = arguments['test-data']
    corpus_class_name   = arguments['corpus_reader_class']
    output_file         = arguments['results_output_file']
    implementation_name = arguments['implementation']

    corpus_reader_class = allowed_classes.find_corpus_reader(corpus_class_name)
    test_corpus = corpus_reader_class(test_data_file)
    model = utils.load_file(model_file)
    implementation = allowed_classes.find_implementation(implementation_name)

    logging.info("Retrieving all documents from test data...")
    test_instances = test_corpus.all_tweets() # TODO: rename this method into 'all_instances', 'all_rows' or similarly generic

    logging.info("Evaluating implementation of {}.".format(implementation.__name__))
    # TODO: Should we only get instances of specified language in advance? Something like:
    #   test_instances = test_corpus.tweets_with_language('it')
    # This is basically what we are doing, but later (spending more memory) I think

    # NOTE: if you want to use test_instances multiple times, they need to be
    # stored in a list, because they have to be regenerated
    # test_instances = list(test_instances)
    evaluation_arguments = utils.convert_unknown_arguments(arguments['eval_args']) or {}
    results = implementation().evaluate(model, test_instances, **evaluation_arguments)
    for result in results:
        utils._save_result(result, output_file)

def main():
    arguments = evaluate_script_args_parser.parse_arguments(sys.argv[1:])
    utils._configure_logger(arguments['loglevel'])
    start_evaluation(arguments)

if __name__ == '__main__':
    main()
