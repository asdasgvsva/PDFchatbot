import React, { useState, useRef, useEffect } from 'react';
import '../css/Chatbot.tw.ts';

interface Message {
  from: 'user' | 'bot';
  text: string;
}

const Chatbot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { from: 'bot', text: '안녕하세요! 궁금한 점을 물어보세요.' },
    { from: 'bot', text: '==================================' },
    { from: 'bot', text: 'ex)BioTech Inc에 대한 최근 뉴스 3건 요약해줘\n' },
    { from: 'bot', text: 'ex)Russell 2000에 포함된 반도체 제조 기업들을 알려줘.' },
  ]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    setMessages([...messages, { from: 'user', text: input }]);
    setLoading(true);
    const userInput = input;
    setInput('');
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userInput })
      });
      const data = await res.json();
      setMessages(msgs => [...msgs, { from: 'bot', text: data.answer }]);
    } catch (e) {
      setMessages(msgs => [...msgs, { from: 'bot', text: '오류가 발생했습니다.' }]);
    }
    setLoading(false);
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="chatbot-container">
      <h2 className="chatbot-header">챗봇</h2>
      <div className="chatbot-messages">
        {messages.map((msg, idx) => {
          const isExample = msg.text.trim().startsWith('ex)');
          return (
            <div
              key={idx}
              className={
                msg.from === 'user'
                  ? 'chatbot-message user'
                  : isExample
                    ? 'chatbot-message bot example'
                    : 'chatbot-message bot'
              }
            >
              <span className="chatbot-bubble">{msg.text}</span>
            </div>
          );
        })}
        <div ref={messagesEndRef} />
      </div>
      <form className="chatbot-input-area">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
          placeholder="메시지를 입력하세요"
          className="chatbot-input"
          disabled={loading}
        />
        <button className="chatbot-send-btn" type="submit" disabled={loading}>전송</button>
      </form>
    </div>
  );
};

export default Chatbot; 