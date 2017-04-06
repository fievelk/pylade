"""Define classes that can be used as corpus readers and implementations.

Classes need to be whitelisted in order to sanitize command-line input and avoid
malicious or wrong code execution.
"""

import logging

from pylade.corpus_readers import TwitterCorpusReader
from pylade.implementations import CavnarTrenkleImpl

CORPUS_READERS = {TwitterCorpusReader}
IMPLEMENTATIONS = {CavnarTrenkleImpl}


def find_corpus_reader(class_name):
    """Return corpus reader class if whitelisted.

    Args:
        class_name (str): A specific corpus reader class name.

    Returns:
        The relative corpus reader class, if it is included in the set of
        allowed classes.

    """
    return _find_class_in_set(class_name, CORPUS_READERS)

def find_implementation(class_name):
    """Return implementation class if whitelisted.

    Args:
        class_name (str): A specific implementation class name.

    Returns:
        The relative implementation class, if it is included in the set of
        allowed classes.

    """
    return _find_class_in_set(class_name, IMPLEMENTATIONS)

# private functions #

def _find_class_in_set(class_name, class_set):
    try:
        return next(class_item
                    for class_item in class_set
                    if class_item.__name__ == class_name)
    except StopIteration as exception:
        logging.error(
            'The provided class name was not found in the available classes.')
        raise exception
