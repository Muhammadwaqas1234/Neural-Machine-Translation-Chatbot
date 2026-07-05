"""Tokenization utilities (spaCy English pipeline, lazy-loaded)."""

_spacy_en = None


def _get_tokenizer():
    global _spacy_en
    if _spacy_en is None:
        import spacy

        _spacy_en = spacy.load("en_core_web_sm")
    return _spacy_en


def tokenize_en(text: str):
    return [tok.text.lower() for tok in _get_tokenizer().tokenizer(text)]


def encode(sentence, vocab, tokenizer):
    tokens = tokenizer(sentence)
    return [vocab.get(tok, vocab["<unk>"]) for tok in tokens]
