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

  const formatDate = (date: Date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };
  const selectedEvents = selectedDate ? events.filter(e => e.date === formatDate(selectedDate)) : [];

  const MAX_EVENTS = 15;
  const visibleEvents = selectedEvents.slice(0, MAX_EVENTS);
  const hasMore = selectedEvents.length > MAX_EVENTS;

  return (
    <section className={tw.section}>
      <h2 className="font-bold text-lg mb-3">주요 일정 캘린더</h2>
      <Calendar
        onClickDay={date => setSelectedDate(date)}
        tileContent={({ date }: { date: Date }) => {
          const ev = events.find(e => e.date === formatDate(date));
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
      )}
    </section>
  );
};

export default CalendarEvents;