// src/App.tsx

import React, { useEffect, useState } from 'react';
import Board from './components/Board';
import Score from './components/Score';
import axios from 'axios';

type Player = 1 | 2;
type GameStatus = 'playing' | 'won' | 'draw';

// ✅ Base API URL from .env.production or fallback
const API_BASE = process.env.REACT_APP_API_URL || '';

const App: React.FC = () => {
  const [board, setBoard] = useState<number[]>(Array(9).fill(0));
  const [currentPlayer, setCurrentPlayer] = useState<Player>(1);
  const [gameId, setGameId] = useState<string | null>(null);
  const [status, setStatus] = useState<GameStatus>('playing');
  const [playerChoice, setPlayerChoice] = useState<Player | null>(null);

  const [scoreX, setScoreX] = useState(0);
  const [scoreO, setScoreO] = useState(0);
  const [scoreDraws, setScoreDraws] = useState(0);

  useEffect(() => {
    if (playerChoice === null) return;

    const startGame = async () => {
      try {
        const res = await axios.post(`${API_BASE}/new_game`, { choice: playerChoice });
        const id = res.data.game_id;
        setGameId(id);
        setCurrentPlayer(res.data.current_player);

        console.log(`🧠 Player chose: ${playerChoice === 1 ? 'X' : 'O'}`);
        console.log('🎮 New game started with ID:', id);
        console.log('⬜ Initial board:', Array(9).fill(0));

        if (playerChoice === 2) {
          console.log('⏳ Waiting for AI first move...');
          await waitForBoardChange(Array(9).fill(0), id);
        }

        await fetchScore();
      } catch (err) {
        console.error('❌ Error starting game:', err);
      }
    };

    startGame();
  }, [playerChoice]);

  const waitForBoardChange = async (oldBoard: number[], gameId: string) => {
    let attempts = 0;
    const maxAttempts = 10;

    while (attempts < maxAttempts) {
      await new Promise((res) => setTimeout(res, 100));
      const res = await axios.get(`${API_BASE}/state?game_id=${gameId}`);
      const newBoard: number[] = res.data.board;
      const gameOver: boolean = res.data.game_over;

      console.log(`🔄 Poll #${attempts + 1}`);
      console.log('⬅️ Old board:', oldBoard);
      console.log('➡️ New board:', newBoard);
      console.log('🎯 Game over?', gameOver);

      const changed = newBoard.some((val: number, i: number) => val !== oldBoard[i]);
      if (changed || gameOver) {
        console.log('✅ Board changed or game ended — updating state.');
        setBoard(newBoard);
        setCurrentPlayer(res.data.current_player);
        setStatus(gameOver ? 'won' : 'playing');
        return;
      }

      attempts++;
    }

    console.warn('⚠️ Board did not change within max attempts');
  };

  const fetchScore = async () => {
    try {
      const res = await axios.get(`${API_BASE}/score`);
      setScoreX(res.data.score_x);
      setScoreO(res.data.score_o);
      setScoreDraws(res.data.score_draws);
      console.log('📊 Fetched score:', res.data);
    } catch (err) {
      console.error('❌ Error fetching score:', err);
    }
  };

  const handleClick = async (index: number) => {
    if (!gameId || board[index] !== 0 || status !== 'playing') return;

    try {
      console.log(`🖱️ Player clicked square ${index}`);
      const oldBoard = [...board];

      await axios.post(`${API_BASE}/move`, {
        game_id: gameId,
        move: index,
      });

      console.log('📤 Move sent to backend, waiting for board update...');
      await waitForBoardChange(oldBoard, gameId);
      await fetchScore();
    } catch (err) {
      console.error('❌ Error making move:', err);
    }
  };

  const handleNewGame = () => {
    setBoard(Array(9).fill(0));
    setStatus('playing');
    setGameId(null);
    setPlayerChoice(null); // Triggers side selection screen again
    console.log('➕ New game requested (score preserved)');
  };

  const handleReset = async () => {
    try {
      await axios.post(`${API_BASE}/reset_score`);
      setBoard(Array(9).fill(0));
      setStatus('playing');
      setGameId(null);
      setPlayerChoice(null);
      console.log('🔁 Game reset');
    } catch (err) {
      console.error('❌ Error resetting game:', err);
    }
  };

  const getTurnMessage = () => {
    if (status !== 'playing') return '';
    return currentPlayer === 1 ? "🔷 X's turn" : "🔶 O's turn";
  };

  const winnerMessage = status === 'won'
    ? board.includes(1) && board.includes(2)
      ? board.filter(x => x === 1).length === board.filter(x => x === 2).length
        ? "🤝 It's a draw"
        : currentPlayer === 1 ? '🔶 O wins!' : '🔷 X wins!'
      : ''
    : '';

  if (playerChoice === null) {
    return (
      <div style={{ textAlign: 'center', marginTop: '100px' }}>
        <h2>Choose your side:</h2>
        <button onClick={() => setPlayerChoice(1)} style={{ marginRight: '20px', padding: '10px 20px' }}>
          🔷 X (goes first)
        </button>
        <button onClick={() => setPlayerChoice(2)} style={{ padding: '10px 20px' }}>
          🔶 O (goes second)
        </button>
      </div>
    );
  }

  return (
    <div style={{ textAlign: 'center' }}>
      <h1>🎯 Tic-Tac-Toe Neural Net</h1>
      <h2>{status === 'playing' ? getTurnMessage() : winnerMessage}</h2>

      <Board board={board} onClick={handleClick} />
      <Score x={scoreX} o={scoreO} draws={scoreDraws} />

      <div style={{ marginTop: '20px' }}>
        <button onClick={handleNewGame} style={{ padding: '10px 20px', marginRight: '10px' }}>
          ➕ New Game
        </button>
        <button onClick={handleReset} style={{ padding: '10px 20px' }}>
          🔄 Reset Game
        </button>
      </div>
    </div>
  );
};

export default App;
