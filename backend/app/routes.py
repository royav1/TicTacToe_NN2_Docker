from flask import request, jsonify
from app import app  # ✅ Use the app defined in __init__.py
from app.game import TicTacToe
from app.model import TicTacToeNet
import torch

games = {}  # game_id → dict with game state

# Score tracking
score_x = 0
score_o = 0
score_draws = 0

# Load model
model = TicTacToeNet()
model.load_state_dict(torch.load("models/tictactoe_model_qlearning.pt"))
model.eval()

def board_to_tensor(board):
    return torch.tensor(board, dtype=torch.float32)

def get_model_move(game: TicTacToe):
    with torch.no_grad():
        q_values = model(board_to_tensor(game.board))
        valid_moves = game.get_valid_move_indexes()
        print("\n🔎 Q-values for current board:")
        for i in range(9):
            print(f"Position {i}: {q_values[i].item():.4f}")
        best_move = max(valid_moves, key=lambda i: q_values[i].item())
    return best_move

def print_score():
    print(f"🏁 Current Score → X: {score_x} | O: {score_o} | Draws: {score_draws}")

@app.route("/new_game", methods=["POST"])
def new_game():
    data = request.json or {}
    choice = data.get("choice")

    if choice not in [1, 2]:
        return jsonify({"error": "You must choose 1 (play as X) or 2 (play as O)"}), 400

    # Return unfinished game if exists
    for gid, gdata in games.items():
        if gdata["result"] is None:
            print(f"\n⚠️ Resuming unfinished game (ID: {gid})")
            gdata["game"].print_board()
            return jsonify({
                "game_id": gid,
                "current_player": gdata["game"].current_player
            })

    game_id = str(len(games) + 1)
    game = TicTacToe()

    human_player = 1 if choice == 1 else -1
    model_player = -human_player

    print(f"\n🆕 New game started (ID: {game_id})")
    print(f"🧑 Human plays as {'X' if human_player == 1 else 'O'}")
    print(f"🤖 Model plays as {'X' if model_player == 1 else 'O'}")

    # If model is X, make the first move
    if game.current_player == model_player:
        model_move = get_model_move(game)
        game.make_move(model_move)
        print(f"\n🤖 Model (X) played first move: {model_move}")
        game.print_board()
        game.switch_player()
        first_move = model_move
    else:
        game.print_board()
        first_move = None

    games[game_id] = {
        "game": game,
        "last_move": first_move,
        "result": None,
        "moves_played": 1 if first_move is not None else 0,
        "human_player": human_player,
        "model_player": model_player
    }

    return jsonify({
        "game_id": game_id,
        "current_player": game.current_player
    })

@app.route("/move", methods=["POST"])
def make_move():
    global score_x, score_o, score_draws

    data = request.json
    game_id = data.get("game_id")
    move = data.get("move")

    if game_id not in games:
        return jsonify({"error": "Invalid game_id"}), 400

    game_data = games[game_id]
    game = game_data["game"]
    human_player = game_data["human_player"]
    model_player = game_data["model_player"]

    if move is None or not (0 <= move < 9) or game.board[move] != 0:
        return jsonify({"error": "Invalid move"}), 400

    game.make_move(move)
    game_data["last_move"] = move
    game_data["moves_played"] += 1
    print(f"\n🧑 Human played move: {move}")
    game.print_board()

    result = game.get_game_result()
    if result is not None:
        game_data["result"] = result
        print(f"\n🎯 Game {game_id} over. Result: {result}")
        if result == 1:
            score_x += 1
        elif result == -1:
            score_o += 1
        else:
            score_draws += 1
        print_score()
        return jsonify({
            "result": result,
            "next_player": None
        })

    game.switch_player()

    model_move = get_model_move(game)
    game.make_move(model_move)
    game_data["last_move"] = model_move
    game_data["moves_played"] += 1
    print(f"\n🤖 Model played move: {model_move}")
    game.print_board()

    result = game.get_game_result()
    if result is not None:
        game_data["result"] = result
        print(f"\n🎯 Game {game_id} over. Result: {result}")
        if result == 1:
            score_x += 1
        elif result == -1:
            score_o += 1
        else:
            score_draws += 1
        print_score()

    game.switch_player()
    return jsonify({
        "model_move": model_move,
        "result": result,
        "next_player": game.current_player
    })

@app.route("/state", methods=["GET"])
def get_state():
    game_id = request.args.get("game_id")
    if game_id not in games:
        return jsonify({"error": "Invalid game_id"}), 400

    game_data = games[game_id]
    game = game_data["game"]
    result = game_data["result"]

    winner_message = None
    if result == 1:
        winner_message = "X wins"
    elif result == -1:
        winner_message = "O wins"
    elif result == 0:
        winner_message = "Draw"

    print(f"\n📥 Requested state for game ID: {game_id}")
    game.print_board()
    if winner_message:
        print(f"🏆 {winner_message}")

    return jsonify({
        "board": game.board,
        "current_player": game.current_player,
        "last_move": game_data["last_move"],
        "moves_played": game_data["moves_played"],
        "game_over": result is not None,
        "result": result,
        "winner_message": winner_message
    })

@app.route("/score", methods=["GET"])
def get_score():
    print("\n📊 Score requested:")
    print_score()
    return jsonify({
        "score_x": score_x,
        "score_o": score_o,
        "score_draws": score_draws
    })

@app.route("/reset_score", methods=["POST"])
def reset_score():
    global score_x, score_o, score_draws
    score_x = 0
    score_o = 0
    score_draws = 0
    games.clear()
    print("\n🔄 Score and game history reset.")
    return jsonify({"message": "Score and game history reset."})
