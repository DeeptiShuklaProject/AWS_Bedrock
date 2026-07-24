import React, { useState } from 'react';
import { List, Link as LinkIcon, Check } from 'lucide-react';

const TableOfContents = ({ headings = [], activeHeadingId, onSelectHeading }) => {
  const [copiedId, setCopiedId] = useState(null);

  const handleCopyLink = (e, headingId) => {
    e.stopPropagation();
    const url = `${window.location.origin}${window.location.pathname}${window.location.search}#${headingId}`;
    navigator.clipboard.writeText(url);
    setCopiedId(headingId);
    setTimeout(() => setCopiedId(null), 2000);
  };

  if (!headings || headings.length === 0) return null;

  return (
    <aside className="toc-panel">
      <div className="toc-card">
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px', paddingBottom: '8px', borderBottom: '1px solid var(--border-color)' }}>
          <List size={15} style={{ color: 'var(--accent-indigo)' }} />
          <h4 className="toc-title" style={{ margin: 0 }}>On This Page</h4>
        </div>

        <nav style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
          {headings.map((item, idx) => {
            const isActive = activeHeadingId === item.id;
            const isSubheading = item.level === 3;

            return (
              <div
                key={`${item.id}-${idx}`}
                onClick={() => onSelectHeading(item.id)}
                className={`toc-item ${isActive ? 'active' : ''}`}
                style={{ paddingLeft: isSubheading ? '14px' : '8px' }}
              >
                <span>{item.text}</span>
              </div>
            );
          })}
        </nav>
      </div>
    </aside>
  );
};

export default TableOfContents;
