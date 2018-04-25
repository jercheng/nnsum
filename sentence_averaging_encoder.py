import torch
import torch.nn as nn
import torch.nn.functional as F


class SentenceAveragingEncoder(nn.Module):
    def __init__(self, embedding_size, dropout=0.0):
        super(SentenceAveragingEncoder, self).__init__()
        self.dropout_ = dropout
        self.output_size_ = embedding_size

    @property
    def size(self):
        return self.output_size_

    def forward(self, inputs, word_count, input_data):
        inputs_sum = inputs.sum(2)
        word_count = word_count.float().masked_fill(
            word_count.eq(0), 1).unsqueeze(2)
        inputs_mean = inputs_sum / word_count
        return inputs_mean

    @property
    def needs_sorted_sentences(self):
        return False