#!/usr/bin/env python3
import random
import torch
from bothelper import read_board, up, down, left, right, botsetup, rotate_board, merge_count, print_board
from dqnlearner_class import DQNLearner

s = botsetup("dqn-bot")

dqn_bot = DQNLearner(n_observations=16, n_actions=4)  

num_episodes = 1000

epsilon = 1.0  
epsilon_min = 0.01  
epsilon_decay = 0.995  
gamma = 0.99  

for episode in range(num_episodes):
    print(f"Episode {episode}")
    board, score = read_board(s)
    state = torch.tensor(board).flatten().float()  
    state = torch.unsqueeze(state, 0)  

    done = False
    total_reward = 0

    while not done:
        if random.random() < epsilon:
            action = random.randint(0, 3)  
        else:
            q_values = dqn_bot(state)
            action = torch.argmax(q_values).item()

        if action == 0:
            up(s)
        elif action == 1:
            down(s)
        elif action == 2:
            left(s)
        elif action == 3:
            right(s)

        next_board, reward = read_board(s)
        next_state = torch.tensor(next_board).flatten().float()
        next_state = torch.unsqueeze(next_state, 0)

        total_reward += reward

        done = "FIN" in next_board

        if not done:
            
            q_next = dqn_bot(next_state)
            td_target = reward + gamma * torch.max(q_next)
        else:
            td_target = torch.tensor(reward)

        
        q_values = dqn_bot(state)
        td_error = td_target - q_values[0][action]

        
        dqn_bot.optimizer.zero_grad()
        loss = torch.mean(torch.square(td_error)) 
        loss.backward()
        dqn_bot.optimizer.step()

        
        state = next_state

    
    if epsilon > epsilon_min:
        epsilon *= epsilon_decay

    print(f"Episode {episode + 1}/{num_episodes}, Total Reward: {total_reward}")

torch.save(dqn_bot.state_dict(), "dqn_bot.pth")
