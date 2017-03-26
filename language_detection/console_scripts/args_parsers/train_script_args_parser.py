#/usr/bin/env python
#! -*- coding: utf-8 -*-

import argparse
import json
import logging

def parse_arguments(args):
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
        help="Chosen method (e.g. CavnarTrenkle)",
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

    return vars(parser.parse_args(args))
