#!/usr/bin/env python3
from bothelper import read_board, up, down, left, right, botsetup, rotate_board, merge_count, print_board
import os
import torch


s = botsetup("smarter-example")


model = torch.load("dqn_bot.pth")
model.eval()


def choose_action(board):
    state = torch.tensor(board).flatten().float()  
    state = torch.unsqueeze(state, 0)  
    with torch.no_grad():
        q_values = model(state)
        action = torch.argmax(q_values).item()
    return action

counter = 0
while True:
    
    board, _ = read_board(s)


    best_action = choose_action(board)


    if best_action == 0:
        up(s)
    elif best_action == 1:
        down(s)
    elif best_action == 2:
        left(s)
    elif best_action == 3:
        right(s)


    if counter % 20 == 0: 
        os.system('clear')
        print(f"Step {counter} : ")
        print()
        print_board(board)
    
    counter += 1
