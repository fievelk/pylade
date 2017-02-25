#!/usr/bin/env python
# -*- codec: utf-8 -*-

"""Tests for CavnarTrenkleImpl."""

from unittest.mock import Mock

from language_detection.implementations import CavnarTrenkleImpl


class TestCavnarTrenkleImpl(object):
    """Tests for CavnarTrenkleImpl class."""

    def test_train(self):
        """Tests for the `train` method."""
        impl = CavnarTrenkleImpl()

        # Prepare arguments and mock objects
        labeled_instances = ['A list', 'of', 'labeled instances']
        lang_ngram_freqs = {
            'it': {'c': 1, 'i': 1, 'a': 1, 'o': 1, 'ci': 1, 'ia': 1, 'ao': 1,
                   'cia': 1, 'iao': 1, 'ciao': 1},
            'en': {'h': 1, 'e': 1, 'l': 2, 'o': 1, 'he': 1, 'el': 1, 'll': 1,
                   'lo': 1, 'hel': 1, 'ell': 1, 'llo': 1, 'hell': 1, 'ello': 1,
                   'hello': 1}
        }

        impl._languages_ngram_frequencies = Mock(
            return_value=lang_ngram_freqs)

        impl._compute_profile_from_frequencies = Mock(
            return_value='Profiles')

        # Call the tested method
        result = impl.train(labeled_instances, limit=10)

        # Assertions
        impl._languages_ngram_frequencies.assert_called_once_with(
            ['A list', 'of', 'labeled instances'])

        assert impl._compute_profile_from_frequencies.call_count == 2

        # Make sure the result is the full dict obtained by looping over
        # the languages and calling _compute_profile_from_frequencies
        assert result == {'en': 'Profiles', 'it': 'Profiles'}
