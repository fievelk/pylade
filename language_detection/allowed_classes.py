import logging

from language_detection.corpus_readers import TwitterCorpusReader
from language_detection.cavnar_trenkle_impl import CavnarTrenkleImpl

CORPUS_READERS = {TwitterCorpusReader}
IMPLEMENTATIONS = {CavnarTrenkleImpl}


def _find_class_in_set(class_name, class_set):
    try:
        return next(class_item
                    for class_item in class_set
                    if class_item.__name__ == class_name)
    except StopIteration as exception:
        logging.error(
            'The provided class name was not found in the available classes.')
        raise exception

def find_corpus_reader(class_name):
    return _find_class_in_set(class_name, CORPUS_READERS)

def find_implementation(class_name):
    return _find_class_in_set(class_name, IMPLEMENTATIONS)
