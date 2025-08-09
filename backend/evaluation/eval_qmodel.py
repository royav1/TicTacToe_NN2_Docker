# backend/evaluation/eval_qmodel.py

import os
import sys
import torch
import random

# Ensure we can import from app.*
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.model import TicTacToeNet
from app.game import TicTacToe, play_game, RESULT_X_WINS, RESULT_O_WINS, RESULT_DRAW

# Load trained model
MODEL_PATH = os.path.join("models", "tictactoe_model_qlearning.pt")
model = TicTacToeNet()
model.load_state_dict(torch.load(MODEL_PATH))
model.eval()

def board_to_tensor(board):
    return torch.tensor(board, dtype=torch.float32)

def get_q_move(game: TicTacToe):
    with torch.no_grad():
        q_values = model(board_to_tensor(game.board))
        valid_moves = game.get_valid_move_indexes()
        best_move = max(valid_moves, key=lambda i: q_values[i].item())
    return game.play_move(best_move)

def random_move(game: TicTacToe):
    move = random.choice(game.get_valid_move_indexes())
    return game.play_move(move)

def evaluate(num_games=1000, player_x=None, player_o=None):
    results = {RESULT_X_WINS: 0, RESULT_O_WINS: 0, RESULT_DRAW: 0}

    for _ in range(num_games):
        final_state = play_game(player_x, player_o)
        result = final_state.get_game_result()
        results[result] += 1

    print("\n🎯 Evaluation Results:")
    print(f"✅ X Wins:   {results[RESULT_X_WINS]}")
    print(f"❌ O Wins:   {results[RESULT_O_WINS]}")
    print(f"🤝 Draws:    {results[RESULT_DRAW]}")
    total = sum(results.values())
    print(f"\n🏁 Win Rate (X): {results[RESULT_X_WINS] / total:.2%}")
    print(f"🏁 Win Rate (O): {results[RESULT_O_WINS] / total:.2%}")
    print(f"🏁 Draw Rate:    {results[RESULT_DRAW] / total:.2%}")

if __name__ == "__main__":
    print("🔍 Evaluating model vs Random player")
    evaluate(player_x=get_q_move, player_o=random_move)

    print("\n🔄 Evaluating model vs itself")
    evaluate(player_x=get_q_move, player_o=get_q_move)

    print("\n🔄 Evaluating Random vs model")
    evaluate(player_x=random_move, player_o=get_q_move)
