# Language Detection

## Requirements

- python 3.5
- `nltk`

## Usage

- Train a model on a training set

```bash
python train.py \
    training_set.csv \
    --implementation CavnarTrenkleImpl \
    --corpus-reader TwitterCorpusReader \
    --output model.json
```

- Evaluate a model on a test set

```bash
python evaluate.py \
    model.json \
    test_set.csv \
    --corpus-reader TwitterCorpusReader \
    --output results.json
    --languages it de \
    --error_values 6000 8000
```

- Detect language of a text, using a trained model

```bash
python detect.py
    model.json \
    "Put text here" \
    --implementation CavnarTrenkleImpl \
    --output detected_language.txt
```
