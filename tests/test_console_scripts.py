#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for command-line scripts."""

from language_detection.console_scripts import detect

class TestDetectScript(object):
    """Tests for detect.py script."""

    def test_detect_script(self):
        """Test detect script."""

        args = {
            'output_file': None,
            'model': 'output/model.pickle',
            'predict_args': None,
            'text': 'This is an english text',
            'implementation': 'CavnarTrenkleImpl',
            'loglevel': 30
        }

        assert detect.start_detection(args) == 'en'
