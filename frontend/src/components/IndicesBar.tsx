import React, { useEffect, useState } from 'react';
import * as tw from '../css/IndicesBar.tw';

interface IndexData {
  ticker: string;
  name: string;
  change: string;
}

const GROUP_SIZE = 5;

const IndicesBar: React.FC = () => {
  const [indices, setIndices] = useState<IndexData[]>([]);
  const [groupIdx, setGroupIdx] = useState(0);

  useEffect(() => {
    fetch('/api/indices')
      .then(res => res.json())
      .then(data => setIndices(Array.isArray(data.indices) ? data.indices : []));
  }, []);

  useEffect(() => {
    if (indices.length === 0) return;
    const interval = setInterval(() => {
      setGroupIdx(idx => (idx + 1) % Math.ceil(indices.length / GROUP_SIZE));
    }, 3000);
    return () => clearInterval(interval);
  }, [indices]);

  const start = groupIdx * GROUP_SIZE;
  const end = start + GROUP_SIZE;
  const currentGroup = indices.slice(start, end);

  return (
    <div className={tw.indicesBar}>
      {currentGroup.map(idx => (
        <div className={tw.indexItem} key={idx.ticker}>
          <span className={tw.indexName}>{idx.ticker}</span>
          <span className={idx.change && idx.change.startsWith('+') ? tw.indexChangeUp : tw.indexChangeDown}>{idx.change}</span>
        </div>
      ))}
    </div>
  );
};

export default IndicesBar;