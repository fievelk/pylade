# Language Detection

## Requirements

- python 3.5
- `nltk`

## Installation

Download repository and install using pip (locally):

```bash
$ git clone git@github.com:fievelk/language-detection.git
$ cd language-detection
$ pip install .
```

## Usage

- Train a model on a training set

```bash
langd_train \
    training_set.csv \
    --implementation CavnarTrenkleImpl \
    --corpus-reader TwitterCorpusReader \
    --output model.json
```

- Evaluate a model on a test set

```bash
langd_eval \
    model.json \
    test_set.csv \
    --corpus-reader TwitterCorpusReader \
    --output results.json
    --languages it de \
    --error_values 6000 8000
```

- Detect language of a text, using a trained model

```bash
langd \
    model.json \
    "Put text here" \
    --implementation CavnarTrenkleImpl \
    --output detected_language.txt
```

## Tests

Use `pytest` from the package root in order to perform tests.
