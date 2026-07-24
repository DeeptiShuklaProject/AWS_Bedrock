import React, { useState, useEffect, useRef } from 'react';
import { 
  ChevronRight, 
  FileText, 
  Folder, 
  FolderOpen, 
  Filter, 
  X,
  Award
} from 'lucide-react';

const SidebarNode = ({ item, activeDoc, onSelectDoc, filterQuery = '', level = 0 }) => {
  const nodeTitle = item.title || item.name || 'Untitled';
  const nodeHref = item.href || item.path || '';
  const nodeChildren = item.contents || item.children || [];
  const isFolder = nodeChildren.length > 0 || item.type === 'directory';

  const [isExpanded, setIsExpanded] = useState(() => {
    if (filterQuery) return true;
    if (activeDoc && nodeHref && activeDoc.startsWith(nodeHref)) return true;
    return level === 0;
  });

  const nodeRef = useRef(null);
  const isActive = nodeHref && activeDoc === nodeHref;

  useEffect(() => {
    if (filterQuery) setIsExpanded(true);
  }, [filterQuery]);

  useEffect(() => {
    if (isActive) {
      setIsExpanded(true);
      nodeRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }, [isActive]);

  const matchesFilter = (node) => {
    if (!filterQuery) return true;
    const t = node.title || node.name || '';
    if (t.toLowerCase().includes(filterQuery.toLowerCase())) return true;
    const kids = node.contents || node.children || [];
    return kids.some(child => matchesFilter(child));
  };

  if (filterQuery && !matchesFilter(item)) return null;

  const handleClick = (e) => {
    e.stopPropagation();
    if (isFolder) {
      setIsExpanded(!isExpanded);
      if (nodeHref) onSelectDoc(nodeHref);
    } else if (nodeHref) {
      onSelectDoc(nodeHref);
    }
  };

  return (
    <div style={{ paddingLeft: level > 0 ? '12px' : '0' }}>
      <div 
        ref={nodeRef}
        onClick={handleClick}
        className={`tree-node-row ${isActive ? 'active' : ''}`}
      >
        {isFolder ? (
          <ChevronRight 
            size={14} 
            style={{ 
              transform: isExpanded ? 'rotate(90deg)' : 'rotate(0deg)', 
              transition: 'transform 0.15s ease',
              color: 'var(--accent-indigo)'
            }} 
          />
        ) : (
          <FileText size={14} style={{ color: isActive ? 'var(--accent-indigo)' : 'var(--text-muted)' }} />
        )}
        
        {isFolder && (
          isExpanded ? (
            <FolderOpen size={15} style={{ color: 'var(--accent-cyan)' }} />
          ) : (
            <Folder size={15} style={{ color: 'var(--accent-indigo)' }} />
          )
        )}

        <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', flex: 1 }} title={nodeTitle}>
          {nodeTitle}
        </span>
      </div>

      {isFolder && isExpanded && (
        <div style={{ marginTop: '2px', borderLeft: '1px solid var(--border-color)', marginLeft: '12px', paddingLeft: '4px' }}>
          {nodeChildren.map((child, idx) => (
            <SidebarNode 
              key={child.href || child.path || idx} 
              item={child} 
              activeDoc={activeDoc} 
              onSelectDoc={onSelectDoc} 
              filterQuery={filterQuery}
              level={level + 1}
            />
          ))}
        </div>
      )}
    </div>
  );
};

const Sidebar = ({ navItems = [], activeDoc, onSelectDoc, onOpenQuizzes }) => {
  const [filterQuery, setFilterQuery] = useState('');

  return (
    <aside className="sidebar-panel">
      {/* Search Filter */}
      <div className="sidebar-filter-box">
        <div className="sidebar-input-wrapper">
          <Filter size={14} style={{ position: 'absolute', left: '10px', color: 'var(--text-muted)' }} />
          <input
            type="text"
            value={filterQuery}
            onChange={(e) => setFilterQuery(e.target.value)}
            placeholder="Filter documentation..."
            className="sidebar-input"
          />
          {filterQuery && (
            <button 
              onClick={() => setFilterQuery('')} 
              style={{ position: 'absolute', right: '10px', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
            >
              <X size={12} />
            </button>
          )}
        </div>
      </div>

      {/* Directory Navigation Tree */}
      <div className="sidebar-tree-container">
        {Array.isArray(navItems) && navItems.length > 0 ? (
          navItems.map((item, index) => (
            <SidebarNode 
              key={item.href || item.path || index} 
              item={item} 
              activeDoc={activeDoc} 
              onSelectDoc={onSelectDoc} 
              filterQuery={filterQuery}
            />
          ))
        ) : (
          <div style={{ padding: '24px 12px', textAlign: 'center', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            No documentation pages found.
          </div>
        )}
      </div>

      {/* Practice Quiz Promo Banner */}
      <div style={{ padding: '12px', borderTop: '1px solid var(--border-color)' }}>
        <button
          onClick={onOpenQuizzes}
          style={{
            width: '100%',
            padding: '10px 12px',
            borderRadius: '10px',
            background: 'rgba(249, 115, 22, 0.1)',
            border: '1px solid rgba(249, 115, 22, 0.3)',
            color: 'var(--accent-orange)',
            fontWeight: 700,
            fontSize: 12,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Award size={16} />
            <span>Practice Quiz</span>
          </div>
          <span style={{ background: 'rgba(249,115,22,0.2)', padding: '1px 6px', borderRadius: '6px', fontSize: '0.65rem' }}>
            20+ Qs
          </span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
