import React, { useState } from 'react';
import { ChevronRight, FileText, Folder, FolderOpen, Star, Bookmark } from 'lucide-react';

// Recursive item renderer for the navigation tree
const SidebarNode = ({ 
  item, 
  activeDoc, 
  onSelectDoc, 
  completedDocs, 
  bookmarkedDocs, 
  toggleDocCompleted, 
  toggleDocBookmarked,
  level = 0 
}) => {
  const { title, href, contents } = item;
  const isFolder = !!contents && contents.length > 0;
  
  const [isExpanded, setIsExpanded] = useState(true); // default to expanded for better navigation

  const handleToggle = (e) => {
    e.stopPropagation();
    setIsExpanded(!isExpanded);
  };

  const handleClick = (e) => {
    e.stopPropagation();
    if (isFolder) {
      setIsExpanded(!isExpanded);
      if (href) {
        onSelectDoc(href);
      }
    } else if (href) {
      onSelectDoc(href);
    }
  };

  // Helper to extract leaves
  const getLeafNodes = (node) => {
    const list = [];
    const traverse = (x) => {
      if (!x) return;
      if (x.href) list.push(x);
      if (x.contents && x.contents.length > 0) {
        x.contents.forEach(traverse);
      }
    };
    traverse(node);
    return list;
  };

  const leafNodes = isFolder ? getLeafNodes(item) : [];
  const completedLeaves = leafNodes.filter(l => completedDocs[l.href]);
  const isCompleted = href && completedDocs[href];
  const isBookmarked = href && bookmarkedDocs[href];
  const isActive = href && activeDoc === href;

  return (
    <div className="nav-node" style={{ paddingLeft: level > 0 ? '8px' : '0' }}>
      <div 
        className={`node-header ${isActive ? 'active-link' : ''}`}
        onClick={handleClick}
      >
        {isFolder ? (
          <>
            <span className={`node-arrow-container`} onClick={handleToggle}>
              <ChevronRight 
                size={14} 
                className={`node-arrow ${isExpanded ? 'expanded' : ''}`} 
              />
            </span>
            {isExpanded ? (
              <FolderOpen size={15} className="folder-icon" />
            ) : (
              <Folder size={15} className="folder-icon" />
            )}
          </>
        ) : (
          <div className="node-left-actions" onClick={e => e.stopPropagation()}>
            <input 
              type="checkbox" 
              checked={!!isCompleted} 
              onChange={() => toggleDocCompleted(href)}
              className="sidebar-checkbox"
              title="Mark as completed"
            />
          </div>
        )}
        
        <span className="node-title-text" title={title}>
          {title}
        </span>

        {isFolder && leafNodes.length > 0 && (
          <span className="folder-completion-badge">
            {completedLeaves.length}/{leafNodes.length}
          </span>
        )}

        {!isFolder && (
          <button 
            className={`sidebar-bookmark-btn ${isBookmarked ? 'is-active' : ''}`}
            onClick={(e) => { e.stopPropagation(); toggleDocBookmarked(href); }}
            title={isBookmarked ? 'Remove bookmark' : 'Bookmark topic'}
          >
            <Star size={12} className={isBookmarked ? 'filled-star' : 'empty-star'} />
          </button>
        )}
      </div>

      {isFolder && isExpanded && (
        <div className="node-children">
          {contents.map((child, index) => (
            <SidebarNode 
              key={index} 
              item={child} 
              activeDoc={activeDoc} 
              onSelectDoc={onSelectDoc} 
              completedDocs={completedDocs}
              bookmarkedDocs={bookmarkedDocs}
              toggleDocCompleted={toggleDocCompleted}
              toggleDocBookmarked={toggleDocBookmarked}
              level={level + 1}
            />
          ))}
        </div>
      )}
    </div>
  );
};

