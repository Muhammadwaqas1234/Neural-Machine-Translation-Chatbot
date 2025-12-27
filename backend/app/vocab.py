import spacy

spacy_en = spacy.load("en_core_web_sm")


def tokenize_en(text: str):
    return [tok.text.lower() for tok in spacy_en.tokenizer(text)]


def encode(sentence, vocab, tokenizer):
    tokens = tokenizer(sentence)
    return [vocab.get(tok, vocab["<unk>"]) for tok in tokens]
