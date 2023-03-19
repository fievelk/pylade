# PyLaDe

[![Build Status](https://travis-ci.org/fievelk/pylade.svg?branch=master)](https://travis-ci.org/fievelk/pylade)

`pylade` is a lightweight language detection tool written in Python. The tool provides a ready-to-use command-line interface, along with more complex scaffolding for customized tasks.

The current version of `pylade` implements the *Cavnar-Trenkle N-Gram-based approach*. However, the tool can be further expanded with customized language identification implementations.

- [Installation](#installation)
- [Usage](#usage)
  - [Train a model on a training set](#train-a-model-on-a-training-set)
  - [Evaluate a model on a test set](#evaluate-a-model-on-a-test-set)
  - [Detect language of a text using a trained model](#detect-language-of-a-text-using-a-trained-model)
  - [Custom implementations and corpora](#custom-implementations-and-corpora)
- [Development](#development)
  - [Testing](#testing)
  - [Generating documentation with Sphinx](#generating-documentation-with-sphinx)
- [Notes](#notes)
- [References](#references)


## Installation

You can install using pip:

```bash
$ pip install pylade
```


## Usage

For a quick use, simply give the following command from terminal:

```console
$ pylade "Put text here"
en
```
Done!

If you want to get deeper and use some more advanced features, please keep reading. **Note:** you can obtain more information about each of the following commands using the `--help` flag.

### Train a model on a training set

```console
$ pylade_train \
    training_set.csv \
    --implementation CavnarTrenkleImpl \
    --corpus-reader TwitterCorpusReader \
    --output model.json \
    --train-args '{"limit": 5000, "verbose": "True"}'
```

`--train-args` is a dictionary of arguments to be passed to the `train()` method of the chosen implementation (`CavnarTrenkleImpl` in the example above). For an accurate description of the arguments please refer to the `train()` method docstring.

**NOTE**: to define a new training set, you can check the format of the file `tests/test_files/training_set_example.csv`.

### Evaluate a model on a test set

```console
$ pylade_eval \
    test_set.csv \
    --model model.json \
    --implementation CavnarTrenkleImpl \
    --corpus-reader TwitterCorpusReader \
    --output results.json \
    --eval-args '{"languages": ["it", "de"], "error_values": 8000}'
```

`--eval-args` is a dictionary of arguments to be passed to the `evaluate()` method of the chosen implementation (`CavnarTrenkleImpl` in the example above). For an accurate description of the arguments please refer to the `evaluate()` method docstring.

### Detect language of a text using a trained model

```console
$ pylade \
    "Put text here" \
    --model model.json \
    --implementation CavnarTrenkleImpl \
    --output detected_language.txt \
    --predict-args '{"error_value": 8000}'
```

`--predict-args` is a dictionary of arguments to be passed to the `predict_language()` method of the chosen implementation (`CavnarTrenkleImpl` in the example above). For an accurate description of the arguments please refer to the `predict_language()` method docstring.

### Custom implementations and corpora

Different language detection approaches can be implemented creating new classes that inherit from the `Implementation` class. This class should be considered as an interface whose methods are meant to be implemented by the inheriting class.

Customized corpus readers can be created the same way, inheriting from the `CorpusReader` interface instead.


## Development

### Testing

You can install development requirements using Poetry (`poetry install`). This will also install requirements needed for testing.

To run tests, just run `tox` from the package root folder.

### Generating documentation with Sphinx

PyLaDe's documentation is generated using Sphinx. If you want to update the docs, you can install the necessary dependencies with Poetry:
```console
$ poetry install --with docs
```
Documentation files are automatically generated from code docstrings. To rebuild the documentation to take changes into consideration, just run the following:
```console
$ cd docs
$ make html
```

## Notes

The default model (`data/model.json`) has been trained using `limit = 5000`. This value provides a good balance between computational performance and accuracy. Please note that this might change if you use your own data to train a new model.


## References

- Cavnar, William B., and John M. Trenkle. "N-gram-based text categorization." *Ann Arbor MI* 48113.2 (1994): 161-175.
