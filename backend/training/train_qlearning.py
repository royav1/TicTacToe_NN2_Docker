# backend/training/train_qlearning.py

import sys
import os
import csv

# Adjust Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque
from app.model import TicTacToeNet
from app.game import TicTacToe

# Hyperparameters
EPISODES = 1500000
DISCOUNT_FACTOR = 1.0
EPSILON_START = 0.6
EPSILON_DECAY = 0.1
EPSILON_DECAY_EVERY = EPISODES // 10  # now 150,000
LEARNING_RATE = 0.1
WIN_REWARD = 1.0
DRAW_REWARD = 0.9
LOSS_REWARD = 0.0
SIDE_MOVE_PENALTY = 0.95  # multiplier penalty if X starts with side move

# Output paths
MODEL_PATH = os.path.join("models", "tictactoe_model_qlearning.pt")
LOG_PATH = os.path.join("logs", "qlearning_training_log.csv")

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Initialize networks
policy_net = TicTacToeNet().to(device)
target_net = TicTacToeNet().to(device)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = optim.SGD(policy_net.parameters(), lr=LEARNING_RATE)
loss_fn = nn.MSELoss()

def board_to_tensor(board):
    return torch.tensor(board, dtype=torch.float32).to(device)

def get_q_values(board, model):
    return model(board_to_tensor(board))

def get_valid_moves(board):
    return [i for i, val in enumerate(board) if val == 0]

def choose_move(board, model, epsilon):
    if random.random() < epsilon:
        return random.choice(get_valid_moves(board))
    with torch.no_grad():
        q_values = get_q_values(board, model)
        valid_moves = get_valid_moves(board)
        q_values_np = q_values.cpu().numpy()
        valid_qs = [(i, q_values_np[i]) for i in valid_moves]
        return max(valid_qs, key=lambda x: x[1])[0]

def is_win(board, player):
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    for i,j,k in wins:
        if board[i] == board[j] == board[k] == player:
            return True
    return False

def is_draw(board):
    return all(cell != 0 for cell in board)

def get_game_result(board, learner_player):
    if is_win(board, learner_player):
        return WIN_REWARD
    elif is_win(board, -learner_player):
        return LOSS_REWARD
    elif is_draw(board):
        return DRAW_REWARD
    return None

def backpropagate(position, move_index, target_value):
    policy_net.train()
    optimizer.zero_grad()

    output = policy_net(board_to_tensor(position))
    target = output.clone().detach()
    target[move_index] = target_value

    for i in range(9):
        if position[i] != 0:
            target[i] = LOSS_REWARD

    loss = loss_fn(output, target)
    loss.backward()
    optimizer.step()
    return loss.item()

def play_training_episode(epsilon):
    game = TicTacToe()
    history = deque()
    losses = []

    learner_player = -1 if random.random() < 0.7 else 1
    first_move_index = None

    while not game.is_full() and game.check_winner() is None:
        board = game.board.copy()
        if game.current_player == learner_player:
            move = choose_move(board, policy_net, epsilon)
            if learner_player == 1 and len(history) == 0:
                first_move_index = move
            history.appendleft((board, move))
        else:
            move = random.choice(get_valid_moves(board))
        game.make_move(move)
        game.switch_player()

    result = get_game_result(game.board, learner_player)
    if result is None or not history:
        return 0.0

    # Apply side penalty if X started with a side move
    if learner_player == 1 and first_move_index in [1, 3, 5, 7]:
        result *= SIDE_MOVE_PENALTY

    next_board, last_move = history[0]
    loss = backpropagate(next_board, last_move, result)
    losses.append(loss)

    for (board, move) in list(history)[1:]:
        with torch.no_grad():
            next_qs = get_q_values(next_board, target_net)
            max_q = torch.max(next_qs).item()
        loss = backpropagate(board, move, DISCOUNT_FACTOR * max_q)
        losses.append(loss)
        next_board = board

    target_net.load_state_dict(policy_net.state_dict())
    return sum(losses) / len(losses) if losses else 0.0

def train():
    print("🚀 Starting Q-learning training...")
    epsilon = EPSILON_START

    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    with open(LOG_PATH, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["episode", "loss"])

        for episode in range(1, EPISODES + 1):
            loss = play_training_episode(epsilon)
            writer.writerow([episode, loss])

            if episode % EPSILON_DECAY_EVERY == 0:
                epsilon = max(0.0, epsilon - EPSILON_DECAY)
                print(f"📉 Epsilon decayed to {epsilon:.2f} at episode {episode}")

            if episode % 10000 == 0 or episode == 1:
                print(f"✅ Completed {episode}/{EPISODES} episodes")

    torch.save(policy_net.state_dict(), MODEL_PATH)
    print("\n✅ Q-learning training complete.")
    print(f"💾 Model saved to: {MODEL_PATH}")
    print(f"📄 Log saved to: {LOG_PATH}")

if __name__ == "__main__":
    train()
