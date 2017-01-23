# #/usr/bin/env python
# #! -*- coding: utf-8 -*-

import argparse
import logging

from language_detection import utils

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

    return vars(parser.parse_args())

def start_detection(arguments):
    model_file = arguments['model']
    model = utils.load_file(model_file)
    text = arguments['text']
    output_file = arguments['output_file']
    implementation = utils.find_implementation(arguments['implementation'])
    # implementation = implementation(model=model, error_value=error_value) # TODO: implement this kind of constructor

    # NOTE: `error_value` should be explicitly passed from command-line. It should
    # in general be equal to the value used for testing.
    logging.info("Identifying language...")
    results = implementation().predict_language(text, model, error_value=8000)
    if output_file:
        utils.save_file(results, output_file)

    print(results)

def main():
    arguments = _parse_arguments()
    utils._configure_logger(arguments['loglevel'])
    start_detection(arguments)

if __name__ == '__main__':
    main()
