#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict

from language_detection import utils

class TestUtils:
    def test_merge_dictionaries_summing(self):
        dict_a = {'a': 5, 'b': 0, 'c': 13}
        defaultdict_a = defaultdict(int)

        for k, v in dict_a.items():
            defaultdict_a[k] = v

        dict_b = {'a': 2, 'c': 1, 'd': 4}
        defaultdict_b = defaultdict(int)
        for k, v in dict_b.items():
            defaultdict_b[k] = v

        dict_expected = {'a': 7, 'b': 0, 'c': 14, 'd': 4}
        defaultdict_expected = defaultdict(int)
        for k, v in dict_expected.items():
            defaultdict_expected[k] = v

        assert utils.merge_dictionaries_summing(defaultdict_a, defaultdict_b) == defaultdict_expected

    def test_convert_unknown_arguments(self):
        dictionary = {"limit": 5000, "verbose": "True"}
        expected = {"limit": 5000, "verbose": True}

        assert utils.convert_unknown_arguments(dictionary) == expected

    # Use pytest tmpdir fixture to create temporary files for tests
    def test_save_file_json(self, tmpdir):
        filename_json = 'test_json.json'
        filepath = '/'.join([str(tmpdir), filename_json])
        utils.save_file('Test Content', filepath)

        assert filename_json in [path.basename for path in tmpdir.visit('*.json')]

    def test_save_file_pickle(self, tmpdir):
        filename_pickle = 'test_pickle.pickle'
        filepath = '/'.join([str(tmpdir), filename_pickle])
        utils.save_file('Test Content', filepath)

        # assert all(x in (path.basename for path in tmpdir.visit()) for x in [filename_json, filename_pickle])
        assert filename_pickle in [path.basename for path in tmpdir.visit('*.pickle')]
