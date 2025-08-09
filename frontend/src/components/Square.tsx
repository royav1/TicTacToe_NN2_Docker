// src/components/Square.tsx
import React from 'react';

type SquareProps = {
  value: number; // 0 = empty, 1 = X, 2 = O
  onClick: () => void;
};

const Square: React.FC<SquareProps> = ({ value, onClick }) => {
  // Convert number to symbol for display
  const renderSymbol = (val: number): string => {
    if (val === 1) return 'X';
    if (val === 2) return 'O';
    return '';
  };

  return (
    <button
      onClick={onClick}
      style={{
        width: '60px',
        height: '60px',
        fontSize: '24px',
        fontWeight: 'bold',
        border: '1px solid #333',
        cursor: 'pointer',
        backgroundColor: '#fff',
      }}
    >
      {renderSymbol(value)}
    </button>
  );
};

export default Square;
