#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for CorpusReader interface."""

from abc import ABC, abstractmethod


class CorpusReader(ABC):
    """Corpus reader interface. Forces a common structure among corpus readers."""

    @abstractmethod
    def all_instances(self, limit=0):
        """Return all instances of the dataset with their labels and properties."""
        pass
