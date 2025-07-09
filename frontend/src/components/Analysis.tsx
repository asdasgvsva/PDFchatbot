import React, { useState, useRef } from 'react';
import axios from 'axios';
import * as tw from '../css/Analysis.tw';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, CartesianGrid } from 'recharts';

interface Company {
  ticker: string;
  name: string;
}

interface EarningsRow {
  period: string;
  actual: number;
  estimate: number;
}

interface NewsRow {
  headline: string;
  summary: string;
  url: string;
  datetime: number;
}

interface AnalysisResult {
  company: Company;
  analysis: string;
  tables: {
    earnings_table: EarningsRow[];
    news_table: NewsRow[];
  };
  news: NewsRow[];
}

const Analysis = () => {
  const [query, setQuery] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [suggestions, setSuggestions] = useState<Company[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [selectedIdx, setSelectedIdx] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);

  // 자동완성 fetch
  const fetchSuggestions = async (val: string) => {
    if (!val.trim()) {
      setSuggestions([]);
      return;
    }
    try {
      const res = await axios.get(`/api/company/list?search=${encodeURIComponent(val)}`);
      // ticker에 입력값이 포함된 경우만 필터
      const filtered = (res.data.companies || []).filter((c: Company) => c.ticker.toUpperCase().includes(val.trim().toUpperCase()));
      setSuggestions(filtered);
    } catch {
      setSuggestions([]);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setQuery(val);
    setError('');
    setShowSuggestions(true);
    setSelectedIdx(-1);
    if (val.trim().length > 0) {
      fetchSuggestions(val);
    } else {
      setSuggestions([]);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (!showSuggestions || suggestions.length === 0) return;
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIdx(idx => Math.min(idx + 1, suggestions.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIdx(idx => Math.max(idx - 1, 0));
    } else if (e.key === 'Enter') {
      if (selectedIdx >= 0 && selectedIdx < suggestions.length) {
        const company = suggestions[selectedIdx];
        setQuery(company.ticker);
        setShowSuggestions(false);
        setSelectedIdx(-1);
        setTimeout(() => {
          inputRef.current?.blur();
          (document.activeElement as HTMLElement)?.blur();
          inputRef.current?.form?.requestSubmit();
        }, 0);
      }
    }
  };

  const handleSuggestionClick = (company: Company) => {
    setQuery(company.ticker);
    setShowSuggestions(false);
    inputRef.current?.focus();
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setResult(null);
    setShowSuggestions(false);
    if (!query.trim()) {
      setError('검색어를 입력해주세요.');
      return;
    }
    setLoading(true);
    try {
      const res = await axios.get(`/api/company/analysis?ticker=${encodeURIComponent(query.trim().toUpperCase())}`);
      setResult(res.data);
    } catch (e: any) {
      setError(e.response?.data?.detail || '분석 결과를 불러오지 못했습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={tw.container} style={{ position: 'relative' }}>
      <form className={tw.searchBar} onSubmit={handleSearch} autoComplete="off" style={{ marginBottom: 40 }}>
        <div style={{ position: 'relative', flex: 1 }}>
          <input
            ref={inputRef}
            className={tw.input}
            value={query}
            onChange={handleInputChange}
            onFocus={() => query && setShowSuggestions(true)}
            onKeyDown={handleKeyDown}
            placeholder="검색어를 입력해주세요 (예시: IONQ)"
            autoComplete="off"
            style={{ width: '100%' }}
          />
          {showSuggestions && suggestions.length > 0 && (
            <ul style={{
              position: 'absolute',
              top: '100%',
              left: 0,
              right: 0,
              zIndex: 10,
              background: '#fff',
              border: '1px solid #e5e7eb',
              borderRadius: 8,
              marginTop: 2,
              maxHeight: 220,
              overflowY: 'auto',
              boxShadow: '0 2px 8px 0 rgba(0,0,0,0.06)',
              listStyle: 'none',
              padding: 0
            }}>
              {suggestions.map((company, idx) => (
                <li
                  key={company.ticker}
                  style={{
                    padding: '8px 16px',
                    cursor: 'pointer',
                    fontSize: 15,
                    display: 'flex',
                    alignItems: 'center',
                    background: idx === selectedIdx ? '#f3f4f6' : undefined
                  }}
                  onMouseDown={e => { e.preventDefault(); handleSuggestionClick(company); }}
                  onMouseOver={() => setSelectedIdx(idx)}
                  onMouseOut={() => setSelectedIdx(-1)}
                >
                  <span style={{ fontWeight: 600 }}>{company.ticker}</span>
                  <span style={{ color: '#888', marginLeft: 8, fontSize: 14 }}>{company.name}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
        <button
          className={tw.button}
          type="submit"
          disabled={loading}
          style={{ marginLeft: 8, minWidth: 80, display: 'flex', alignItems: 'center', justifyContent: 'center' }}
        >
          {loading ? (
            <span style={{
              display: 'inline-block',
              width: 20,
              height: 20,
              border: '3px solid #fff',
              borderTop: '3px solid #2563eb',
              borderRadius: '50%',
              animation: 'spin 1s linear infinite',
              marginRight: 0
            }}
            // @ts-ignore
            className="analysis-spinner"
            />
          ) : '검색'}
        </button>
      </form>
      {error && <div className={tw.error}>{error}</div>}
      {result && (
        <div style={{ width: '100%', maxWidth: 700, background: '#fff', borderRadius: 16, boxShadow: '0 2px 12px 0 rgba(0,0,0,0.06)', padding: 32, marginTop: 32 }}>
          <h3 style={{ fontWeight: 700, fontSize: 22, marginBottom: 8 }}>{result.company.name} ({result.company.ticker})</h3>
          {/* AI 분석서 */}
          <div style={{ borderTop: '2px solid #e5e7eb', paddingTop: 24, marginTop: 24, marginBottom: 32 }}>
            <h4 style={{ fontWeight: 600, marginBottom: 8 }}>AI 분석서</h4>
            <pre style={{ background: '#f8fafc', borderRadius: 8, padding: 20, fontSize: 16, marginBottom: 0, whiteSpace: 'pre-wrap' }}>{result.analysis}</pre>
          </div>
          {/* 실적 표 */}
          <div style={{ borderTop: '2px solid #e5e7eb', paddingTop: 24, marginTop: 0, marginBottom: 32 }}>
            <h4 style={{ fontWeight: 600, marginBottom: 8 }}>실적 표</h4>
            <div style={{
              width: '100%',
              maxWidth: 500,
              minHeight: 260,
              margin: '0 auto',
              background: '#fff',
              borderRadius: 12,
              boxShadow: '0 1px 6px 0 rgba(0,0,0,0.04)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              padding: 0
            }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: 0 }}>
                <thead>
                  <tr>
                    <th style={{ borderBottom: '1px solid #eee', padding: 8, textAlign: 'left' }}>분기</th>
                    <th style={{ borderBottom: '1px solid #eee', padding: 8, textAlign: 'left' }}>실적</th>
                    <th style={{ borderBottom: '1px solid #eee', padding: 8, textAlign: 'left' }}>예상</th>
                  </tr>
                </thead>
                <tbody>
                  {result.tables.earnings_table.map(row => (
                    <tr key={row.period}>
                      <td style={{ padding: 8 }}>{row.period}</td>
                      <td style={{ padding: 8 }}>{row.actual}</td>
                      <td style={{ padding: 8 }}>{row.estimate}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
          {/* 실적 그래프 */}
          <div style={{ borderTop: '2px solid #e5e7eb', paddingTop: 24, marginTop: 0, marginBottom: 32 }}>
            <h4 style={{ fontWeight: 600, marginBottom: 8 }}>실적 그래프</h4>
            <div style={{
              width: '100%',
              maxWidth: 500,
              minHeight: 260,
              margin: '0 auto',
              background: '#fff',
              borderRadius: 12,
              boxShadow: '0 1px 6px 0 rgba(0,0,0,0.04)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              padding: 0
            }}>
              <ResponsiveContainer width="100%" height={260}>
                <BarChart
                  data={result.tables.earnings_table}
                  margin={{ top: 16, right: 24, left: 0, bottom: 8 }}
                  barCategoryGap="20%"
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="period" tick={{ fontSize: 13 }} />
                  <YAxis tick={{ fontSize: 13 }} />
                  <Tooltip
                    contentStyle={{ borderRadius: 8, fontSize: 14 }}
                    labelStyle={{ fontWeight: 600 }}
                    formatter={(value: any) => value?.toLocaleString?.() ?? value}
                  />
                  <Legend iconType="circle" />
                  <Bar
                    dataKey="actual"
                    fill="#2563eb"
                    name="실적"
                    radius={[12, 12, 0, 0]}
                    maxBarSize={32}
                    isAnimationActive={true}
                  />
                  <Bar
                    dataKey="estimate"
                    fill="#f59e42"
                    name="예상"
                    radius={[12, 12, 0, 0]}
                    maxBarSize={32}
                    isAnimationActive={true}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
          {/* 주요 뉴스 */}
          <div style={{ borderTop: '2px solid #e5e7eb', paddingTop: 24, marginTop: 0 }}>
            <h4 style={{ fontWeight: 600, marginBottom: 8 }}>주요 뉴스</h4>
            <ul style={{ padding: 0, margin: 0, listStyle: 'none' }}>
              {result.news.map(n => (
                <li key={n.url} style={{ marginBottom: 20 }}>
                  <a href={n.url} target="_blank" rel="noopener noreferrer" style={{ fontWeight: 600, color: '#2563eb', textDecoration: 'underline' }}>{n.headline}</a>
                  <div style={{ color: '#555', fontSize: 15, marginTop: 4 }}>{n.summary}</div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default Analysis;

<style>{`
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.analysis-spinner { vertical-align: middle; }
`}</style> 