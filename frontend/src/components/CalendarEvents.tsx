import React, { useState } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';

const events = [
  { date: '2025-07-03', company: 'AAPL', event: 'Earnings Call' },
  { date: '2025-07-03', company: 'AA3PL', event: 'Earnings Call12' },
];

const CalendarEvents = () => {
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const formatDate = (date: Date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };
  const selectedEvents = selectedDate ? events.filter(e => e.date === formatDate(selectedDate)) : [];
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
      <Calendar
        onClickDay={date => setSelectedDate(date)}
        tileContent={({ date }: { date: Date }) => {
          const ev = events.find(e => e.date === formatDate(date));
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
      )}
    </section>
  );
};

export default CalendarEvents;