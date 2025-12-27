import torch
from app.model import Encoder, Decoder, Attention, Seq2Seq
from app.vocab import tokenize_en, encode

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load checkpoint
checkpoint = torch.load("app/nmt_seq2seq_attention.pth", map_location=device)

eng_vocab = checkpoint["eng_vocab"]
fr_vocab = checkpoint["fr_vocab"]

# Build model
encoder = Encoder(len(eng_vocab), 256, 512, 2)
attention = Attention(512)
decoder = Decoder(len(fr_vocab), 256, 512, attention)

model = Seq2Seq(encoder, decoder).to(device)

model.encoder.load_state_dict(checkpoint["encoder_state_dict"])
model.decoder.load_state_dict(checkpoint["decoder_state_dict"])

model.eval()

# Inverse vocab for decoding
inv_fr_vocab = {v: k for k, v in fr_vocab.items()}


def translate(sentence: str, max_len: int = 20):
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
