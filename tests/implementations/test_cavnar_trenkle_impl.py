#!/usr/bin/env python
# -*- codec: utf-8 -*-

"""Tests for CavnarTrenkleImpl."""

from pylade.implementations import CavnarTrenkleImpl


class TestCavnarTrenkleImpl(object):
    """Tests for CavnarTrenkleImpl class."""

    def test_train(self):
        """Tests for the `train` method."""
        impl = CavnarTrenkleImpl()

        # Prepare arguments and mock objects
        labeled_instances = [
            {
                'id_str': '123456168300273664',
                'language': 'it',
                'text': 'Ciao'
            },
            {
                'id_str': '123456168300273665',
                'language': 'en',
                'text': 'hello'
            }]

        # Call the tested method without specifying limit value
        result = impl.train(labeled_instances, limit=None)
        expected = {
            'en': ['l', 'o', 'lo', 'llo', 'll', 'hello', 'hell', 'hel', 'he',
                   'h', 'ello', 'ell', 'el', 'e'],
            'it': ['o', 'iao', 'ia', 'i', 'ciao', 'cia', 'ci', 'c', 'ao', 'a']
        }

        assert result == expected

        # Call the tested method using a limit
        result = impl.train(labeled_instances, limit=8)
        expected = {
            'en': ['l', 'o', 'lo', 'llo', 'll', 'hello', 'hell', 'hel'],
            'it': ['o', 'iao', 'ia', 'i', 'ciao', 'cia', 'ci', 'c']
        }

        assert result == expected
