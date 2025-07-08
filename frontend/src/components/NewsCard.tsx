import React from 'react';
import '../css/NewsCard.css';

interface NewsCardProps {
  title: string;
  date: string;
  source: string;
  url: string;
}

const NewsCard: React.FC<NewsCardProps> = ({ title, date, source, url }) => (
  <a href={url} target="_blank" rel="noopener noreferrer" className="news-card-link">
    <div className="news-card news-card-compact">
      <div className="news-card-title">{title}</div>
      <div className="news-card-meta-right">
        {date} · {source}
      </div>
    </div>
  </a>
);

export default NewsCard;