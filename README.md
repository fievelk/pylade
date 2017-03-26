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

For a quick use, simply give the following command from terminal:

```bash
langd "Put text here"
# en
```
Done!

If you want to get deeper and use some more advanced features, please keep reading. **Note:** you can obtain more information about each of the following commands using the `--help` flag.

### Train a model on a training set

```bash
langd_train \
    training_set.csv \
    --implementation CavnarTrenkleImpl \
    --corpus-reader TwitterCorpusReader \
    --output model.json \
    --train-args '{"limit": 5000, "verbose": "True"}'
```

### Evaluate a model on a test set

```bash
langd_eval \
    test_set.csv \
    -m model.json \
    --corpus-reader TwitterCorpusReader \
    --output results.json \
    --eval-args '{"languages": ["it", "de"], "error_values": 8000}'
```

### Detect language of a text using a trained model

```bash
langd \
    "Put text here" \
    -m model.json \
    --implementation CavnarTrenkleImpl \
    --output detected_language.txt \
    --predict-args '{"error_value": 8000}'
```

## Info

The default model (`data/model.json`) has been trained using `limit = 5000`. This value provides a good balance between computational performance and accuracy. Please note that this might change if you use your own data to train a new model.

## Tests

Give the command `tox` from the package root in order to perform tests.

Tests with `tox` require the following dependencies:

- `tox`
- `pytest`
