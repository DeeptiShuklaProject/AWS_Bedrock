import React, { useState, useEffect } from 'react';
import { 
  ArrowUp, 
  List, 
  HelpCircle, 
  Keyboard, 
  X, 
  ChevronRight 
} from 'lucide-react';

export const PageExperienceControls = ({ headings = [], onSelectHeading }) => {
  const [scrollPercent, setScrollPercent] = useState(0);
  const [showBackToTop, setShowBackToTop] = useState(false);
  const [activeHeadingId, setActiveHeadingId] = useState('');
  const [showShortcuts, setShowShortcuts] = useState(false);

  useEffect(() => {
    const docPanel = document.querySelector('.doc-panel');
    if (!docPanel) return;

    const handleScroll = () => {
      const scrollTop = docPanel.scrollTop;
      const scrollHeight = docPanel.scrollHeight - docPanel.clientHeight;
      const progress = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
      setScrollPercent(progress);
      setShowBackToTop(scrollTop > 300);

      // Detect active heading based on scroll position
      if (headings.length > 0) {
        for (let i = headings.length - 1; i >= 0; i--) {
          const el = document.getElementById(headings[i].id);
          if (el) {
            const rect = el.getBoundingClientRect();
            if (rect.top <= 180) {
              setActiveHeadingId(headings[i].id);
              break;
            }
          }
        }
      }
    };

    docPanel.addEventListener('scroll', handleScroll);
    return () => docPanel.removeEventListener('scroll', handleScroll);
  }, [headings]);

  // Keyboard navigation shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;

      const docPanel = document.querySelector('.doc-panel');
      if (!docPanel) return;

      if (e.key === 'j' || e.key === 'ArrowDown') {
        docPanel.scrollBy({ top: 120, behavior: 'smooth' });
      } else if (e.key === 'k' || e.key === 'ArrowUp') {
        docPanel.scrollBy({ top: -120, behavior: 'smooth' });
      } else if (e.key === '?') {
        setShowShortcuts(prev => !prev);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const scrollToTop = () => {
    const docPanel = document.querySelector('.doc-panel');
    if (docPanel) {
      docPanel.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  return (
    <>
      {/* Top Scroll Progress Indicator */}
      <div className="top-scroll-progress-bar" style={{ width: `${scrollPercent}%` }} />

      {/* Floating Floating TOC Side Navigator */}
      {headings.length > 0 && (
        <aside className="sticky-toc-navigator">
          <div className="sticky-toc-header">
            <List size={13} />
            <span>ON THIS PAGE</span>
          </div>
          <nav className="sticky-toc-list">
            {headings.map((h, i) => {
              const isActive = h.id === activeHeadingId;
              return (
                <button
                  key={i}
                  onClick={() => onSelectHeading && onSelectHeading(h.id)}
                  className={`sticky-toc-item ${isActive ? 'active' : ''} level-${h.level || 2}`}
                >
                  <ChevronRight size={11} className="toc-item-arrow" />
                  <span className="toc-item-text">{h.text}</span>
                </button>
              );
            })}
          </nav>
        </aside>
      )}

      {/* Floating Controls (Back to top & Shortcuts) */}
      <div className="floating-page-controls">
        <button 
          onClick={() => setShowShortcuts(true)} 
          className="floating-btn"
          title="Keyboard Shortcuts (?)"
        >
          <Keyboard size={16} />
        </button>

        {showBackToTop && (
          <button 
            onClick={scrollToTop} 
            className="floating-btn top-btn"
            title="Back to Top"
          >
            <ArrowUp size={16} />
          </button>
        )}
      </div>

      {/* Keyboard Shortcuts Modal */}
      {showShortcuts && (
        <div className="shortcuts-modal-overlay" onClick={() => setShowShortcuts(false)}>
          <div className="shortcuts-modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <div className="modal-title">
                <Keyboard size={18} />
                <span>Keyboard Shortcuts</span>
              </div>
              <button onClick={() => setShowShortcuts(false)} className="modal-close">
                <X size={16} />
              </button>
            </div>
            <div className="shortcuts-list">
              <div className="shortcut-row">
                <kbd>J</kbd> / <kbd>↓</kbd>
                <span>Scroll Down</span>
              </div>
              <div className="shortcut-row">
                <kbd>K</kbd> / <kbd>↑</kbd>
                <span>Scroll Up</span>
              </div>
              <div className="shortcut-row">
                <kbd>?</kbd>
                <span>Toggle Keyboard Shortcuts</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
