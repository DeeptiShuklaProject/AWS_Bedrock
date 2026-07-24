import React, { useState, useEffect, useRef } from 'react';
import { Search, X, FileText, Folder, CornerDownLeft, Sparkles } from 'lucide-react';

const SearchModal = ({ isOpen, onClose, navItems = [], onSelectDoc }) => {
  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef(null);

  // Flatten all document pages from navigation tree safely
  const flattenNavItems = (items, pathPrefix = '') => {
    let docs = [];
    if (!Array.isArray(items)) return docs;

    items.forEach((item) => {
      if (!item) return;
      const title = item.title || item.name || 'Untitled';
      const docPath = item.href || item.path || '';
      const currentPath = pathPrefix ? `${pathPrefix} / ${title}` : title;
      const isFile = item.type === 'file' || (docPath && !item.contents && !item.children);

      if (isFile && docPath) {
        docs.push({
          title: title,
          path: docPath,
          category: pathPrefix || 'General Docs',
          fullPathDisplay: currentPath
        });
      }

      const kids = item.contents || item.children;
      if (Array.isArray(kids) && kids.length > 0) {
        docs = docs.concat(flattenNavItems(kids, currentPath));
      }
    });

    return docs;
  };

  const allDocs = flattenNavItems(navItems);

  const searchResults = query.trim() === '' 
    ? allDocs.slice(0, 8) 
    : allDocs.filter(doc => 
        doc.title.toLowerCase().includes(query.toLowerCase()) ||
        doc.category.toLowerCase().includes(query.toLowerCase())
      ).slice(0, 15);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
      setQuery('');
      setSelectedIndex(0);
    }
  }, [isOpen]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!isOpen) return;
      if (e.key === 'Escape') {
        onClose();
      } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        setSelectedIndex(prev => (prev + 1) % (searchResults.length || 1));
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        setSelectedIndex(prev => (prev - 1 + searchResults.length) % (searchResults.length || 1));
      } else if (e.key === 'Enter' && searchResults[selectedIndex]) {
        e.preventDefault();
        onSelectDoc(searchResults[selectedIndex].path);
        onClose();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, searchResults, selectedIndex, onSelectDoc, onClose]);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="search-modal-card" onClick={(e) => e.stopPropagation()}>
        {/* Header Search Input */}
        <div className="search-modal-header">
          <Search size={20} style={{ color: 'var(--accent-indigo)' }} />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setSelectedIndex(0);
            }}
            placeholder="Type to search documentation topics, guides..."
            className="search-modal-input"
          />
          {query && (
            <button 
              onClick={() => setQuery('')}
              style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
            >
              <X size={16} />
            </button>
          )}
        </div>

        {/* Results List */}
        <div className="search-results-list">
          {searchResults.length > 0 ? (
            searchResults.map((doc, idx) => {
              const isSelected = idx === selectedIndex;
              return (
                <div
                  key={doc.path || idx}
                  onClick={() => {
                    onSelectDoc(doc.path);
                    onClose();
                  }}
                  onMouseEnter={() => setSelectedIndex(idx)}
                  className={`search-result-item ${isSelected ? 'selected' : ''}`}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <FileText size={18} style={{ color: isSelected ? 'var(--accent-indigo)' : 'var(--text-muted)' }} />
                    <div>
                      <h4 style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-primary)' }}>{doc.title}</h4>
                      <p style={{ fontSize: '0.72rem', color: 'var(--text-secondary)' }}>{doc.category}</p>
                    </div>
                  </div>

                  <CornerDownLeft size={14} style={{ color: 'var(--text-muted)' }} />
                </div>
              );
            })
          ) : (
            <div style={{ padding: '32px', textAlign: 'center', color: 'var(--text-muted)' }}>
              <Sparkles size={28} style={{ margin: '0 auto 8px auto', color: 'var(--accent-indigo)' }} />
              <p style={{ fontSize: '0.88rem', fontWeight: 600 }}>No matching documentation topics found</p>
              <p style={{ fontSize: '0.78rem', marginTop: '4px' }}>Try searching for EC2, VPC, Lambda, Bedrock, Docker...</p>
            </div>
          )}
        </div>

        {/* Footer Shortcut Hints */}
        <div style={{ padding: '10px 16px', background: 'var(--bg-surface)', borderTop: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
          <div>Use <kbd style={{ padding: '1px 5px', borderRadius: '4px', background: 'var(--bg-card)', border: '1px solid var(--border-color)' }}>↑</kbd> <kbd style={{ padding: '1px 5px', borderRadius: '4px', background: 'var(--bg-card)', border: '1px solid var(--border-color)' }}>↓</kbd> to navigate, <kbd style={{ padding: '1px 5px', borderRadius: '4px', background: 'var(--bg-card)', border: '1px solid var(--border-color)' }}>↵</kbd> to select</div>
          <div><kbd style={{ padding: '1px 5px', borderRadius: '4px', background: 'var(--bg-card)', border: '1px solid var(--border-color)' }}>ESC</kbd> to close</div>
        </div>
      </div>
    </div>
  );
};

export default SearchModal;
