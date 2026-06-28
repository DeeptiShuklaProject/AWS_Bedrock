import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import DocReader from './components/DocReader';
import ChatPanel from './components/ChatPanel';
import { Sun, Moon, MessageSquare, Database, Sparkles, RefreshCw } from 'lucide-react';

const App = () => {
  // Theme state
  const [theme, setTheme] = useState(() => localStorage.getItem('kb-theme') || 'light');
  
  // Knowledge Base States
  const [kbs, setKbs] = useState([]);
  const [selectedKb, setSelectedKb] = useState('');
  
  // Navigation & Document States
  const [navItems, setNavItems] = useState([]);
  const [activeDoc, setActiveDoc] = useState('');
  const [docContent, setDocContent] = useState('');
  const [docLoading, setDocLoading] = useState(false);
  
  // Chat States
  const [messages, setMessages] = useState([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(true);
  const [hasApiKey, setHasApiKey] = useState(true);
  
  // Indexing State
  const [isIndexing, setIsIndexing] = useState(false);
  const [indexStatus, setIndexStatus] = useState('');

  // Apply theme class
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('kb-theme', theme);
  }, [theme]);

  // Save selected KB selection to localStorage
  useEffect(() => {
    if (selectedKb) {
      localStorage.setItem('kb-selected-id', selectedKb);
    }
  }, [selectedKb]);

  // Load KBs and Config on startup
  useEffect(() => {
    const fetchConfig = async () => {
      try {
        const response = await fetch('/api/config');
        const data = await response.json();
        setHasApiKey(data.has_api_key);
        setIsChatOpen(data.has_api_key); // Automatically close panel if key is missing
      } catch (e) {
        console.error('Failed to load application config:', e);
      }
    };

    const fetchKbs = async () => {
      try {
        const response = await fetch('/api/kbs');
        const data = await response.json();
        setKbs(data);
        if (data.length > 0) {
          const cachedKb = localStorage.getItem('kb-selected-id');
          const hasCached = data.some(kb => kb.id === cachedKb);
          if (hasCached) {
            setSelectedKb(cachedKb);
          } else {
            // Fallback default (prioritize Custom Notes, then Bedrock)
            const notesKb = data.find(kb => kb.id === 'doc_replica_notes');
            if (notesKb) {
              setSelectedKb(notesKb.id);
            } else {
              const bedrockKb = data.find(kb => kb.id === 'doc_replica_amazon');
              setSelectedKb(bedrockKb ? bedrockKb.id : data[0].id);
            }
          }
        }
      } catch (e) {
        console.error('Failed to load knowledge bases:', e);
      }
    };

    fetchConfig();
    fetchKbs();
  }, []);

  // Load Navigation tree when KB changes
  useEffect(() => {
    if (!selectedKb) return;
    
    // Immediately clear stale doc state to prevent cross-KB fetch race condition
    setActiveDoc('');
    setDocContent('');
    
    const fetchNavigation = async () => {
      try {
        const response = await fetch(`/api/kbs/${selectedKb}/navigation`);
        const data = await response.json();
        setNavItems(data);
        
        // Reset chat state
        setMessages([]);
        
        // Auto-select the first document in the tree as the home page
        if (data && data.length > 0) {
          const findFirstDoc = (items) => {
            for (const item of items) {
              if (item.href) return item.href;
              if (item.contents && item.contents.length > 0) {
                const found = findFirstDoc(item.contents);
                if (found) return found;
              }
            }
            return '';
          };
          const firstDoc = findFirstDoc(data);
          setActiveDoc(firstDoc);
        } else {
          setActiveDoc('');
          setDocContent('');
        }
      } catch (e) {
        console.error('Failed to load navigation:', e);
        setActiveDoc('');
        setDocContent('');
      }
    };
    
    fetchNavigation();
  }, [selectedKb]);

  // Load Document Content when activeDoc changes
  useEffect(() => {
    if (!selectedKb || !activeDoc) return;
    
    const fetchDoc = async () => {
      setDocLoading(true);
      try {
        const response = await fetch(`/api/kbs/${selectedKb}/document?path=${encodeURIComponent(activeDoc)}`);
        if (!response.ok) throw new Error('Document not found');
        const data = await response.json();
        setDocContent(data.content);
      } catch (e) {
        console.error('Failed to load document:', e);
        setDocContent(`# Error\nCould not load document: ${activeDoc}`);
      } finally {
        setDocLoading(false);
      }
    };
    
    fetchDoc();
  }, [activeDoc, selectedKb]);

  // Toggle theme
  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  // Trigger Indexing
  const handleIndexKb = async () => {
    if (!selectedKb || isIndexing) return;
    setIsIndexing(true);
    setIndexStatus('Indexing...');
    try {
      const response = await fetch(`/api/kbs/${selectedKb}/index`, {
        method: 'POST'
      });
      const data = await response.json();
      if (response.ok) {
        setIndexStatus('✓ Indexed!');
        setTimeout(() => setIndexStatus(''), 3000);
      } else {
        setIndexStatus('❌ Failed');
        alert(data.detail || 'Indexing failed');
      }
    } catch (e) {
      console.error('Indexing failed:', e);
      setIndexStatus('❌ Failed');
    } finally {
      setIsIndexing(false);
    }
  };

  // Send Message to Agent
  const handleSendMessage = async (text) => {
    // Add user message
    const userMsg = { sender: 'user', text };
    setMessages(prev => [...prev, userMsg]);
    
    setIsGenerating(true);
    try {
      const response = await fetch(`/api/kbs/${selectedKb}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: text })
      });
      const data = await response.json();
      
      const agentMsg = {
        sender: 'agent',
        text: data.answer,
        sources: data.sources
      };
      
      setMessages(prev => [...prev, agentMsg]);
    } catch (e) {
      console.error('Chat failed:', e);
      setMessages(prev => [...prev, {
        sender: 'agent',
        text: '❌ Sorry, I failed to process your question. Please make sure the backend server is running and the Gemini API key is configured.'
      }]);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="app-container">
      {/* Top Navbar */}
      <header className="top-bar">
        <div className="logo-section">
          <span className="logo-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" style={{ display: 'block' }}>
              <defs>
                <linearGradient id="auraDiagGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#ff79c6" />
                  <stop offset="50%" stopColor="#bd93f9" />
                  <stop offset="100%" stopColor="#00f2fe" />
                </linearGradient>
                <radialGradient id="auraPinkRadial" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stopColor="#ff79c6" stopOpacity="0.5" />
                  <stop offset="60%" stopColor="#bd93f9" stopOpacity="0.2" />
                  <stop offset="100%" stopColor="#bd93f9" stopOpacity="0" />
                </radialGradient>
                <radialGradient id="auraTealRadial" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stopColor="#00f2fe" stopOpacity="0.4" />
                  <stop offset="60%" stopColor="#50fa7b" stopOpacity="0.15" />
                  <stop offset="100%" stopColor="#50fa7b" stopOpacity="0" />
                </radialGradient>
              </defs>
              <circle className="aura-wave-1" cx="12" cy="12" r="9.5" fill="url(#auraPinkRadial)" />
              <circle className="aura-wave-2" cx="12" cy="12" r="8.5" fill="url(#auraTealRadial)" />
              <path d="M5.5 6.5h6l3.5 3.5v9.5a1 1 0 0 1-1 1h-8.5a1 1 0 0 1-1-1v-13a1 1 0 0 1 1-1z" stroke="url(#auraDiagGrad)" strokeWidth="1.5" strokeLinejoin="round" opacity="0.45" />
              <path d="M8.5 3.5H14l3.5 3.5V17.5a1 1 0 0 1-1 1h-8a1 1 0 0 1-1-1V4.5a1 1 0 0 1 1-1z" stroke="url(#auraDiagGrad)" strokeWidth="1.8" strokeLinejoin="round" />
              <path d="M14 3.5V7h3.5" stroke="url(#auraDiagGrad)" strokeWidth="1.8" strokeLinejoin="round" />
              <path d="M11 9.5h3.5M11 12h3.5M11 14.5h2" stroke="url(#auraDiagGrad)" strokeWidth="1.5" strokeLinecap="round" />
            </svg>
          </span>
          <span>AuraDocs</span>
        </div>
        
        <div className="controls-section">
          {/* KB Dropdown Selector */}
          <div className="kb-selector-container">
            <select 
              value={selectedKb} 
              onChange={(e) => setSelectedKb(e.target.value)}
              className="kb-dropdown"
              disabled={isIndexing}
            >
              {kbs.map(kb => (
                <option key={kb.id} value={kb.id}>{kb.name}</option>
              ))}
            </select>
          </div>

          {/* Index Button (Only show if API key is active) */}
          {hasApiKey && (
            <button 
              onClick={handleIndexKb} 
              className="icon-btn action-btn secondary-btn"
              disabled={isIndexing || !selectedKb}
              title="Rebuild Semantic Vector Index for this KB"
            >
              <RefreshCw size={14} className={isIndexing ? 'loader-spinner' : ''} />
              <span>{indexStatus || 'Index KB'}</span>
            </button>
          )}

          {/* Multi-Theme Selector */}
          <div className="theme-selector-container">
            <select 
              value={theme} 
              onChange={(e) => setTheme(e.target.value)}
              className="theme-dropdown"
              title="Select Theme"
            >
              <option value="dark">Dark Theme</option>
              <option value="light">Light Theme</option>
              <option value="cyberpunk">Cyberpunk</option>
              <option value="catppuccin">Catppuccin</option>
            </select>
          </div>

          {/* Toggle Chat (Only show if API key is active) */}
          {hasApiKey && (
            <button 
              onClick={() => setIsChatOpen(!isChatOpen)} 
              className={`icon-btn ${isChatOpen ? 'secondary-btn' : ''}`}
              title="Toggle AI Assistant"
              style={isChatOpen ? { backgroundColor: 'var(--hover-bg)' } : {}}
            >
              <MessageSquare size={16} />
            </button>
          )}
        </div>
      </header>

      {/* Main Workspace Layout */}
      <main className={`app-workspace ${isChatOpen && hasApiKey ? 'chat-open' : ''}`}>
        {/* Sidebar Nav */}
        <Sidebar 
          navItems={navItems} 
          activeDoc={activeDoc} 
          onSelectDoc={setActiveDoc} 
        />

        {/* Document Reader */}
        <DocReader 
          activeDoc={activeDoc} 
          docContent={docContent} 
          isLoading={docLoading} 
          onSelectDoc={setActiveDoc}
          selectedKb={selectedKb}
        />

        {/* AI Chat Agent (Only render if key is active) */}
        {isChatOpen && hasApiKey && (
          <ChatPanel 
            messages={messages} 
            onSendMessage={handleSendMessage} 
            isGenerating={isGenerating} 
            onSelectDoc={setActiveDoc}
          />
        )}
      </main>
    </div>
  );
};

export default App;
