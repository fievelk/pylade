#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for Implementation interface."""

from abc import ABC, abstractmethod


class Implementation(ABC):
    """
    Implementation interface. Forces a common structure among implementations
    of different NLP techniques. An implementation can be thought as a model
    (e.g.: Ngram model implementation, Cavnar-Trenkle model implementation).

    """

    @abstractmethod
    def train(self):
        """Train model."""
        pass

    @abstractmethod
    def evaluate(self):
        """Evaluate model."""
        pass

    @abstractmethod
    def predict_language(self):
        """Predict language."""
        pass
