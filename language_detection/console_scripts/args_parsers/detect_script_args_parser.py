# #/usr/bin/env python
# #! -*- coding: utf-8 -*-

import argparse
import logging
import json

def parse_arguments(args):
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
        'model',
        help="Path to model input file (e.g. model.json)",
    )
    parser.add_argument(
        'text',
        help="Text to be translated",
    )
    parser.add_argument(
        '-i', '--implementation',
        help="Chosen method (e.g. CanvarTrenkle)",
        action="store", dest="implementation",
        default='CavnarTrenkleImpl'
    )
    parser.add_argument(
        '-o', '--output',
        help="Output results file in JSON (e.g. results.json)",
        action="store", dest="output_file",
        default=None
    )
    # This argument is a json object which will be mapped to dict
    parser.add_argument(
        '--predict-args',
        help="Arguments for the prediction method (JSON format)",
        action="store", dest="predict_args",
        type=json.loads
    )

    return vars(parser.parse_args(args))
