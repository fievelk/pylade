# #/usr/bin/env python
# #! -*- coding: utf-8 -*-

import logging
import sys

from language_detection import utils
from language_detection import allowed_classes
from language_detection.console_scripts import detect_script_args_parser

def start_detection(arguments):
    model_file = arguments['model']
    model = utils.load_file(model_file)
    text = arguments['text']
    output_file = arguments['output_file']
    implementation = allowed_classes.find_implementation(arguments['implementation'])
    # implementation = implementation(model=model, error_value=error_value) # TODO: implement this kind of constructor

    # NOTE: `error_value` should in general be equal to the value used for testing.
    prediction_arguments = utils.convert_unknown_arguments(arguments['predict_args']) or {}

    logging.info("Identifying language...")
    results = implementation().predict_language(text, model, **prediction_arguments)
    if output_file:
        utils.save_file(results, output_file)

    print(results)
    return results

def main():
    arguments = detect_script_args_parser.parse_arguments(sys.argv[1:])
    utils._configure_logger(arguments['loglevel'])
    start_detection(arguments)

if __name__ == '__main__':
    main()
