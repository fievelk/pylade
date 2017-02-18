import os
import pytest

from language_detection.corpus_readers import TwitterCorpusReader, CSVCorpusReader

@pytest.fixture()
def twitter_corpus():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    corpus_path = current_dir + '/test_files/training_set_example.csv'
    return TwitterCorpusReader(corpus_path, delimiter='|')

@pytest.fixture()
def csv_corpus():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    corpus_path = current_dir + '/test_files/training_set_example.csv'
    return CSVCorpusReader(corpus_path, delimiter='|')

class TestTwitterCorpusReader:
    def test_available_languages(self, twitter_corpus):
        assert set(twitter_corpus.available_languages) == set(['en', 'it'])

class TestCSVCorpusReader:
    def test_all_instances(self, csv_corpus):
        expected = {
            'id_str': '123456789012345671',
            'language': 'en',
            'text': 'This is an english example'
            }

        # Test result
        assert next(csv_corpus.all_instances()) == expected

        # Test limit parameter
        assert len(list(csv_corpus.all_instances(limit=2))) == 2
