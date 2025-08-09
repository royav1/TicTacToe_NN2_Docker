// src/components/Score.tsx
import React from 'react';

type ScoreProps = {
  x: number;
  o: number;
  draws: number;
};

const Score: React.FC<ScoreProps> = ({ x, o, draws }) => {
  return (
    <div style={{ marginTop: '20px' }}>
      <h3>🏁 Scoreboard</h3>
      <p>❌ X: {x}</p>
      <p>⭕ O: {o}</p>
      <p>🤝 Draws: {draws}</p>
    </div>
  );
};

export default Score;
