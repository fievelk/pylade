#!/usr/bin/env python
#! -*- coding: utf-8 -*-

from collections import defaultdict
import json
import logging
import os
import pickle

# from nltk.util import ngrams
from nltk.tokenize import wordpunct_tokenize # TODO: delete

from language_detection.corpus_readers.twitter_corpus_reader import TwitterCorpusReader
from language_detection.cavnar_trenkle_impl import CavnarTrenkleImpl

CORPUS_READERS = {TwitterCorpusReader}
IMPLEMENTATIONS = {CavnarTrenkleImpl}

def _find_class_in_set(class_name, class_set):
    try:
        return next(class_item for class_item in class_set if class_item.__name__ == class_name )
    except StopIteration as exception:
        logging.error('The provided class name was not found in the available classes.')
        raise exception

def find_corpus_reader(class_name):
    return _find_class_in_set(class_name, CORPUS_READERS)

def find_implementation(class_name):
    return _find_class_in_set(class_name, IMPLEMENTATIONS)

def _nested_defaultdict():
    """
    Note: this function is defined in order to avoid Pickle errors:
        AttributeError: Can't pickle local object
        'TwitterCorpusReader.ngram_frequencies.<locals>.<lambda>'
    Explanation:
        Functions are pickled by name, not by code. Unpickling will only work
        if a function with the same name is present in in the same module.
        This is why pickling a lambda won't work: they have no individual names.

    """
    return defaultdict(int)

def merge_dictionaries_summing(first_dict, second_dict):
    """
    Merge two dictionaries summing values with the same key. Returns the enriched
    version of the first dictionary (so it works in place).
    Note: this works only with defaultdict.

    """
    for k, v in second_dict.items():
        first_dict[k] += v
    return first_dict

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

        for k,v in result.items():
            if k in previous_results:
                previous_results[k].update(v)
            else:
                previous_results[k] = v

        with open(output_file, mode='w') as f:
            f.write(json.dumps(previous_results, indent=2))

def _save_as_pickle(content, output_file_path):
    logging.info("Writing pickle file: {}".format(output_file_path))
    pickle.dump(content, open(output_file_path, "wb"))

def _save_as_json(content, output_file_path, indent=2):
    logging.info("Writing json file: {}".format(output_file_path))
    with open(output_file_path, mode='w') as f:
        f.write(json.dumps(content, indent=2))

def _save_generic_file(content, output_file_path):
    with open(output_file_path, 'w') as f:
        f.write(content)

def save_file(content, output_file_path):
    """
    Save content to output file.

    """
    # Detect format from file name
    _, ext = os.path.splitext(output_file_path)
    save = _find_IO_function('save', ext)
    save(content, output_file_path)

def _find_IO_function(operation, extension):
    """
    If the extension is supported, return the related saving function for that specific
    file type. Otherwise, return reference to a generic saving function.
    Supported `operation` values: 'save', 'load'.

    """
    return SUPPORTED_FORMATS_FUNCTIONS[operation].get(extension, _save_generic_file)

def _load_json_file(input_file):
    with open(input_file) as in_file:
        result = json.load(in_file)
    return result

def _load_pickle_file(input_file):
    return pickle.load(open(input_file, "rb"))

def load_file(file_path):
    # Detect format from file name
    _, ext = os.path.splitext(file_path)
    load = _find_IO_function('load', ext)
    return load(file_path)

def _configure_logger(loglevel):
    """Configure logging levels."""
    logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.DEBUG)
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

def convert_unknown_arguments(dictionary):
    """Digits are automatically evaluated by json. We need to evaluate booleans."""
    if not dictionary:
        return
    for k,v in dictionary.items():
        # if v.isdigit():
        #     dictionary[k] = int(v)
        if _is_true(v):
            dictionary[k] = True
        elif _is_false(v):
            dictionary[k] = False
    return dictionary

# TODO: Move this constant somewhere else.
SUPPORTED_FORMATS_FUNCTIONS = {
    'save': {
        '.json'  : _save_as_json,
        '.pickle': _save_as_pickle
    },
    'load': {
        '.json'  : _load_json_file,
        '.pickle': _load_pickle_file
    }
}
