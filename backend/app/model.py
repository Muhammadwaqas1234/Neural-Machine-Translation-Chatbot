import torch
import torch.nn as nn
import random


class Encoder(nn.Module):
    def __init__(self, vocab_size, emb_dim, hid_dim, n_layers):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, emb_dim)
        self.rnn = nn.LSTM(
            emb_dim,
            hid_dim,
            n_layers,
            bidirectional=True,
            batch_first=True
        )

    def forward(self, src):
        embedded = self.embedding(src)
        outputs, (hidden, cell) = self.rnn(embedded)
        return outputs, hidden, cell


class Attention(nn.Module):
    def __init__(self, hid_dim):
        super().__init__()
        self.attn = nn.Linear(hid_dim * 3, hid_dim)
        self.v = nn.Linear(hid_dim, 1, bias=False)

    def forward(self, hidden, encoder_outputs):
        src_len = encoder_outputs.shape[1]
        hidden = hidden.unsqueeze(1).repeat(1, src_len, 1)
        energy = torch.tanh(
            self.attn(torch.cat((hidden, encoder_outputs), dim=2))
        )
        attention = self.v(energy).squeeze(2)
        return torch.softmax(attention, dim=1)


class Decoder(nn.Module):
    def __init__(self, vocab_size, emb_dim, hid_dim, attention):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, emb_dim)
        self.attention = attention
        self.rnn = nn.LSTM(
            hid_dim * 2 + emb_dim,
            hid_dim,
            batch_first=True
        )
        self.fc = nn.Linear(hid_dim * 3, vocab_size)

    def forward(self, input, hidden, cell, encoder_outputs):
        input = input.unsqueeze(1)
        embedded = self.embedding(input)

        attn_weights = self.attention(hidden[-1], encoder_outputs)
        context = torch.bmm(attn_weights.unsqueeze(1), encoder_outputs)

        rnn_input = torch.cat((embedded, context), dim=2)
        output, (hidden, cell) = self.rnn(
            rnn_input,
            (hidden[:1], cell[:1])
        )

        output = self.fc(
            torch.cat((output.squeeze(1), context.squeeze(1)), dim=1)
        )

        return output, hidden, cell


class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
