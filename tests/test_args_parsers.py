#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for command-line scripts argument parsers."""

from pylade.console_scripts.args_parsers import (
    detect_script_args_parser,
    evaluate_script_args_parser,
    train_script_args_parser
    )

class TestScriptArgumentParsers(object):
    """Tests for argument parsers used by command-line scripts."""

    def test_detect_arguments_parser(self):
        """Test argument parser for detect.py script."""

        args = [
            'This is an english text',
            '-m', 'pylade/data/model.json'
            ]

        expected = {
            'output_file': None,
            'model': 'pylade/data/model.json',
            'predict_args': None,
            'text': 'This is an english text',
            'implementation': 'CavnarTrenkleImpl',
            'loglevel': 30
        }

        assert detect_script_args_parser.parse_arguments(args) == expected

    def test_evaluate_arguments_parser(self):
        """Test argument parser for evaluate.py script."""

        args = [
            '/path/to/test_set.csv',
            '-m', 'path/to/pylade/data/model.json',
            '--corpus-reader', 'SomeCorpusReader',
            '--output', 'my_results.json',
            '--eval-args', '{"languages": ["it", "de"], "error_values": 8000}'
            ]

        expected = {
            'model': 'path/to/pylade/data/model.json',
            'test-data': '/path/to/test_set.csv',
            'corpus_reader_class': 'SomeCorpusReader',
            'results_output_file': 'my_results.json',
            'implementation': 'CavnarTrenkleImpl',
            'eval_args': {"languages": ["it", "de"], "error_values": 8000},
            'loglevel': 30
        }

        assert evaluate_script_args_parser.parse_arguments(args) == expected

    def test_train_arguments_parser(self):
        """Test argument parser for evaluate.py script."""

        args = [
            '/path/to/training_set.csv',
            ]

        args = [
            '/path/to/training_set.csv',
            '--implementation', 'SomeCustomImplementation',
            '--corpus-reader', 'SomeCorpusReader',
            '--output', 'path/to/pylade/data/model.json',
            '--train-args', '{"limit": 5000, "verbose": "True"}'
            ]

        expected = {
            'training-data': '/path/to/training_set.csv',
            'implementation': 'SomeCustomImplementation',
            'corpus_reader_class': 'SomeCorpusReader',
            'model_output_file': 'path/to/pylade/data/model.json',
            'train_args': {'limit': 5000, 'verbose': 'True'},
            'loglevel': 30
        }

        assert train_script_args_parser.parse_arguments(args) == expected
