"""Translation inference.

The Seq2Seq checkpoint is loaded lazily on first request and cached.
If PyTorch or the checkpoint file is unavailable, the translator
reports itself unavailable and the API returns 503 instead of the
whole application crashing at import time.

The trained checkpoint is not committed to the repository (size).
Train it with the notebook at the repo root and place it at
``MODEL_PATH`` (default: backend/app/nmt_seq2seq_attention.pth).
"""

import logging
import os
import threading

logger = logging.getLogger(__name__)

MODEL_PATH = os.getenv("MODEL_PATH", os.path.join(os.path.dirname(__file__), "nmt_seq2seq_attention.pth"))
MAX_LEN = int(os.getenv("MAX_LEN", 30))

_lock = threading.Lock()
_state = None
_load_error = None


class TranslatorUnavailable(RuntimeError):
    pass


def _load():
    global _state, _load_error
    if _state is not None or _load_error is not None:
        return
    with _lock:
        if _state is not None or _load_error is not None:
            return
        try:
            import torch

            from app.model import Attention, Decoder, Encoder, Seq2Seq

            if not os.path.exists(MODEL_PATH):
                raise FileNotFoundError(
                    f"Checkpoint not found at {MODEL_PATH}. Train the model with "
                    "the notebook and place the .pth file there (see README)."
                )

            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            checkpoint = torch.load(MODEL_PATH, map_location=device)

            eng_vocab = checkpoint["eng_vocab"]
            fr_vocab = checkpoint["fr_vocab"]

            encoder = Encoder(len(eng_vocab), 256, 512, 2)
            attention = Attention(512)
            decoder = Decoder(len(fr_vocab), 256, 512, attention)
            model = Seq2Seq(encoder, decoder).to(device)

            model.encoder.load_state_dict(checkpoint["encoder_state_dict"])
            model.decoder.load_state_dict(checkpoint["decoder_state_dict"])
            model.eval()

            _state = {
                "torch": torch,
                "model": model,
                "device": device,
                "eng_vocab": eng_vocab,
                "fr_vocab": fr_vocab,
                "inv_fr_vocab": {v: k for k, v in fr_vocab.items()},
            }
            logger.info("NMT checkpoint loaded on %s", device)
        except Exception as exc:
            _load_error = str(exc)
            logger.exception("Failed to load translation model")


def is_available() -> bool:
    _load()
    return _state is not None


def load_error():
    return _load_error


def translate(sentence: str, max_len: int = MAX_LEN) -> str:
    _load()
    if _state is None:
        raise TranslatorUnavailable(_load_error or "Model not loaded")

    from app.vocab import encode, tokenize_en

    torch = _state["torch"]
    model = _state["model"]
    device = _state["device"]
    eng_vocab = _state["eng_vocab"]
    fr_vocab = _state["fr_vocab"]
    inv_fr_vocab = _state["inv_fr_vocab"]

    tokens = (
        [eng_vocab["<sos>"]]
        + encode(sentence, eng_vocab, tokenize_en)
        + [eng_vocab["<eos>"]]
    )
    src = torch.tensor(tokens).unsqueeze(0).to(device)

    with torch.no_grad():
        encoder_outputs, hidden, cell = model.encoder(src)

    input_token = torch.tensor([fr_vocab["<sos>"]]).to(device)
    result = []

    for _ in range(max_len):
        with torch.no_grad():
            output, hidden, cell = model.decoder(
                input_token, hidden, cell, encoder_outputs
            )
        pred = output.argmax(1).item()
        if pred == fr_vocab["<eos>"]:
            break
        result.append(inv_fr_vocab[pred])
        input_token = torch.tensor([pred]).to(device)

    return " ".join(result)
