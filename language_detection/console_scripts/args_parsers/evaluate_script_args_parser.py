# #/usr/bin/env python
# #! -*- coding: utf-8 -*-

import argparse
import logging
import json

def parse_arguments(args):
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

    return vars(parser.parse_args(args))
