#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utility functions shared across the project."""

from collections import defaultdict
import json
import logging
import os
import pickle


def nested_defaultdict():
    """Allow to avoid Pickle errors with lambdas.

    This function is defined in order to avoid Pickle errors. E.g.:

    >>> AttributeError: Can't pickle local object # doctest: +SKIP
    ... 'TwitterCorpusReader.ngram_frequencies.<locals>.<lambda>'

    Returns:
        a `defaultdict` of integers.

    NOTE:
        Functions are pickled by name, not by code. Unpickling will only
        work if a function with the same name is present in in the same
        module. This is why pickling a lambda won't work: they have no
        individual names.

    """
    return defaultdict(int)

def merge_dictionaries_summing(first_dict, second_dict):
    """Merge two dictionaries summing values with the same key.

    Args:
        first_dict (defaultdict): A defaultdict dictionary.
        second_dict (defaultdict): A defaultdict dictionary.

    Returns:
        The enriched version of the first dictionary (it works in place). The
        returned object is of type `defaultdict`.

    Note:
        This only works only with two input objects for the moment. Later
        improvements could be made, if needed.

    """
    for k, v in second_dict.items():
        first_dict[k] += v
    return first_dict

def save_file(content, output_file_path):
    """Save content to output file.

    The implementation needed to save the specific file type is evaluated
    based on the filename extension.

    Args:
        content: The content that has to be stored
        output_file_path (str): The path to the output file where the content
            will be stored.

    """
    # Detect format from file name
    _, ext = os.path.splitext(output_file_path)
    save = _find_IO_function('save', ext)
    save(content, output_file_path)

def load_file(file_path):
    """Load content from file.

    The implementation needed to load the specific file type is evaluated
    based on the filename extension.

    Args:
        file_path (str): The path to the file to be loaded.

    Returns:
        The loaded file content.

    """
    # Detect format from file name
    _, ext = os.path.splitext(file_path)
    load = _find_IO_function('load', ext)
    return load(file_path)

def convert_unknown_arguments(dictionary):
    """Convert strings in dictionary to their proper typed values.

    Digits are automatically evaluated by json. We need to evaluate
    booleans.

    Args:
        dictionary (dict): The dictionary whose values need to be converted.

    >>> ex_dict = { 'flag': 'true', 'verbose': 'False' }
    >>> convert_unknown_arguments(ex_dict) == {'flag': True, 'verbose': False}
    True

    """
    if not dictionary:
        return
    for k, v in dictionary.items():
        # if v.isdigit():
        #     dictionary[k] = int(v)
        if _is_true(v):
            dictionary[k] = True
        elif _is_false(v):
            dictionary[k] = False
    return dictionary

# Private functions

def _save_result(result, output_file):
    res_list = []
    # If file does not exist or it is empty
    if not os.path.isfile(output_file) or os.path.getsize(output_file) == 0:
        res_list.append(result)
        with open(output_file, mode='w') as f:
            f.write(json.dumps(result, indent=2))
    else:
        with open(output_file, 'r') as feeds_json:
            previous_results = json.load(feeds_json)

        for k, v in result.items():
            if k in previous_results:
                previous_results[k].update(v)
            else:
                previous_results[k] = v

        with open(output_file, mode='w') as f:
            f.write(json.dumps(previous_results, indent=2))

def _save_as_pickle(content, output_file_path):
    logging.info("Writing pickle file: %s", output_file_path)
    pickle.dump(content, open(output_file_path, "wb"))

def _save_as_json(content, output_file_path, indent=2):
    logging.info("Writing json file: %s", output_file_path)
    with open(output_file_path, mode='w') as f:
        f.write(json.dumps(content, indent=indent))

def _save_generic_file(content, output_file_path):
    with open(output_file_path, 'w') as f:
        f.write(content)

def _find_IO_function(operation, extension):
    """If the extension is supported, return the related saving function for
    that specific file type. Otherwise, return reference to a generic saving
    function. Supported `operation` values: 'save', 'load'.

    """
    return _supported_formats_functions()[operation].get(
        extension, _save_generic_file)

def _load_json_file(input_file):
    with open(input_file) as in_file:
        result = json.load(in_file)
    return result

def _load_pickle_file(input_file):
    return pickle.load(open(input_file, "rb"))

def _configure_logger(loglevel):
    """Configure logging levels."""
    logging.basicConfig(
        format='%(levelname)s : %(message)s', level=logging.DEBUG)
    logging.basicConfig(level=loglevel)

# def _is_number(n):
#     try:
#         float(n)
#         return True
#     except ValueError:
#         return False

def _is_true(value):
    return value in ['True', 'true']

def _is_false(value):
    return value in ['False', 'false']

def _supported_formats_functions():
    return {
        'save': {
            '.json'  : _save_as_json,
            '.pickle': _save_as_pickle
        },
        'load': {
            '.json'  : _load_json_file,
            '.pickle': _load_pickle_file
        }
    }