const Sidebar = ({ 
  navItems, 
  activeDoc, 
  onSelectDoc, 
  completedDocs, 
  bookmarkedDocs, 
  recentlyViewedDocs, 
  toggleDocCompleted, 
  toggleDocBookmarked 
}) => {
  const [isBookmarksExpanded, setIsBookmarksExpanded] = useState(true);
  const [isRecentExpanded, setIsRecentExpanded] = useState(true);

  // Helper to extract leaf nodes
  const getLeafNodes = (node) => {
    const list = [];
    const traverse = (x) => {
      if (!x) return;
      if (x.href) list.push(x);
      if (x.contents && x.contents.length > 0) {
        x.contents.forEach(traverse);
      }
    };
    traverse(node);
    return list;
  };

  // Progress Calculations
  const allLeafNodes = navItems ? navItems.reduce((acc, item) => [...acc, ...getLeafNodes(item)], []) : [];
  const totalCompleted = allLeafNodes.filter(l => completedDocs[l.href]).length;
  const overallPercentage = allLeafNodes.length > 0 ? Math.round((totalCompleted / allLeafNodes.length) * 100) : 0;

  return (
    <div className="sidebar-panel">
      <div className="sidebar-header">
        Navigation
      </div>

      {/* Dynamic Course Progress Bar */}
      <div className="sidebar-progress-container">
        <div className="sidebar-progress-text">
          <span>Course Progress</span>
          <span className="progress-value">{overallPercentage}%</span>
        </div>
        <div className="sidebar-progress-track">
          <div className="sidebar-progress-fill" style={{ width: `${overallPercentage}%` }}></div>
        </div>
        <div className="sidebar-progress-subtext">
          {totalCompleted} of {allLeafNodes.length} modules complete
        </div>
      </div>

      {/* Bookmarks Section */}
      {Object.keys(bookmarkedDocs).length > 0 && (
        <div className="sidebar-special-section">
          <div className="special-section-header" onClick={() => setIsBookmarksExpanded(!isBookmarksExpanded)}>
            <div className="header-title">
              <Bookmark size={12} className="icon-blue" />
              <span>Bookmarks ({Object.keys(bookmarkedDocs).length})</span>
            </div>
            <ChevronRight size={12} className={`section-arrow ${isBookmarksExpanded ? 'expanded' : ''}`} />
          </div>
          {isBookmarksExpanded && (
            <div className="special-section-list">
              {allLeafNodes.filter(n => bookmarkedDocs[n.href]).map((node, i) => (
                <div 
                  key={i} 
                  className={`special-item ${activeDoc === node.href ? 'active' : ''}`}
                  onClick={() => onSelectDoc(node.href)}
                >
                  <Star size={10} className="filled-star" />
                  <span className="special-item-text">{node.title}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Recently Viewed Section */}
      {recentlyViewedDocs.length > 0 && (
        <div className="sidebar-special-section">
          <div className="special-section-header" onClick={() => setIsRecentExpanded(!isRecentExpanded)}>
            <div className="header-title">
              <FileText size={12} className="icon-purple" />
              <span>Recently Viewed</span>
            </div>
            <ChevronRight size={12} className={`section-arrow ${isRecentExpanded ? 'expanded' : ''}`} />
          </div>
          {isRecentExpanded && (
            <div className="special-section-list">
              {recentlyViewedDocs.map((href, i) => {
                const node = allLeafNodes.find(n => n.href === href);
                if (!node) return null;
                return (
                  <div 
                    key={i} 
                    className={`special-item ${activeDoc === href ? 'active' : ''}`}
                    onClick={() => onSelectDoc(href)}
                  >
                    <span className="special-item-dot"></span>
                    <span className="special-item-text">{node.title}</span>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

      {/* Main Navigation Tree */}
      <div className="nav-tree-container">
        {navItems && navItems.length > 0 ? (
          navItems.map((item, index) => (
            <SidebarNode 
              key={index} 
              item={item} 
              activeDoc={activeDoc} 
              onSelectDoc={onSelectDoc} 
              completedDocs={completedDocs}
              bookmarkedDocs={bookmarkedDocs}
              toggleDocCompleted={toggleDocCompleted}
              toggleDocBookmarked={toggleDocBookmarked}
            />
          ))
        ) : (
          <div className="sidebar-empty">
            No documentation pages found.
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar;
