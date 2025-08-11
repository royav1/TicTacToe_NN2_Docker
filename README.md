## 🎮 Play Online:
You can try the deployed version here: [Play Tic-Tac-Toe Online](https://splendid-rugelach-3ff6a4.netlify.app/)

# to activate this (Dockerized) Tic-Tac_toe program do the following steps:

## 1) Clone the repo
git clone https://github.com/<your-username>/TicTacToe_NN2_Docker.git

cd TicTacToe_NN2_Docker

## 2) Build & run both services
docker-compose up --build

## this will generate:
1. Frontend: http://localhost:3000
2. Backend (API): http://localhost:5000
The docker-compose.yml file automatically builds both the backend and frontend from their respective Dockerfiles and runs them together on the same network.

## To stop:
In the same terminal (Ctrl+C), or in another terminal:
docker-compose down


### To rebuild without cache (if code changes):
docker-compose build --no-cache && docker-compose up
