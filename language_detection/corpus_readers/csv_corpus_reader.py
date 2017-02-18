#!/usr/bin/env python
#! -*- coding: utf-8 -*-

"""Corpus reader for CSV datasets."""

import csv
import sys

from .corpus_reader import CorpusReader

class CSVCorpusReader(CorpusReader):
    """Corpus Reader for CSV datasets."""

    def __init__(self, corpus_path, delimiter='|'):
        # TODO: Check if corpus path leads to an existing file (create property)
        self.corpus_path = corpus_path
        self.delimiter = delimiter

    def all_instances(self, limit=0):
        """
        Read the corpus and returns a generator for all instances. Each instance
        is a dictionary.

        """
        if not limit:
            limit = sys.maxsize
        with open(self.corpus_path, 'r') as input_file:
            input_data = csv.DictReader(input_file, delimiter=self.delimiter)
            # Skip header
            # if self._has_header(input_file):
            #     next(input_data)
            for i, row in enumerate(input_data):
                if i >= limit:
                    return
                yield row

    # Private methods #

    def _has_header(self, input_stream):
        """Find out if the file has a header."""
        sniffer = csv.Sniffer()
        has_header = sniffer.has_header(input_stream.readline())
        input_stream.seek(0) # Go back to beginning of file
        return has_header
