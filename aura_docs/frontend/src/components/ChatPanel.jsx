import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles } from 'lucide-react';

const ChatPanel = ({ messages, onSendMessage, isGenerating, onSelectDoc }) => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom of messages list
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isGenerating]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || isGenerating) return;
    onSendMessage(input);
    setInput('');
  };

  return (
    <div className="chat-panel">
      <div className="chat-header">
        <div className="chat-title">
          <Sparkles size={16} className="text-secondary" />
          <span>AI Assistant</span>
        </div>
        <div className="chat-subtitle">Gemini RAG Agent</div>
      </div>

      <div className="messages-list">
        {messages.length === 0 ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-secondary)', textAlign: 'center', padding: '20px' }}>
            <Bot size={32} style={{ marginBottom: '12px', opacity: 0.6 }} />
            <p style={{ fontSize: '0.875rem', fontWeight: 500 }}>Ask a question about this knowledge base.</p>
            <p style={{ fontSize: '0.75rem', marginTop: '4px', opacity: 0.8 }}>The AI will answer using the local documentation files.</p>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div 
              key={index} 
              className={`chat-message ${msg.sender === 'user' ? 'message-user' : 'message-agent'}`}
            >
              <div className="message-header" style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.75rem', fontWeight: 700, marginBottom: '4px', opacity: 0.8 }}>
                {msg.sender === 'user' ? (
                  <>
                    <User size={12} />
                    <span>You</span>
                  </>
                ) : (
                  <>
                    <Bot size={12} />
                    <span>Bedrock Agent</span>
                  </>
                )}
              </div>
              <div className="message-text" style={{ whiteSpace: 'pre-wrap' }}>
                {msg.text}
              </div>
              
              {/* Source citations */}
              {msg.sources && msg.sources.length > 0 && (
                <div className="message-sources">
                  <div style={{ fontWeight: 600, fontSize: '0.7rem', textTransform: 'uppercase', marginBottom: '2px' }}>Sources:</div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px 12px' }}>
                    {msg.sources.map((src, sIdx) => {
                      const baseName = src.split('/').pop();
                      return (
                        <span 
                          key={sIdx} 
                          className="source-tag" 
                          onClick={() => onSelectDoc(src)}
                          title={src}
                        >
                          {baseName}
                        </span>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          ))
        )}
        
        {isGenerating && (
          <div className="chat-message message-agent">
            <div className="message-header" style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.75rem', fontWeight: 700, opacity: 0.8 }}>
              <Bot size={12} />
              <span>Thinking...</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '6px 0' }}>
              <div className="loader-spinner"></div>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Searching documents and formulating answer...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <form onSubmit={handleSubmit} className="chat-form">
          <input
            type="text"
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question..."
            disabled={isGenerating}
          />
          <button 
            type="submit" 
            className="icon-btn" 
            style={{ backgroundColor: 'var(--accent-color)', color: 'var(--accent-text)', border: 'none' }}
            disabled={isGenerating || !input.trim()}
          >
            <Send size={16} />
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatPanel;
