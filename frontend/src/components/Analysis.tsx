import React, { useState } from "react";
import axios from "axios";
import "./Analysis.css";

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
    <div className="analysis-container">
      <h2>기업분석</h2>
      <div className="analysis-search-bar">
        <input
          value={ticker}
          onChange={e => setTicker(e.target.value.toUpperCase())}
          placeholder="티커 입력 (예: IONQ)"
        />
        <button onClick={handleSearch} disabled={loading || !ticker}>
          {loading ? "분석 중..." : "분석"}
        </button>
      </div>
      {error && <div className="analysis-error">{error}</div>}
      {result && (
        <div className="analysis-result">
          <h3>{result.company.name} ({result.company.ticker})</h3>
          <h4>분석서</h4>
          <pre className="analysis-report">{result.analysis}</pre>

          <h4>실적 차트</h4>
          <div className="analysis-chart-placeholder">차트 영역 (예: recharts, chart.js 등)</div>

          <h4>주가 차트</h4>
          <div className="analysis-chart-placeholder">차트 영역 (예: recharts, chart.js 등)</div>

          <h4>실적 표</h4>
          <table className="analysis-table">
            <thead>
              <tr>
                <th>분기</th><th>실적</th><th>예상</th>
              </tr>
            </thead>
            <tbody>
              {result.tables.earnings_table.map(row => (
                <tr key={row.period}>
                  <td>{row.period}</td>
                  <td>{row.actual}</td>
                  <td>{row.estimate}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <h4>주요 뉴스</h4>
          <ul className="analysis-news-list">
            {result.news.map(n => (
              <li key={n.url}>
                <a href={n.url} target="_blank" rel="noopener noreferrer">{n.headline}</a>
                <div className="analysis-news-summary">{n.summary}</div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Analysis;
