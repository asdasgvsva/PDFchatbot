import React, { useEffect, useState, useRef } from 'react';
import '../css/TopMovers.tw';

interface Mover {
  ticker: string;
  name: string;
  change: string;
}

const GROUP_SIZE = 5;
const TOTAL_COUNT = 30;
const INTERVAL_MS = 3000;

const TopMovers: React.FC = () => {
  const [movers, setMovers] = useState<Mover[]>([]);
  const [groupIdx, setGroupIdx] = useState(0);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    fetch('/api/top-movers')
      .then(res => res.json())
      .then(data => setMovers(Array.isArray(data.movers) ? data.movers.slice(0, TOTAL_COUNT) : []));
  }, []);

  useEffect(() => {
    if (movers.length === 0) return;
    intervalRef.current = setInterval(() => {
      setGroupIdx(idx => (idx + 1) % Math.ceil(movers.length / GROUP_SIZE));
    }, INTERVAL_MS);
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [movers]);

  const start = groupIdx * GROUP_SIZE;
  const end = start + GROUP_SIZE;
  const currentGroup = movers.slice(start, end);

  return (
    <div className="top-movers-section">
      <ul className="top-movers-list">
        {currentGroup.map((m, idx) => (
          <li key={m.ticker} className="top-mover-item">
            <span className="mover-ticker">{m.ticker}</span>
            <span className="mover-name">{m.name}</span>
            <span className={`mover-change ${m.change.startsWith('+') ? 'up' : 'down'}`}>{m.change}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TopMovers; 