import React from 'react';
import { 
  BookOpen, 
  Search, 
  Sun, 
  Moon, 
  Award, 
  Menu, 
  Layers,
  Terminal
} from 'lucide-react';

const Navbar = ({
  kbs = [],
  selectedKb,
  onSelectKb,
  onOpenSearch,
  onOpenQuizzes,
  onOpenPlayground,
  activeView,
  setActiveView,
  theme,
  setTheme,
  onToggleMobileSidebar
}) => {
  return (
    <header className="top-navbar">
      {/* Brand Section */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <button 
          onClick={onToggleMobileSidebar}
          style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer', display: 'none' }}
          className="mobile-menu-btn"
        >
          <Menu size={20} />
        </button>

        <button 
          onClick={() => setActiveView('home')}
          className="nav-brand"
        >
          <div className="brand-icon-box">
            <div className="brand-icon-inner">
              <BookOpen size={20} />
            </div>
          </div>
          <div className="brand-title-group">
            <div className="brand-title">
              AuraDocs <span className="brand-badge">PRO</span>
            </div>
            <div className="brand-subtitle">Interactive Developer Portal</div>
          </div>
        </button>
      </div>

      {/* Global Quick Search Button */}
      <button onClick={onOpenSearch} className="header-search-btn">
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Search size={16} style={{ color: 'var(--accent-indigo)' }} />
          <span>Search docs, guides, code & terms...</span>
        </div>
        <kbd className="search-shortcut-kbd">ctrl K</kbd>
      </button>

      {/* Right Action Controls */}
      <div className="nav-actions">
        {/* KB Picker */}
        {kbs.length > 0 && (
          <div className="kb-select-pill">
            <Layers size={14} style={{ color: 'var(--accent-indigo)' }} />
            <select
              value={selectedKb}
              onChange={(e) => onSelectKb(e.target.value)}
            >
              {kbs.map((kb) => (
                <option key={kb.id} value={kb.id} style={{ background: '#1e293b', color: '#fff' }}>
                  {kb.name}
                </option>
              ))}
            </select>
          </div>
        )}

        {/* Interactive Code Playground Button */}
        <button 
          onClick={onOpenPlayground} 
          className="secondary-cta-btn" 
          style={{ padding: '10px 18px', fontSize: '0.88rem', borderColor: 'var(--accent-cyan)', color: 'var(--accent-cyan)' }}
        >
          <Terminal size={16} />
          <span>Code Playground</span>
        </button>

        {/* Practice Quizzes Launch Button */}
        <button onClick={onOpenQuizzes} className="quiz-launch-btn">
          <Award size={16} />
          <span>Quizzes</span>
          <span style={{ fontSize: '0.65rem', background: 'rgba(255,255,255,0.2)', padding: '1px 6px', borderRadius: '10px' }}>
            20+ Qs
          </span>
        </button>

        {/* Theme Toggle Button */}
        <button
          onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
          className="theme-toggle-btn"
          title="Toggle Theme"
        >
          {theme === 'dark' ? <Sun size={18} style={{ color: '#f59e0b' }} /> : <Moon size={18} style={{ color: '#6366f1' }} />}
        </button>
      </div>
    </header>
  );
};

export default Navbar;
