import React, { useState } from 'react';
import { ChevronRight, FileText, Folder, FolderOpen } from 'lucide-react';

// Recursive item renderer for the navigation tree
const SidebarNode = ({ item, activeDoc, onSelectDoc, level = 0 }) => {
  const { title, href, contents } = item;
  const isFolder = !!contents && contents.length > 0;
  
  const [isExpanded, setIsExpanded] = useState(false);

  const handleToggle = (e) => {
    e.stopPropagation();
    setIsExpanded(!isExpanded);
  };

  const handleClick = (e) => {
    e.stopPropagation();
    if (isFolder) {
      setIsExpanded(!isExpanded);
      // If the folder has an associated page (like index.md), load it
      if (href) {
        onSelectDoc(href);
      }
    } else if (href) {
      onSelectDoc(href);
    }
  };

  const isActive = href && activeDoc === href;

  return (
    <div className="nav-node" style={{ paddingLeft: level > 0 ? '6px' : '0' }}>
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
              <FolderOpen size={16} className="folder-icon" />
            ) : (
              <Folder size={16} className="folder-icon" />
            )}
          </>
        ) : (
          <FileText size={16} className="file-icon" />
        )}
        
        <span className="node-title-text" title={title}>
          {title}
        </span>
      </div>

      {isFolder && isExpanded && (
        <div className="node-children">
          {contents.map((child, index) => (
            <SidebarNode 
              key={index} 
              item={child} 
              activeDoc={activeDoc} 
              onSelectDoc={onSelectDoc} 
              level={level + 1}
            />
          ))}
        </div>
      )}
    </div>
  );
};

const Sidebar = ({ navItems, activeDoc, onSelectDoc }) => {
  return (
    <div className="sidebar-panel">
      <div className="sidebar-header">
        Navigation
      </div>
      <div className="nav-tree-container">
        {navItems && navItems.length > 0 ? (
          navItems.map((item, index) => (
            <SidebarNode 
              key={index} 
              item={item} 
              activeDoc={activeDoc} 
              onSelectDoc={onSelectDoc} 
            />
          ))
        ) : (
          <div className="sidebar-empty" style={{ padding: '20px', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
            No documentation pages found.
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar;
