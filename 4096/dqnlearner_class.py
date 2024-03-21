import math
import random
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

class DQNLearner(nn.Module):
    def __init__(self, n_observations, n_actions):
        super(DQNLearner, self).__init__()
        
        self.fc1 = nn.Linear(n_observations, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, n_actions)

        
        self.optimizer = optim.Adam(self.parameters(), lr=0.001)

    def forward(self, x):
        
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
