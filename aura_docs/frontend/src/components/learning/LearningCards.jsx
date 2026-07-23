import React, { useState } from 'react';
import { 
  Lightbulb, 
  Sparkles, 
  CheckCircle2, 
  AlertTriangle, 
  AlertCircle, 
  Info, 
  HelpCircle, 
  ChevronDown, 
  ChevronUp, 
  ArrowRight, 
  Award, 
  ShieldCheck, 
  Zap, 
  BookOpen 
} from 'lucide-react';

// ==========================================
// 1. Concept Card Component
// ==========================================
export const ConceptCard = ({ title, children, category = 'Core Concept' }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="concept-card-wrapper">
      <div className="concept-card-header">
        <div className="concept-icon-badge">
          <Lightbulb size={18} className="text-yellow-400" />
        </div>
        <div className="concept-title-group">
          <span className="concept-category-tag">{category.toUpperCase()}</span>
          <h3 className="concept-title">{title}</h3>
        </div>
      </div>
      <div className="concept-card-body">
        {children}
      </div>
    </div>
  );
};

// ==========================================
// 2. Why It Matters Component
// ==========================================
export const WhyItMatters = ({ children }) => {
  return (
    <div className="why-it-matters-card">
      <div className="why-header">
        <Zap size={18} className="why-icon" />
        <span className="why-title">WHY THIS MATTERS IN PRODUCTION</span>
      </div>
      <div className="why-body">
        {children}
      </div>
    </div>
  );
};

// ==========================================
// 3. Key Takeaways Component
// ==========================================
export const KeyTakeaways = ({ items = [], children }) => {
  return (
    <div className="key-takeaways-card">
      <div className="takeaways-header">
        <Award size={18} className="takeaways-icon" />
        <span className="takeaways-title">KEY TAKEAWAYS & CORE CONCEPTS</span>
      </div>
      <div className="takeaways-body">
        {children || (
          <ul className="takeaways-list">
            {items.map((item, i) => (
              <li key={i}>
                <CheckCircle2 size={15} className="text-emerald-500 flex-shrink-0" />
                <span>{item}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

// ==========================================
// 4. Best Practices Component
// ==========================================
export const BestPractices = ({ children }) => {
  return (
    <div className="best-practices-card">
      <div className="bp-header">
        <ShieldCheck size={18} className="bp-icon" />
        <span className="bp-title">ENGINEERING BEST PRACTICES</span>
      </div>
      <div className="bp-body">
        {children}
      </div>
    </div>
  );
};

// ==========================================
// 5. Common Mistakes Component
// ==========================================
export const CommonMistakes = ({ children }) => {
  return (
    <div className="common-mistakes-card">
      <div className="cm-header">
        <AlertTriangle size={18} className="cm-icon" />
        <span className="cm-title">COMMON MISTAKES & PITFALLS</span>
      </div>
      <div className="cm-body">
        {children}
      </div>
    </div>
  );
};

// ==========================================
// 6. Info, Warning, Tip, Interview Callout Cards
// ==========================================
export const InfoCard = ({ title = "IMPORTANT NOTE", children }) => (
  <div className="callout-card callout-info">
    <div className="callout-header">
      <Info size={16} />
      <span>{title}</span>
    </div>
    <div className="callout-body">{children}</div>
  </div>
);

export const WarningCard = ({ title = "WARNING", children }) => (
  <div className="callout-card callout-warning">
    <div className="callout-header">
      <AlertTriangle size={16} />
      <span>{title}</span>
    </div>
    <div className="callout-body">{children}</div>
  </div>
);

export const TipCard = ({ title = "PRO TIP", children }) => (
  <div className="callout-card callout-tip">
    <div className="callout-header">
      <Sparkles size={16} />
      <span>{title}</span>
    </div>
    <div className="callout-body">{children}</div>
  </div>
);

export const InterviewTip = ({ title = "INTERVIEW INSIGHT", children }) => (
  <div className="callout-card callout-interview">
    <div className="callout-header">
      <HelpCircle size={16} />
      <span>{title}</span>
    </div>
    <div className="callout-body">{children}</div>
  </div>
);

// ==========================================
// 7. Accordion / Expandable Section Component
// ==========================================
export const Accordion = ({ title, children, defaultOpen = false }) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="accordion-card">
      <button 
        onClick={() => setIsOpen(!isOpen)} 
        className={`accordion-trigger ${isOpen ? 'open' : ''}`}
      >
        <span className="accordion-title">{title}</span>
        {isOpen ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
      </button>
      {isOpen && (
        <div className="accordion-content">
          {children}
        </div>
      )}
    </div>
  );
};
