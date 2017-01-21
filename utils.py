#!/usr/bin/env python
#! -*- coding: utf-8 -*-

from collections import defaultdict
from copy import deepcopy
import json
import logging
import os
import pickle

# from nltk.util import ngrams
from nltk.tokenize import wordpunct_tokenize # TODO: delete

from twitter_corpus_reader import TwitterCorpusReader
from cavnar_trenkle_impl import CavnarTrenkleImpl

CORPUS_READERS = {TwitterCorpusReader}
IMPLEMENTATIONS = {CavnarTrenkleImpl}

# Temporarily use lambdas to postpone function definition
# TODO: Move this constant somewhere else.
SUPPORTED_FORMATS_FUNCTIONS = {
    'save': {
        '.json'  : lambda : _save_as_json,
        '.pickle': lambda : _save_as_pickle
    }
}

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


def _merge_dictionaries_summing(first_dict, second_dict):
    """
    Merge two dictionaries summing values with the same key. Returns the enriched
    version of the first dictionary (so it works in place).
    Note: this works only with defaultdict.

    """
    for k, v in second_dict.items():
        first_dict[k] += v
    return first_dict
#
# # Results and evaluation
#
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

def _save_result(output_file, result):
    res_list = []
    if not os.path.isfile(output_file):
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
    save = _saving_function(ext)
    save(content, output_file_path)

def _saving_function(extension):
    """
    If the extension is supported, return the related saving function for that specific
    file type. Otherwise, return reference to a generic saving function.

    """
    return SUPPORTED_FORMATS_FUNCTIONS['save'].get(extension, _save_generic_file)

def _load_json_file(input_file):
    with open(input_file) as in_file:
        result = json.load(in_file)
    return result

def _load_pickle_file(input_file):
    return pickle.load(open(input_file, "rb"))

def load_file(input_file_path, file_format='json'):
    if file_format == 'json':
        return _load_json_file(input_file_path)
    elif file_format == 'pickle':
        return _load_pickle_file(input_file_path)

def _configure_logger(loglevel):
    """Configure logging levels."""
    logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.DEBUG)
    logging.basicConfig(level=loglevel)
