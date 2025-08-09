# 🧠 Tic-Tac-Toe Neural Net — Backend
## This is the backend portion of a full-stack Tic-Tac-Toe game powered by a Q-learning-trained neural network agent. The backend handles:

## Game logic:
Neural network inference
Game state persistence
RESTful API endpoints for the frontend

## 🧠 AI Training Overview:
The AI is trained using Q-learning with a neural network instead of tabular Q-learning. This allows generalization across similar board states.

## 🔧 Training Details:
Episodes: 1.5 million games of self-play
Architecture: Fully connected neural network (TicTacToeNet)
Input: 9 cells (values: 0 = empty, 1 = X, -1 = O)
Hidden layers: Two layers of 36 neurons each
Output: Q-values for 9 possible moves

## Training strategy:
Epsilon-greedy exploration (with decay)
Penalized suboptimal first moves (e.g. side cells)
Target network for stability

## Rewards:
Win: 1
Draw: 0.9
Loss: 0

## Logs:
Training progress: logs/qlearning_training_log.csv
Minimax evaluation: logs/qmodel_vs_minimax_log.csv
Model output: Final model is saved to models/tictactoe_model_qlearning.pt


## Routes:
Method	Route	Description
POST	/new_game	Starts a new game. Accepts a choice (1 = human as X, 2 = human as O). Returns a game_id. If AI goes first, it makes a move automatically.
POST	/move	    Sends the human’s move. Requires game_id and move index (0–8).
GET	    /state	    Retrieves the current board, current player, game status (win/draw), and metadata. Requires game_id.
GET	    /score	    Returns the running total of X wins, O wins, and draws.
POST	/reset_score	Resets the score and clears all active and past games. Used by the frontend’s reset button.
