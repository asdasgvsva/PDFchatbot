<<<<<<< HEAD
import React, { useState, useEffect } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import axios from 'axios';
import * as tw from '../css/CalendarEvents.tw';

const CalendarEvents = () => {
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [events, setEvents] = useState<{ date: string; company: string; event: string }[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        setLoading(true);
        const res = await axios.get('/api/calendar/events');
        setEvents(res.data.events || []);
        setError(null);
      } catch (err: any) {
        setError('이벤트를 불러오지 못했습니다.');
      } finally {
        setLoading(false);
      }
    };
    fetchEvents();
  }, []);

=======
import React, { useState } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';

const events = [
  { date: '2025-07-03', company: 'AAPL', event: 'Earnings Call' },
  { date: '2025-07-03', company: 'AA3PL', event: 'Earnings Call12' },
];

const CalendarEvents = () => {
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
>>>>>>> 4dfa035daeb614c7a8807fbc966899c348a475ef
  const formatDate = (date: Date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };
  const selectedEvents = selectedDate ? events.filter(e => e.date === formatDate(selectedDate)) : [];
<<<<<<< HEAD

  const MAX_EVENTS = 15;
  const visibleEvents = selectedEvents.slice(0, MAX_EVENTS);
  const hasMore = selectedEvents.length > MAX_EVENTS;

  return (
    <section className={tw.section}>
      <h2 className="font-bold text-lg mb-3">주요 일정 캘린더</h2>
=======
  const cellStyle = {
    padding: 4,
    maxWidth: 120,
    minWidth: 60,
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
    fontSize: 'clamp(12px, 1em, 16px)',
  };

  const cardStyle = {
    width: '100%',
    background: '#fff',
    borderRadius: 16,
    boxShadow: '0 2px 12px 0 rgba(0,0,0,0.06)',
    padding: 20,
    marginBottom: 16,
  };

  return (
    <section>
>>>>>>> 4dfa035daeb614c7a8807fbc966899c348a475ef
      <Calendar
        onClickDay={date => setSelectedDate(date)}
        tileContent={({ date }: { date: Date }) => {
          const ev = events.find(e => e.date === formatDate(date));
<<<<<<< HEAD
          return ev ? <span className={tw.dot}>●</span> : null;
        }}
      />
      {loading && <div className={tw.loading}>불러오는 중...</div>}
      {error && <div className={tw.error}>{error}</div>}
      {selectedEvents.length > 0 && (
        selectedEvents.length > 10 ? (
          <div style={{ maxHeight: 280, overflowY: 'auto' }}>
            <table className={tw.table}>
              <thead>
                <tr>
                  <th className={tw.th}>기업</th>
                  <th className={tw.th}>이벤트</th>
                  <th className={tw.th}>날짜</th>
                </tr>
              </thead>
              <tbody>
                {selectedEvents.map((ev, idx) => (
                  <tr key={ev.company + ev.date} className={tw.tr(idx, selectedEvents.length)}>
                    <td className={tw.td}>{ev.company}</td>
                    <td className={tw.td}>{ev.event}</td>
                    <td className={tw.td}>{ev.date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <table className={tw.table}>
            <thead>
              <tr>
                <th className={tw.th}>기업</th>
                <th className={tw.th}>이벤트</th>
                <th className={tw.th}>날짜</th>
              </tr>
            </thead>
            <tbody>
              {selectedEvents.map((ev, idx) => (
                <tr key={ev.company + ev.date} className={tw.tr(idx, selectedEvents.length)}>
                  <td className={tw.td}>{ev.company}</td>
                  <td className={tw.td}>{ev.event}</td>
                  <td className={tw.td}>{ev.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )
=======
          return ev ? <span style={{ color: 'red', fontSize: 12 }}>●</span> : null;
        }}
      />
      {selectedEvents.length > 0 && (
        <table style={{ marginTop: 12, width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={{ borderBottom: '1px solid #ccc', textAlign: 'left', padding: 4 }}>기업</th>
              <th style={{ borderBottom: '1px solid #ccc', textAlign: 'left', padding: 4 }}>이벤트</th>
              <th style={{ borderBottom: '1px solid #ccc', textAlign: 'left', padding: 4 }}>날짜</th>
            </tr>
          </thead>
          <tbody>
            {selectedEvents.map((ev, idx) => (
              <tr key={ev.company + ev.date} style={{
                borderBottom: idx !== selectedEvents.length - 1 ? '1px solid #eee' : undefined
              }}>
                <td style={cellStyle}>{ev.company}</td>
                <td style={cellStyle}>{ev.event}</td>
                <td style={cellStyle}>{ev.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
>>>>>>> 4dfa035daeb614c7a8807fbc966899c348a475ef
      )}
    </section>
  );
};

export default CalendarEvents;