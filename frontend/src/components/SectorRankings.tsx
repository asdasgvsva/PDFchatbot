import React from 'react';

const rankings = [
  { type: '수익률 TOP 10', data: [
    { ticker: 'AAPL', value: '+12.3%' },
    { ticker: 'TSLA', value: '+10.1%' },
    { ticker: 'NVDA', value: '+9.8%' },
    { ticker: 'AMD', value: '+8.7%' },
    { ticker: 'MSFT', value: '+7.5%' },
  ]},
  { type: '공매도 증가율 TOP 10', data: [
    { ticker: 'GME', value: '+22.1%' },
    { ticker: 'AMC', value: '+18.4%' },
    { ticker: 'BBBY', value: '+15.2%' },
    { ticker: 'TSLA', value: '+12.9%' },
    { ticker: 'AAPL', value: '+10.3%' },
  ]},
];

const SectorRankings = () => (
  <>
    <h3> 섹터별 랭킹</h3>
    {rankings.map(rank => (
      <>
        <div key={rank.type}>{rank.type}</div>
        <ul>
          {rank.data.map(item => (
            <li key={item.ticker}>
              <span>{item.ticker}</span> <span style={{ color: '#2ecc40' }}>{item.value}</span>
            </li>
          ))}
        </ul>
      </>
    ))}
  </>
);

export default SectorRankings;
