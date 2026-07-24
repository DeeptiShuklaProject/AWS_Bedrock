import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import DocReader from './components/DocReader';
import TableOfContents from './components/TableOfContents';
import SearchModal from './components/SearchModal';
import ImageViewerModal from './components/ImageViewerModal';
import QuizModule from './components/QuizModule';
import HeroLandingPage from './components/HeroLandingPage';
import ChatPanel from './components/ChatPanel';
import CodePlaygroundModal from './components/CodePlaygroundModal';
import { Sparkles, X } from 'lucide-react';

const App = () => {
  const [theme, setTheme] = useState('dark');
  const [kbs, setKbs] = useState([]);
  const [selectedKb, setSelectedKb] = useState('');
  
  const [activeView, setActiveView] = useState('home');
  const [navItems, setNavItems] = useState([]);
  const [activeDoc, setActiveDoc] = useState('');
  const [docContent, setDocContent] = useState('');
  const [docLoading, setDocLoading] = useState(false);
  
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isPlaygroundOpen, setIsPlaygroundOpen] = useState(false);
  const [playgroundInitialCode, setPlaygroundInitialCode] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);
  const [isChatOpen, setIsChatOpen] = useState(false);

  const [docHeadings, setDocHeadings] = useState([]);
  const [activeHeadingId, setActiveHeadingId] = useState('');
  const [readingProgress, setReadingProgress] = useState(0);

  // Dynamic Theme Handler (Dark / Light)
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('kb-theme', theme);
  }, [theme]);

  // Global Keyboard Shortcut listener (Cmd+K / Ctrl+K)
  useEffect(() => {
    const handleGlobalKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsSearchOpen(prev => !prev);
      }
    };
    window.addEventListener('keydown', handleGlobalKeyDown);
    return () => window.removeEventListener('keydown', handleGlobalKeyDown);
  }, []);

  // Track Scroll Progress & Active Heading
  useEffect(() => {
    const handleScroll = () => {
      const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
      if (totalHeight > 0) {
        const progress = (window.scrollY / totalHeight) * 100;
        setReadingProgress(Math.min(Math.max(progress, 0), 100));
      }

      if (docHeadings.length > 0) {
        const scrollPos = window.scrollY + 120;
        for (let i = docHeadings.length - 1; i >= 0; i--) {
          const el = document.getElementById(docHeadings[i].id);
          if (el && el.offsetTop <= scrollPos) {
            setActiveHeadingId(docHeadings[i].id);
            break;
          }
        }
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [docHeadings]);

  // Sync state with URL Search Parameters
  useEffect(() => {
    if (!selectedKb) return;
    localStorage.setItem('kb-selected-id', selectedKb);
    
    const url = new URL(window.location.href);
    const urlKb = url.searchParams.get('kb');
    const urlDoc = url.searchParams.get('doc');
    
    let changed = false;
    if (urlKb !== selectedKb) {
      url.searchParams.set('kb', selectedKb);
      changed = true;
    }
    
    if (activeView === 'doc' && activeDoc) {
      if (urlDoc !== activeDoc) {
        url.searchParams.set('doc', activeDoc);
        changed = true;
      }
    } else {
      if (urlDoc) {
        url.searchParams.delete('doc');
        changed = true;
      }
    }
    
    if (changed) {
      window.history.replaceState({}, '', url.toString());
    }
  }, [selectedKb, activeDoc, activeView]);

  // Fetch Knowledge Bases List
  useEffect(() => {
    const fetchKbs = async () => {
      try {
        const response = await fetch('/api/kbs');
        const data = await response.json();
        setKbs(Array.isArray(data) ? data : []);

        if (Array.isArray(data) && data.length > 0) {
          const params = new URLSearchParams(window.location.search);
          const urlKb = params.get('kb');
          const urlDoc = params.get('doc');
          const hasUrlKb = data.some(kb => kb.id === urlKb);
          
          if (hasUrlKb) {
            setSelectedKb(urlKb);
            if (urlDoc) {
              setActiveDoc(urlDoc);
              setActiveView('doc');
            }
          } else {
            const cachedKb = localStorage.getItem('kb-selected-id');
            const hasCached = data.some(kb => kb.id === cachedKb);
            if (hasCached) {
              setSelectedKb(cachedKb);
            } else {
              const udayKb = data.find(kb => kb.id === 'Uday_AWS_Services_notes');
              setSelectedKb(udayKb ? udayKb.id : data[0].id);
            }
          }
        }
      } catch (e) {
        console.error('Failed to load knowledge bases:', e);
      }
    };

    fetchKbs();
  }, []);

  // Fetch Navigation Tree when selected KB changes
  useEffect(() => {
    if (!selectedKb) return;

    const fetchNavTree = async () => {
      try {
        const response = await fetch(`/api/kbs/${selectedKb}/navigation`);
        const data = await response.json();
        setNavItems(Array.isArray(data) ? data : []);

        const params = new URLSearchParams(window.location.search);
        const urlDoc = params.get('doc');
        if (urlDoc) {
          setActiveDoc(urlDoc);
          setActiveView('doc');
        }
      } catch (e) {
        console.error('Failed to load navigation tree:', e);
      }
    };

    fetchNavTree();
  }, [selectedKb]);

  // Fetch Document Content when activeDoc or selectedKb changes
  useEffect(() => {
    if (!selectedKb || !activeDoc || activeView !== 'doc') return;

    const fetchDocContent = async () => {
      setDocLoading(true);
      try {
        const encodedDocPath = encodeURIComponent(activeDoc);
        const response = await fetch(`/api/kbs/${selectedKb}/document?path=${encodedDocPath}`);
        if (response.ok) {
          const data = await response.json();
          setDocContent(data.content || '');
        } else {
          setDocContent(`# Error Loading Document\n\nFailed to load content for \`${activeDoc}\`.`);
        }
      } catch (e) {
        setDocContent(`# Error Loading Document\n\nNetwork or server error: ${e.message}`);
      } finally {
        setDocLoading(false);
      }
    };

    fetchDocContent();
  }, [selectedKb, activeDoc, activeView]);

  const handleSelectDoc = (docPath) => {
    setActiveDoc(docPath);
    setActiveView('doc');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSelectHeading = (headingId) => {
    let el = document.getElementById(headingId);
    if (!el) {
      const headings = document.querySelectorAll('.doc-content h1, .doc-content h2, .doc-content h3, .doc-content h4');
      for (const h of headings) {
        if (h.id === headingId || h.id.toLowerCase() === headingId.toLowerCase()) {
          el = h;
          break;
        }
      }
    }
    if (el) {
      const topOffset = el.getBoundingClientRect().top + window.scrollY - 95;
      window.scrollTo({ top: topOffset, behavior: 'smooth' });
    }
  };

  const handleOpenPlaygroundWithCode = (codeSnippet) => {
    setPlaygroundInitialCode(codeSnippet || '');
    setIsPlaygroundOpen(true);
  };

  return (
    <div className="app-layout">
      {/* Top Reading Progress Bar */}
      {activeView === 'doc' && (
        <div 
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            height: '3px',
            background: 'var(--primary-gradient)',
            width: `${readingProgress}%`,
            zIndex: 50,
            transition: 'width 0.15s ease'
          }}
        />
      )}

      {/* Top Navbar */}
      <Navbar
        kbs={kbs}
        selectedKb={selectedKb}
        onSelectKb={(kbId) => {
          setSelectedKb(kbId);
          setActiveView('home');
        }}
        onOpenSearch={() => setIsSearchOpen(true)}
        onOpenQuizzes={() => setActiveView('quizzes')}
        onOpenPlayground={() => handleOpenPlaygroundWithCode('')}
        activeView={activeView}
        setActiveView={setActiveView}
        theme={theme}
        setTheme={setTheme}
      />

      {/* Main Workspace Layout */}
      <div className="main-workspace">
        {/* Left Sidebar */}
        <Sidebar
          navItems={navItems}
          activeDoc={activeDoc}
          onSelectDoc={handleSelectDoc}
          onOpenQuizzes={() => setActiveView('quizzes')}
        />

        {/* Central Canvas Area */}
        <main className={`canvas-area ${activeView === 'doc' ? 'has-toc' : ''}`}>
          {activeView === 'home' && (
            <HeroLandingPage
              navItems={navItems}
              onOpenSearch={() => setIsSearchOpen(true)}
              onOpenQuizzes={() => setActiveView('quizzes')}
              onOpenPlayground={() => handleOpenPlaygroundWithCode('')}
              onSelectDoc={handleSelectDoc}
            />
          )}

          {activeView === 'quizzes' && (
            <QuizModule
              onBackToDocs={() => setActiveView('home')}
            />
          )}

          {activeView === 'doc' && (
            <div style={{ display: 'flex', width: '100%', gap: '28px' }}>
              <DocReader
                activeDoc={activeDoc}
                docContent={docContent}
                isLoading={docLoading}
                onSelectDoc={handleSelectDoc}
                navItems={navItems}
                onExtractHeadings={setDocHeadings}
                onOpenImage={(src, alt) => setSelectedImage({ src, alt })}
                onOpenPlayground={handleOpenPlaygroundWithCode}
              />

              <TableOfContents
                headings={docHeadings}
                activeHeadingId={activeHeadingId}
                onSelectHeading={handleSelectHeading}
              />
            </div>
          )}
        </main>

        {/* Floating AI Chat Assistant Toggle */}
        <button
          onClick={() => setIsChatOpen(prev => !prev)}
          style={{
            position: 'fixed',
            bottom: '24px',
            right: '24px',
            zIndex: 40,
            background: isChatOpen ? 'var(--accent-rose)' : 'var(--primary-gradient)',
            color: '#fff',
            border: 'none',
            borderRadius: '16px',
            padding: '12px 20px',
            fontWeight: 800,
            fontSize: '0.88rem',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            boxShadow: 'var(--shadow-lg)'
          }}
        >
          {isChatOpen ? <X size={18} /> : <Sparkles size={18} />}
          <span>{isChatOpen ? 'Close Chat' : 'Ask AI Agent'}</span>
        </button>

        {/* AI Chat Drawer */}
        {isChatOpen && (
          <div 
            style={{
              position: 'fixed',
              bottom: '80px',
              right: '24px',
              zIndex: 40,
              width: '400px',
              height: '560px',
              borderRadius: '24px',
              background: 'var(--bg-card)',
              border: '1px solid var(--border-color)',
              boxShadow: 'var(--shadow-lg)',
              overflow: 'hidden'
            }}
          >
            <ChatPanel
              selectedKb={selectedKb}
              activeDoc={activeDoc}
              onClose={() => setIsChatOpen(false)}
              onSelectDoc={handleSelectDoc}
            />
          </div>
        )}
      </div>

      {/* Modals */}
      <SearchModal
        isOpen={isSearchOpen}
        onClose={() => setIsSearchOpen(false)}
        navItems={navItems}
        onSelectDoc={handleSelectDoc}
      />

      <CodePlaygroundModal
        isOpen={isPlaygroundOpen}
        initialCode={playgroundInitialCode}
        onClose={() => setIsPlaygroundOpen(false)}
      />

      <ImageViewerModal
        src={selectedImage?.src}
        alt={selectedImage?.alt}
        onClose={() => setSelectedImage(null)}
      />
    </div>
  );
};

export default App;
