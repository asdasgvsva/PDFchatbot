import React, { useState, useRef, useEffect } from 'react';
import IndicesBar from './components/IndicesBar';
import NewsList from './components/NewsList';
import TopMovers from './components/TopMovers';
import Chatbot from './components/Chatbot';
import Analysis from './components/Analysis';
import CalendarEvents from './components/CalendarEvents';
import SectorRankings from './components/SectorRankings';
import * as tw from './css/App.tw';
import { FaSearch, FaBell, FaUserCircle } from 'react-icons/fa';

function App() {
  const [tab, setTab] = useState<'news' | 'analysis'>('news');

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className={tw.root}>
      {/* 메뉴바 */}
      <div className={tw.menuBar}>
        <div className="flex items-center gap-2">
          <span className="font-extrabold text-lg text-black tracking-tight">Russell</span>
        </div>
        <div className="flex gap-2">
          <button
            className={tw.menuBtn + ' ' + (tab === 'news' ? tw.menuBtnActive : tw.menuBtnInactive)}
            onClick={() => setTab('news')}
          >
            뉴스
          </button>
          <button
            className={tw.menuBtn + ' ' + (tab === 'analysis' ? tw.menuBtnActive : tw.menuBtnInactive)}
            onClick={() => setTab('analysis')}
          >
            기업분석
          </button>
        </div>
        <div className="flex items-center gap-2">
          <span style={{cursor: 'pointer'}}><FaSearch color="#222" size={18} /></span>
          <span style={{cursor: 'pointer'}}><FaBell color="#222" size={18} /></span>
          <span style={{cursor: 'pointer'}}><FaUserCircle color="#222" size={22} /></span>
        </div>
      </div>
      {/* 지수바 */}
      <IndicesBar />
      {/* 본문 */}
      {tab === 'news' ? (
        <div className={tw.mainContent}>
          <section className={tw.section}>
            <NewsList />
          </section>
          {/* CalendarEvents와 SectorRankings를 aside로 묶지 않고 각각 별도 카드로 분리 */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 20, maxWidth: 400, minWidth: 320, marginLeft: 24 }}>
            <div className={tw.card}>
              <CalendarEvents />
            </div>
            <div className={tw.card}>
              <SectorRankings />
            </div>
          </div>
        </div>
      ) : (
        <div className={tw.analysisContent}>
          <Analysis />
        </div>
      )}
    </div>
  );
}
export default App;