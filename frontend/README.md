# 🎯 Tic-Tac-Toe Neural Net — Frontend
## This is the React + TypeScript frontend for the Tic-Tac-Toe Neural Network project. It allows a human player to play against a Q-learning-trained AI through a simple, responsive interface.

## 🧩 Features
🎮 Play as either X (first) or O (second)
🧠 Plays against a neural network trained via Q-learning
🔄 Start new games while preserving score
❌ Reset button clears score and game history
📊 Live display of win / loss / draw statistics
✅ Board updates after each move, waiting for the AI’s response

## 🔗 Backend Integration
The frontend communicates with the Flask backend using HTTP requests.
Ensure the backend is running at http://localhost:5000.

## 🚀 Available Routes (used by the frontend)
Method	Route	Purpose
POST	/new_game	Starts a new game with player choice (1 = X, 2 = O).
POST	/move	Sends the player’s move to the backend.
GET	    /state	Fetches current game board, turn, and result.
GET	    /score	Gets the current X / O / Draw scores.
POST	/reset_score	Fully resets game and score state.

## How to Run:
1. npm install
2. npm start
3. Open http://localhost:3000 in your browser.

## 🧠 Gameplay Flow
1. Player is prompted to choose X or O.
2. If AI goes first (you chose O), it plays immediately.
3. The board updates after each move using polling (max 10 attempts).
4. Game status and winner are displayed.
5. Use "New Game" to start a new round (score is kept).
6. Use "Reset Game" to clear score and restart completely.