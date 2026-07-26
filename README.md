🧠 Tic-Tac-Toe Neural Net — Full Dockerized Application

![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![Reinforcement Learning](https://img.shields.io/badge/Reinforcement%20Learning-Q--Learning-blueviolet)


Play Tic-Tac-Toe against a Q-learning–trained neural network.
This repository contains the entire application (frontend + backend + trained model) packaged with Docker for easy deployment and local play.

## Live Demo

[Play the live demo](https://royav1-tictactoe-ai.netlify.app)

The Render free-tier backend may take a short time to wake after inactivity.

📌 The original frontend and backend repositories are now private.
This Docker repo is the main public version of the project.

🎮 Project Overview

This is a full-stack Tic-Tac-Toe game where a human can play against a neural network agent trained using Q-learning and self-play.
The system includes:

* 🧠 Reinforcement Learning Model (PyTorch)
* 🔙 Flask Backend API
* 🎨 React + TypeScript Frontend
* 🐳 Dockerized deployment (backend + frontend in one command)

🧠 AI Performance
The trained agent demonstrates strong performance:
* As X (first player):
Consistently defeats the Minimax optimal opponent.

* As O (second player):
Achieves near-perfect draw performance.
In almost all scenarios it forces a draw, but there exists a specific sequence of moves where it can still be defeated.
Most casual players will draw or lose when playing against it.

This reflects the natural limitations of Q-learning with function approximation: even highly trained agents may not achieve absolute perfect play, but still perform at a strong level.


🏗️ Architecture
```
┌──────────────┐      ┌────────────────┐      ┌────────────────────────┐
│   React UI   │ ---> │ Flask Backend  │ ---> │ Q-Learning Neural Net  │
│  (TypeScript)│ <--- │   REST API     │ <--- │   (PyTorch Model)      │
└──────────────┘      └────────────────┘      └────────────────────────┘
```

* Frontend handles game UI, polling for AI moves, score display, and state transitions.
* Backend handles game logic, AI inference, state persistence, and win/draw detection.
* Neural Net produces Q-values for available moves.


🧠 AI Training Summary

The AI was trained using Q-learning with a neural network (function approximation), allowing generalization across board states.

🔧 Training Configuration
* Episodes: 1.5 million self-play games
* Input: 9 cells (0 = empty, 1 = X, -1 = O)
* Network: Fully connected
  - Hidden layers: 36 neurons × 2
  - Output: Q-values for 9 possible moves
* Exploration: Epsilon-greedy with decay
* Rewards:
  - Win → 1
  - Draw → 0.9
  - Loss → 0

* Stabilization: Target network
* Penalty: Suboptimal opening moves (side cells)

📄 Logs & Model Files
* Training log: logs/qlearning_training_log.csv
* Minimax evaluation: logs/qmodel_vs_minimax_log.csv
* Saved model: models/tictactoe_model_qlearning.pt

🎮 Gameplay Features
* Play as X (first) or O (second)
* Neural network replies instantly to your moves
* Live scoreboard (X wins / O wins / Draws)
* Automatic AI first move if you choose O
* Polling system ensures board updates only when AI move is ready
* New Game keeps score, Reset clears everything

🔗 Backend API (Flask)
Method	Route	Description
POST	/new_game	Start game (1 = X, 2 = O). AI moves first if needed.
POST	/move	Send player's move (0–8).
GET	/state	Get current board, turn, result, and metadata.
GET	/score	Get scoreboard.
POST	/reset_score	Reset score + clear history.

🧩 Frontend (React + TypeScript)
Key UI features:
* User chooses who plays first
* Responsive 3×3 grid
* Board updates after AI response (polling mechanism)
* Shows win/draw status
* Reset button resets backend + frontend state


🐳 Run the Entire App With Docker
1️⃣ Clone the repository:
```bash
git clone https://github.com/<your-username>/TicTacToe_NN2_Docker.git
cd TicTacToe_NN2_Docker
```
2️⃣ Build & run both services (frontend + backend):
```bash
docker-compose up --build
```
3️⃣ Open your browser:
* Frontend: http://localhost:3000
* Backend API: http://localhost:5000

The docker-compose.yml file builds and runs both services on the same network.
4️⃣ Stop
```bash
Ctrl + C
docker-compose down
```
🔄 Rebuild without cache
```bash
docker-compose build --no-cache && docker-compose up
```

🌐 Deployment Status

The project runs locally via Docker Compose (frontend + backend).
Public portfolio deployment instructions are included below for Netlify and Render.

## Portfolio Deployment

The project is prepared for a split public deployment:

* React frontend on Netlify
* Flask backend on Render
* Local Docker Compose workflow preserved

Live URLs:

* Public frontend demo: `https://royav1-tictactoe-ai.netlify.app`
* Backend API: `https://tictactoe-nn2-docker.onrender.com`
* Health endpoint: `https://tictactoe-nn2-docker.onrender.com/health`

Required environment variables:

Frontend on Netlify:

```bash
REACT_APP_API_URL=https://tictactoe-nn2-docker.onrender.com
```

Backend on Render:

```bash
FRONTEND_ORIGINS=http://localhost:3000,https://royav1-tictactoe-ai.netlify.app
PORT=<provided by Render>
FLASK_DEBUG=false
```

Do not use `*` for production CORS. Set `FRONTEND_ORIGINS` to the exact local and production frontend origins, separated by commas.

Netlify settings:

* Base directory: `frontend`
* Build command: `npm run build`
* Publish directory: `build`
* Required environment variable: `REACT_APP_API_URL`

Render settings:

* Root directory: `backend`
* Runtime: Python
* Build command: `pip install -r requirements.txt`
* Start command: `gunicorn app:app`
* Health check path: `/health`
* Required environment variables: `FRONTEND_ORIGINS`, `FLASK_DEBUG`

The Gunicorn target is `app:app`: the Flask application object is named `app` and is exported from the `backend/app` package in `backend/app/__init__.py`.

Deployment order:

1. Create the Render backend service from the `backend` directory.
2. Set Render environment variables with `FRONTEND_ORIGINS=http://localhost:3000` until the Netlify URL exists.
3. Deploy Render and copy the Render service URL.
4. Create the Netlify frontend site from the `frontend` directory.
5. Set `REACT_APP_API_URL` in Netlify to the Render service URL.
6. Deploy Netlify and copy the Netlify live-demo URL.
7. Update Render `FRONTEND_ORIGINS` to include both `http://localhost:3000` and the Netlify origin.
8. Redeploy Render, then redeploy Netlify if its backend URL changed.

Local Docker usage remains unchanged:

```bash
docker compose up --build
```

Local URLs:

* Frontend: `http://localhost:3000`
* Backend API: `http://localhost:5000`
* Health check: `http://localhost:5000/health`

The tracked `frontend/.env.production` keeps the Docker Compose frontend build pointed at `http://localhost:5000`. Netlify should provide `REACT_APP_API_URL` through its environment settings instead of committing production URLs.

