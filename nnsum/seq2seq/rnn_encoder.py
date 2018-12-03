import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence


class RNNEncoder(nn.Module):
    def __init__(self, embedding_context, hidden_dim=512, num_layers=1, 
                 rnn_cell="GRU"):
        super(RNNEncoder, self).__init__()

        rnn_cell = rnn_cell.upper()
        assert rnn_cell in ["LSTM", "GRU", "RNN"]
        assert hidden_dim > 0
        assert num_layers > 0

        self._emb_ctx = embedding_context        
        self._rnn = getattr(nn, rnn_cell)(
            embedding_context.output_size, hidden_dim, num_layers=num_layers)
           
    @property
    def rnn(self):
        return self._rnn

    @property
    def embedding_context(self):
        return self._emb_ctx

    def forward(self, features, lengths):
        emb = self._emb_ctx(features)        
        emb_packed = pack_padded_sequence(emb, lengths)
        context_packed, state = self._rnn(emb_packed)
        context, _ = pad_packed_sequence(context_packed, batch_first=True)
        return context, state