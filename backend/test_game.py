from app.game import TicTacToe
from app.model import TicTacToeNet
import torch
import os

# Load trained model
MODEL_PATH = os.path.join("models", "tictactoe_model_qlearning.pt")
model = TicTacToeNet()
model.load_state_dict(torch.load(MODEL_PATH))
model.eval()

def board_to_tensor(board):
    return torch.tensor(board, dtype=torch.float32)

def get_model_move(game: TicTacToe):
    with torch.no_grad():
        q_values = model(board_to_tensor(game.board))
        valid_moves = game.get_valid_move_indexes()
        best_move = max(valid_moves, key=lambda i: q_values[i].item())
    return best_move

def main():
    game = TicTacToe()

    print("🎮 Tic Tac Toe — Human (X) vs Model (O)")
    print("You are X. Board positions are:")
    print(" 1 | 2 | 3\n---+---+---\n 4 | 5 | 6\n---+---+---\n 7 | 8 | 9\n")

    while True:
        game.print_board()

        if game.current_player == 1:
            # Human plays as X
            move = input("🧑 Your move (1–9): ")

            if not move.isdigit():
                print("❌ Please enter a number between 1 and 9.")
                continue

            move = int(move) - 1
            if move < 0 or move > 8:
                print("❌ Invalid move range.")
                continue
            if not game.make_move(move):
                print("❌ That cell is already taken.")
                continue
        else:
            # Model plays as O
            move = get_model_move(game)
            game.make_move(move)
            print(f"\n🤖 Model (O) played move: {move + 1}")

        result = game.get_game_result()
        if result is not None:
            game.print_board()
            if result == 1:
                print("🎉 You win!")
            elif result == -1:
                print("🏆 Model (O) wins!")
            else:
                print("🤝 It's a draw!")
            break

        game.switch_player()

if __name__ == "__main__":
    main()
