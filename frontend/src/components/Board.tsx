// src/components/Board.tsx
import React from 'react';
import Square from './Square';

type BoardProps = {
  board: number[]; // 0 = empty, 1 = X, -1 = O from backend
  onClick: (index: number) => void;
};

const Board: React.FC<BoardProps> = ({ board, onClick }) => {
  const renderSquare = (index: number) => {
    let value = board[index];
    if (value === -1) value = 2; // Map backend O (-1) to frontend O (2)

    return (
      <Square
        key={index}
        value={value}
        onClick={() => onClick(index)}
      />
    );
  };

  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 60px)',
        gap: '4px',
        justifyContent: 'center',
      }}
    >
      {board.map((_, i) => renderSquare(i))}
    </div>
  );
};

export default Board;
