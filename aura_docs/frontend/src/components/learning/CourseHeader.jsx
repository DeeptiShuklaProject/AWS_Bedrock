import React, { useState, useEffect } from 'react';
import { 
  Clock, 
  BarChart2, 
  CheckCircle2, 
  Bookmark, 
  Share2, 
  List, 
  Sparkles, 
  Target, 
  Check, 
  Zap, 
  BookOpen 
} from 'lucide-react';

export const CourseHeader = ({ 
  title, 
  docPath, 
  wordCount = 1200, 
  headings = [], 
  onSelectHeading 
}) => {
  const readingTime = Math.max(2, Math.ceil(wordCount / 200));
  
  // Storage keys based on doc path
  const bookmarkKey = `auradocs_bookmark_${docPath}`;
  const completeKey = `auradocs_complete_${docPath}`;

  const [isBookmarked, setIsBookmarked] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);
  const [copied, setCopied] = useState(false);
  const [showTocDropdown, setShowTocDropdown] = useState(false);

  useEffect(() => {
    if (!docPath) return;
    setIsBookmarked(localStorage.getItem(bookmarkKey) === 'true');
    setIsCompleted(localStorage.getItem(completeKey) === 'true');
  }, [docPath]);

  const toggleBookmark = () => {
    const next = !isBookmarked;
    setIsBookmarked(next);
    localStorage.setItem(bookmarkKey, next ? 'true' : 'false');
  };

  const toggleCompleted = () => {
    const next = !isCompleted;
    setIsCompleted(next);
    localStorage.setItem(completeKey, next ? 'true' : 'false');
  };

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Extract chapter number if present
  const chapterMatch = title ? title.match(/Chapter[_-](\d+)/i) : null;
  const chapterNum = chapterMatch ? `CHAPTER ${chapterMatch[1]}` : 'LEARNING MODULE';
  const cleanTitle = title ? title.replace(/Chapter[_-]\d+[_-]?/i, '').replace(/_/g, ' ') : 'Module Overview';

  return (
    <div className="course-header-container">
      {/* Top Meta Header Bar */}
      <div className="course-meta-top">
        <div className="badge-group">
          <span className="chapter-badge">
            <BookOpen size={13} />
            {chapterNum}
          </span>
          <span className="difficulty-badge">
            <BarChart2 size={13} />
            ADVANCED
          </span>
          <span className="reading-time-badge">
            <Clock size={13} />
            {readingTime} MIN READ
          </span>
        </div>

        <div className="course-header-actions">
          <button 
            onClick={toggleCompleted}
            className={`action-pill ${isCompleted ? 'completed' : ''}`}
            title={isCompleted ? "Marked as completed" : "Mark chapter as complete"}
          >
            <CheckCircle2 size={15} />
            <span>{isCompleted ? "Completed" : "Mark Complete"}</span>
          </button>

          <button 
            onClick={toggleBookmark}
            className={`action-pill ${isBookmarked ? 'bookmarked' : ''}`}
            title="Bookmark this chapter"
          >
            <Bookmark size={15} fill={isBookmarked ? "currentColor" : "none"} />
            <span>{isBookmarked ? "Bookmarked" : "Bookmark"}</span>
          </button>

          <button 
            onClick={handleShare}
            className="action-pill"
            title="Share URL"
          >
            {copied ? <Check size={15} color="#10b981" /> : <Share2 size={15} />}
            <span>{copied ? "Copied!" : "Share"}</span>
          </button>
        </div>
      </div>

      {/* Chapter Main Title */}
      <h1 className="course-main-title">
        {cleanTitle}
      </h1>

      {/* Interactive Overview Card */}
      <div className="course-overview-card">
        <div className="overview-grid">
          <div className="overview-col">
            <div className="col-header">
              <Target size={16} className="text-accent" />
              <span>Skills You'll Master</span>
            </div>
            <ul className="skills-list">
              <li><Zap size={13} /> Bedrock AgentCore Architecture & Execution</li>
              <li><Zap size={13} /> Multi-Agent Orchestration & Tool Use</li>
              <li><Zap size={13} /> Production Enterprise Patterns</li>
            </ul>
          </div>

          <div className="overview-col">
            <div className="col-header">
              <Sparkles size={16} className="text-accent" />
              <span>Key Learning Objectives</span>
            </div>
            <ul className="objectives-list">
              <li>Understand runtime isolation & memory models</li>
              <li>Deploy code-first agentic infrastructure</li>
              <li>Implement observability & compliance controls</li>
            </ul>
          </div>
        </div>

        {/* Navigation & TOC bar */}
        {headings.length > 0 && (
          <div className="header-toc-bar">
            <div className="toc-title">
              <List size={15} />
              <span>Chapter Navigation ({headings.length} Sections)</span>
            </div>
            <div className="toc-chips-scroll">
              {headings.slice(0, 6).map((h, i) => (
                <button 
                  key={i} 
                  onClick={() => onSelectHeading && onSelectHeading(h.id)}
                  className="toc-chip"
                >
                  {h.text}
                </button>
              ))}
              {headings.length > 6 && (
                <span className="toc-more">+{headings.length - 6} more</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
