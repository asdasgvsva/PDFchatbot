import React, { useEffect, useState } from 'react';
import * as tw from '../css/NewsList.tw';

interface NewsItem {
  headline_ko: string;
  summary_ko: string;
  url: string;
}

const PAGE_SIZE = 15;

const NewsList: React.FC = () => {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [images, setImages] = useState<{ [url: string]: string | null }>({});

  useEffect(() => {
    fetch(`/api/news?page=${page}&limit=${PAGE_SIZE}`)
      .then(res => res.json())
      .then(data => {
        const newsArr = Array.isArray(data) ? data : (data.news || []);
        setNews(newsArr);
        if (data.totalCount) {
          setTotalPages(Math.ceil(data.totalCount / PAGE_SIZE));
        }
        // 이미지 미리 fetch
        (newsArr as NewsItem[]).forEach((item: NewsItem) => {
          if (!images[item.url]) {
            fetch(`/api/news/image?headline=${encodeURIComponent(item.headline_ko)}`)
              .then(res => res.json())
              .then(imgData => {
                setImages(prev => ({ ...prev, [item.url]: imgData.image_url }));
              });
          }
        });
      })
      .catch(err => {
        console.error('뉴스 불러오기 실패:', err);
      });
    // eslint-disable-next-line
  }, [page]);

  const renderPagination = () => {
    const pages = [];
    const maxPage = totalPages;
    const current = page;
    const windowSize = 5;
    let start = Math.max(1, current - Math.floor(windowSize / 2));
    let end = Math.min(maxPage, start + windowSize - 1);
    if (end - start < windowSize - 1) start = Math.max(1, end - windowSize + 1);

    if (current > 1) {
      pages.push(
        <button key="prev" className={tw.pageBtn} onClick={() => setPage(current - 1)}>&lt;</button>
      );
    }
    for (let i = start; i <= end; i++) {
      pages.push(
        <button
          key={i}
          className={`${tw.pageBtn} ${i === current ? tw.pageBtnActive : ""}`}
          onClick={() => setPage(i)}
          disabled={i === current}
        >
          {i}
        </button>
      );
    }
    if (current < maxPage) {
      pages.push(
        <button key="next" className={tw.pageBtn} onClick={() => setPage(current + 1)}>&gt;</button>
      );
    }
    return <div className={tw.pagination}>{pages}</div>;
  };

  return (
    <div className={tw.container}>
      <div style={{ fontWeight: 700, fontSize: 20, marginBottom: 16 }}>주요뉴스</div>
      {news.map((item, idx) => (
        <React.Fragment key={item.url}>
          <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center', gap: 20 }}>
            {images[item.url] ? (
              <img
                src={images[item.url] || ''}
                alt="뉴스 이미지"
                style={{ width: 96, height: 96, objectFit: 'cover', borderRadius: 10, background: '#f3f4f6', flexShrink: 0 }}
              />
            ) : (
              <div style={{ width: 96, height: 96, borderRadius: 10, background: '#e5e7eb', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#bbb', fontSize: 32, flexShrink: 0 }}>
                ?
              </div>
            )}
            <div style={{ flex: 1 }}>
              <a href={item.url} target="_blank" rel="noopener noreferrer" className={tw.headline} style={{ display: 'block', textDecoration: 'none' }}>
                {item.headline_ko}
              </a>
              <div className={tw.summary}>{item.summary_ko}</div>
            </div>
          </div>
          {idx !== news.length - 1 && (
            <div style={{ borderBottom: '1px solid #bbb', margin: '8px 0' }} />
          )}
        </React.Fragment>
      ))}
      {renderPagination()}
    </div>
  );
};

export default NewsList;
