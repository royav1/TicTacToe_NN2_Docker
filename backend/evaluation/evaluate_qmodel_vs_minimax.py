# backend/evaluation/evaluate_qmodel_vs_minimax.py

import os
import sys
import csv
import torch

# Ensure imports like app.model work
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

def get_minimax_move(game: TicTacToe):
    def minimax(board, player):
        winner = board.check_winner()
        if winner == 1:
            return 1
        elif winner == -1:
            return -1
        elif board.is_full():
            return 0

        scores = []
        for move in board.get_valid_move_indexes():
            new_board = board.play_move(move)
            score = minimax(new_board, -player)
            scores.append(score)

        return max(scores) if player == 1 else min(scores)

    best_score = float('-inf')
    best_move = None
    for move in game.get_valid_move_indexes():
        new_game = game.play_move(move)
        score = minimax(new_game, -game.current_player)
        if score > best_score:
            best_score = score
            best_move = move

    return game.play_move(best_move)

def evaluate(player_x, player_o, num_games=1000, label=""):
    results = {RESULT_X_WINS: 0, RESULT_O_WINS: 0, RESULT_DRAW: 0}

    for i in range(1, num_games + 1):
        final_state = play_game(player_x, player_o)
        result = final_state.get_game_result()
        results[result] += 1

        if i % 100 == 0:
            print(f"   ...{label} Progress: {i}/{num_games} games")

    return results

def save_results(results, log_path):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Matchup", "X Wins", "O Wins", "Draws"])
        for label, data in results.items():
            writer.writerow([
                label,
                data.get(RESULT_X_WINS, 0),
                data.get(RESULT_O_WINS, 0),
                data.get(RESULT_DRAW, 0),
            ])

def print_summary(results, label):
    total = sum(results.values())
    print(f"\n🎯 Evaluation Results for {label}:")
    print(f"✅ X Wins:   {results[RESULT_X_WINS]}")
    print(f"❌ O Wins:   {results[RESULT_O_WINS]}")
    print(f"🤝 Draws:    {results[RESULT_DRAW]}")
    print(f"\n🏁 Win Rate (X): {results[RESULT_X_WINS] / total:.2%}")
    print(f"🏁 Win Rate (O): {results[RESULT_O_WINS] / total:.2%}")
    print(f"🏁 Draw Rate:    {results[RESULT_DRAW] / total:.2%}")

if __name__ == "__main__":
    print("🤖 Evaluating Q-model (X) vs Minimax (O)...")
    results_1 = evaluate(player_x=get_q_move, player_o=get_minimax_move, label="Q (X) vs Minimax (O)")
    print_summary(results_1, "Q-model (X) vs Minimax (O)")

    print("\n🧠 Evaluating Minimax (X) vs Q-model (O)...")
    results_2 = evaluate(player_x=get_minimax_move, player_o=get_q_move, label="Minimax (X) vs Q (O)")
    print_summary(results_2, "Minimax (X) vs Q-model (O)")

    # Save both result sets
    all_results = {
        "Q-model (X) vs Minimax (O)": results_1,
        "Minimax (X) vs Q-model (O)": results_2,
    }
    save_results(all_results, os.path.join("logs", "qmodel_vs_minimax_log.csv"))
