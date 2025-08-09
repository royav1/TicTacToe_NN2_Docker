# backend/app/model.py

import torch
import torch.nn as nn
import torch.nn.functional as F

class TicTacToeNet(nn.Module):
    def __init__(self):
        super(TicTacToeNet, self).__init__()
        self.fc1 = nn.Linear(9, 36)  # 9 board cells → 36 neurons
        self.fc2 = nn.Linear(36, 36)
        self.output_layer = nn.Linear(36, 9)  # Output: one Q-value per cell

    def forward(self, x):
        """
        x: tensor of shape (batch_size, 9)
        returns: tensor of shape (batch_size, 9) with values in [0, 1]
        """
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return torch.sigmoid(self.output_layer(x))  # Q-values bounded in [0, 1]
