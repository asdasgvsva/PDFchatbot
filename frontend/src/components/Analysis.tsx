import React, { useState } from "react";
import axios from "axios";
import * as tw from '../css/Analysis.tw';

interface Company {
  ticker: string;
  name: string;
}

interface EarningsRow {
  period: string;
  actual: number;
  estimate: number;
}

interface QuoteRow {
  date: string;
  close: number;
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
  charts: {
    earnings_chart: EarningsRow[];
    price_chart: QuoteRow[];
  };
  tables: {
    earnings_table: EarningsRow[];
    news_table: NewsRow[];
  };
  news: NewsRow[];
}

const Analysis: React.FC = () => {
  const [ticker, setTicker] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await axios.get(`/api/company/analysis?ticker=${ticker}`);
      setResult(res.data);
    } catch (e: any) {
      setError(e.response?.data?.detail || "분석 중 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={tw.container}>
      <h2 className="text-2xl font-bold mb-4">기업분석</h2>
      <div className={tw.searchBar}>
        <input
          value={ticker}
          onChange={e => setTicker(e.target.value.toUpperCase())}
          placeholder="티커 입력 (예: IONQ)"
          className={tw.input}
        />
        <button onClick={handleSearch} disabled={loading || !ticker} className={tw.button}>
          {loading ? "분석 중..." : "분석"}
        </button>
      </div>
      {error && <div className={tw.error}>{error}</div>}
      {result && (
        <div className={tw.result}>
          <h3 className="text-xl font-bold mb-2">{result.company.name} ({result.company.ticker})</h3>
          <h4 className="font-semibold mb-1">분석서</h4>
          <pre className={tw.report}>{result.analysis}</pre>

          <h4 className="font-semibold mb-1">실적 차트</h4>
          <div className={tw.chartPlaceholder}>차트 영역 (예: recharts, chart.js 등)</div>

          <h4 className="font-semibold mb-1">주가 차트</h4>
          <div className={tw.chartPlaceholder}>차트 영역 (예: recharts, chart.js 등)</div>

          <h4 className="font-semibold mb-1">실적 표</h4>
          <table className={tw.table}>
            <thead>
              <tr>
                <th className={tw.th}>분기</th><th className={tw.th}>실적</th><th className={tw.th}>예상</th>
              </tr>
            </thead>
            <tbody>
              {result.tables.earnings_table.map(row => (
                <tr key={row.period}>
                  <td className={tw.td}>{row.period}</td>
                  <td className={tw.td}>{row.actual}</td>
                  <td className={tw.td}>{row.estimate}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <h4 className="font-semibold mb-1">주요 뉴스</h4>
          <ul className={tw.newsList}>
            {result.news.map(n => (
              <li key={n.url} className={tw.newsItem}>
                <a href={n.url} target="_blank" rel="noopener noreferrer" className={tw.newsLink}>{n.headline}</a>
                <div className={tw.newsSummary}>{n.summary}</div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Analysis; 