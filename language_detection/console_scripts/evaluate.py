# #/usr/bin/env python
# #! -*- coding: utf-8 -*-

import argparse
import json
import logging

from language_detection import utils
from language_detection import allowed_classes

def _parse_arguments():
    """Parse arguments provided from command-line and return them as a dictionary."""
    description = "Evaluate a language detection model using a test corpus."
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
        'model',
        help="Path to model input file (e.g. model.json)",
    )
    parser.add_argument(
        '-i', '--implementation',
        help="Chosen method (e.g. CanvarTrenkle)",
        action="store", dest="implementation",
        default='CavnarTrenkleImpl'
    )
    parser.add_argument(
        'test-data',
        help="Path for test data file (e.g. test_tweets.csv). This file needs to\
              be compatible with the Corpus Reader (specified with the \
              --corpus-reader option)",
        default='test_data.csv'
    )
    parser.add_argument(
        '-c', '--corpus-reader',
        help="Corpus Reader class for test data (e.g. TwitterCorpusReader)",
        action="store", dest="corpus_reader_class",
        default='TwitterCorpusReader'
    )
    parser.add_argument(
        '-o', '--output',
        help="Output results file in JSON (e.g. results.json)",
        action="store", dest="results_output_file",
        default='results.json'
    )
    # This argument is a json object which will be mapped to dict
    parser.add_argument(
        '--eval-args',
        help="Arguments for the evaluation method (JSON format)",
        action="store", dest="eval_args",
        type=json.loads
    )

    return vars(parser.parse_args())

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
    arguments = _parse_arguments()
    utils._configure_logger(arguments['loglevel'])
    start_evaluation(arguments)

if __name__ == '__main__':
    main()
