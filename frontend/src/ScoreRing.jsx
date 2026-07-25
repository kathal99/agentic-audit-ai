import React from 'react';

export default function ScoreRing({ score }) {
  const normalized = Math.max(0, Math.min(score, 100));
  const angle = (normalized / 100) * 270;
  const color = normalized >= 70 ? '#22c55e' : normalized >= 40 ? '#f59e0b' : '#fb7185';

  return (
    <div className="score-ring">
      <svg viewBox="0 0 120 120" width="120" height="120">
        <circle cx="60" cy="60" r="50" stroke="#1f2937" strokeWidth="10" fill="none" />
        <circle
          cx="60"
          cy="60"
          r="50"
          stroke={color}
          strokeWidth="10"
          fill="none"
          strokeLinecap="round"
          transform="rotate(-135 60 60)"
          strokeDasharray={`${(angle / 360) * 314} 314`}
        />
      </svg>
      <div className="score-ring__label">
        <span>{normalized}</span>
        <small>SECURITY</small>
      </div>
    </div>
  );
}
