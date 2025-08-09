import React from 'react';

type StatusProps = {
  currentPlayer: 1 | 2;
  winnerMessage: string | null;
  isPlaying: boolean;
};

const Status: React.FC<StatusProps> = ({ currentPlayer, winnerMessage, isPlaying }) => {
  const getMessage = () => {
    if (!isPlaying && winnerMessage) return `🏆 ${winnerMessage}`;
    return currentPlayer === 1 ? "🔷 X's turn" : "🔶 O's turn";
  };

  return (
    <h2 style={{ marginBottom: '20px', color: isPlaying ? '#222' : '#C33' }}>
      {getMessage()}
    </h2>
  );
};

export default Status;
