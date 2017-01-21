# #/usr/bin/env python
# #! -*- coding: utf-8 -*-

import argparse
import logging

import utils

def _parse_arguments():
    """Parse arguments provided from command-line and return them as a dictionary."""
    parser = argparse.ArgumentParser()
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
        '-m', '--model',
        help="Path to model input file (e.g. model.json)",
        action="store", dest="model_file",
        default='model.json'
    )
    parser.add_argument(
        '-i', '--implementation',
        help="Chosen method (e.g. CanvarTrenkle)",
        action="store", dest="implementation",
        default='CavnarTrenkleImpl'
    )
    parser.add_argument(
        '--model-format',
        help="Model file format (e.g. json)",
        action="store", dest="model_file_format",
        default='json'
    )
    parser.add_argument(
        '-t', '--test-data',
        help="Path for test data file (e.g. test_tweets.csv). This file needs to\
              be compatible with the Corpus Reader (specified with the \
              --corpus-reader option)",
        action="store", dest="test_data_file",
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

    return vars(parser.parse_args())

def start_evaluation(arguments):
    model_file = arguments['model_file'] #json
    model_file_format = arguments['model_file_format']
    model = utils.load_file(model_file, file_format=model_file_format)

    test_data_file = arguments['test_data_file']
    corpus_reader_class = utils.find_corpus_reader(arguments['corpus_reader_class'])
    test_corpus = corpus_reader_class(test_data_file)

    # languages =  training_corpus.available_languages() # Find a way to pass all possible labels
    logging.info("Retrieving all documents from test data...")
    test_instances = test_corpus.all_tweets() # TODO: rename this method into 'all_instances', 'all_rows' or similarly generic

    output_file = arguments['results_output_file']

    implementation = utils.find_implementation(arguments['implementation'])
    # TODO: At the moment, results are just accuracy (float). We should foresee a dictionary of key-values (precision, recall, accuracy, ...)
    # TODO: `only_language` and `error_value` should be kwargs explicitly passed by command-line.
    # This is because they can differ from implementation to implementation
    results = implementation().evaluate(model, test_instances, only_language=None, error_value=8000)
    utils.save_file(model, output_file)


# TODO: This was used to test several implementations using several parameters.
# How can we restore something similar, taking parameters from CLI?
# def evaluate_implementation(implementation, error_values, languages, output_file=None, *args, **kwargs):
#     """
#     Evaluate language identification implementation.
#
#     """
#     print("Evaluating implementation of {}.".format(implementation.__name__))
#     print("Error values: ", error_values)
#     print("Languages: ", languages)
#     print()
#
#     results = defaultdict(lambda: defaultdict(float))
#     for lang in languages:
#         for err_val in error_values:
#             print("Evaluating results for [LANG: {}, ERR_VAL: {}]".format(lang, err_val))
#             # Only evaluate tweets with this language
#             kwargs['only_language'] = lang
#             acc = implementation(*args, **kwargs, error_value=err_val)
#             single_result = {lang: {str(err_val): acc}}
#             results[lang][str(err_val)] = acc
#             if output_file:
#                 _save_result(output_file, single_result)
#     return results



if __name__ == '__main__':
    arguments = _parse_arguments()
    utils._configure_logger(arguments['loglevel'])
    start_evaluation(arguments)
