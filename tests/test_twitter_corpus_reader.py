import os
import pytest

from language_detection.corpus_readers import TwitterCorpusReader

@pytest.fixture()
def twitter_corpus():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    corpus_path = current_dir + '/test_files/training_set_example.csv'
    return TwitterCorpusReader(corpus_path)

class TestTwitterCorpus:
    def test_available_languages(self, twitter_corpus):
        assert set(twitter_corpus.available_languages ) == set(['en', 'it'])
