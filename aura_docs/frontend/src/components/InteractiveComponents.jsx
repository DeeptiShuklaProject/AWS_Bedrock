import React, { useState, useEffect } from 'react';
import { 
  CheckCircle, AlertCircle, HelpCircle, Info, Lightbulb, 
  AlertTriangle, ChevronDown, ChevronUp, Copy, Check, 
  Play, ArrowRight, Clock, Settings, Cpu, Layers, 
  List, Terminal, Lock, Unlock, BookOpen, Award, Zap, RefreshCw
} from 'lucide-react';

// ==========================================
// 1. Badge Component
// ==========================================
export const Badge = ({ text, type = 'default' }) => {
  const styles = {
    default: { background: 'var(--hover-bg)', color: 'var(--text-primary)', border: '1px solid var(--border-color)' },
    success: { background: 'rgba(16, 185, 129, 0.1)', color: '#10b981', border: '1px solid rgba(16, 185, 129, 0.2)' },
    warning: { background: 'rgba(245, 158, 11, 0.1)', color: '#f59e0b', border: '1px solid rgba(245, 158, 11, 0.2)' },
    danger: { background: 'rgba(239, 68, 68, 0.1)', color: '#ef4444', border: '1px solid rgba(239, 68, 68, 0.2)' },
    info: { background: 'rgba(59, 130, 246, 0.1)', color: '#3b82f6', border: '1px solid rgba(59, 130, 246, 0.2)' },
    accent: { background: 'rgba(139, 92, 246, 0.15)', color: '#a78bfa', border: '1px solid rgba(139, 92, 246, 0.3)' }
  };
  return (
    <span style={{
      display: 'inline-flex',
      alignItems: 'center',
      padding: '2px 8px',
      borderRadius: '12px',
      fontSize: '0.75rem',
      fontWeight: '600',
      lineHeight: '1',
      verticalAlign: 'middle',
      margin: '0 4px',
      ...styles[type]
    }}>
      {text}
    </span>
  );
};

// ==========================================
// 2. LearningObjectives Component
// ==========================================
export const LearningObjectives = ({ children }) => {
  const items = React.Children.toArray(children).map(child => {
    if (typeof child === 'string') {
      return child.split('\n').map(c => c.replace(/^-\s*/, '').trim()).filter(Boolean);
    }
    return child;
  }).flat();

  return (
    <div style={{
      background: 'rgba(139, 92, 246, 0.05)',
      borderLeft: '4px solid var(--accent-color)',
      borderRadius: '8px',
      padding: '20px',
      margin: '24px 0',
      boxShadow: 'var(--shadow-sm)'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
        <BookOpen size={18} style={{ color: 'var(--accent-color)' }} />
        <h4 style={{ margin: '0', fontSize: '1rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          Learning Objectives
        </h4>
      </div>
      <ul style={{ listStyle: 'none', padding: '0', margin: '0', display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {items.map((item, idx) => (
          <li key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '10px', fontSize: '0.9rem' }}>
            <CheckCircle size={16} style={{ color: 'var(--accent-color)', marginTop: '2px', flexShrink: '0' }} />
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

// ==========================================
// 3. InfoCard, Tip, Warning, Callout
// ==========================================
export const InfoCard = ({ title, children }) => (
  <div style={{
    background: 'var(--hover-bg)',
    border: '1px solid var(--border-color)',
    borderRadius: '10px',
    padding: '18px 22px',
    margin: '20px 0',
    boxShadow: 'var(--shadow-sm)'
  }}>
    {title && <h5 style={{ margin: '0 0 10px 0', fontSize: '0.95rem', fontWeight: '700', color: 'var(--text-primary)' }}>{title}</h5>}
    <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: '1.6' }}>{children}</div>
  </div>
);

export const Tip = ({ children }) => (
  <div style={{
    background: 'rgba(16, 185, 129, 0.05)',
    borderLeft: '4px solid #10b981',
    borderRadius: '0 8px 8px 0',
    padding: '16px 20px',
    margin: '20px 0',
    display: 'flex',
    gap: '12px'
  }}>
    <Lightbulb size={20} style={{ color: '#10b981', flexShrink: '0', marginTop: '2px' }} />
    <div>
      <div style={{ fontWeight: '700', fontSize: '0.8rem', color: '#10b981', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '4px' }}>Pro Tip</div>
      <div style={{ fontSize: '0.9rem', lineHeight: '1.6' }}>{children}</div>
    </div>
  </div>
);

export const Warning = ({ children }) => (
  <div style={{
    background: 'rgba(245, 158, 11, 0.05)',
    borderLeft: '4px solid #f59e0b',
    borderRadius: '0 8px 8px 0',
    padding: '16px 20px',
    margin: '20px 0',
    display: 'flex',
    gap: '12px'
  }}>
    <AlertTriangle size={20} style={{ color: '#f59e0b', flexShrink: '0', marginTop: '2px' }} />
    <div>
      <div style={{ fontWeight: '700', fontSize: '0.8rem', color: '#f59e0b', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '4px' }}>Warning</div>
      <div style={{ fontSize: '0.9rem', lineHeight: '1.6' }}>{children}</div>
    </div>
  </div>
);

export const Callout = ({ title, type = 'info', children }) => {
  const configs = {
    info: { border: '#3b82f6', bg: 'rgba(59, 130, 246, 0.05)', icon: <Info size={18} style={{ color: '#3b82f6' }} /> },
    success: { border: '#10b981', bg: 'rgba(16, 185, 129, 0.05)', icon: <CheckCircle size={18} style={{ color: '#10b981' }} /> },
    warning: { border: '#f59e0b', bg: 'rgba(245, 158, 11, 0.05)', icon: <AlertTriangle size={18} style={{ color: '#f59e0b' }} /> },
    danger: { border: '#ef4444', bg: 'rgba(239, 68, 68, 0.05)', icon: <AlertCircle size={18} style={{ color: '#ef4444' }} /> }
  };
  const config = configs[type] || configs.info;
  return (
    <div style={{
      background: config.bg,
      borderLeft: `4px solid ${config.border}`,
      borderRadius: '0 8px 8px 0',
      padding: '16px 20px',
      margin: '20px 0',
      display: 'flex',
      gap: '12px'
    }}>
      <div style={{ flexShrink: '0', marginTop: '2px' }}>{config.icon}</div>
      <div>
        {title && <div style={{ fontWeight: '700', fontSize: '0.85rem', color: config.border, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '4px' }}>{title}</div>}
        <div style={{ fontSize: '0.9rem', lineHeight: '1.6' }}>{children}</div>
      </div>
    </div>
  );
};

// ==========================================
// 4. ExpandableSection Component
// ==========================================
export const ExpandableSection = ({ title, children }) => {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <div style={{
      border: '1px solid var(--border-color)',
      borderRadius: '8px',
      margin: '16px 0',
      overflow: 'hidden',
      background: 'var(--hover-bg)'
    }}>
      <button 
        onClick={() => setIsOpen(!isOpen)}
        style={{
          width: '100%',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          padding: '14px 18px',
          background: 'none',
          border: 'none',
          color: 'var(--text-primary)',
          fontSize: '0.9rem',
          fontWeight: '600',
          cursor: 'pointer',
          outline: 'none'
        }}
      >
        <span>{title}</span>
        {isOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
      </button>
      {isOpen && (
        <div style={{
          padding: '18px',
          background: 'var(--bg-panel)',
          borderTop: '1px solid var(--border-color)',
          fontSize: '0.9rem',
          lineHeight: '1.6'
        }}>
          {children}
        </div>
      )}
    </div>
  );
};

// ==========================================
// 5. Accordion & AccordionItem
// ==========================================
export const Accordion = ({ children }) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', margin: '20px 0' }}>
    {children}
  </div>
);

export const AccordionItem = ({ title, children }) => (
  <ExpandableSection title={title}>{children}</ExpandableSection>
);

// ==========================================
// 6. Tabs & Tab
// ==========================================
export const Tabs = ({ children }) => {
  const tabElements = React.Children.toArray(children);
  const [activeIdx, setActiveIdx] = useState(0);

  if (tabElements.length === 0) return null;

  return (
    <div style={{
      border: '1px solid var(--border-color)',
      borderRadius: '10px',
      margin: '24px 0',
      overflow: 'hidden',
      background: 'var(--bg-panel)'
    }}>
      <div style={{
        display: 'flex',
        background: 'var(--hover-bg)',
        borderBottom: '1px solid var(--border-color)',
        overflowX: 'auto'
      }}>
        {tabElements.map((tab, idx) => (
          <button
            key={idx}
            onClick={() => setActiveIdx(idx)}
            style={{
              padding: '12px 20px',
              border: 'none',
              background: activeIdx === idx ? 'var(--bg-panel)' : 'transparent',
              color: activeIdx === idx ? 'var(--text-primary)' : 'var(--text-secondary)',
              fontWeight: '600',
              fontSize: '0.85rem',
              cursor: 'pointer',
              outline: 'none',
              borderBottom: activeIdx === idx ? '2px solid var(--accent-color)' : '2px solid transparent',
              transition: 'all 0.2s'
            }}
          >
            {tab.props.label}
          </button>
        ))}
      </div>
      <div style={{ padding: '20px', fontSize: '0.9rem', lineHeight: '1.6' }}>
        {tabElements[activeIdx]}
      </div>
    </div>
  );
};

export const Tab = ({ children }) => <div>{children}</div>;

// ==========================================
// 7. CodeBlock Component (Enhanced syntax block)
// ==========================================
export const CodeBlock = ({ code, language = 'python', filename }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div style={{
      position: 'relative',
      background: 'var(--code-bg)',
      border: '1px solid var(--border-color)',
      borderRadius: '8px',
      margin: '20px 0',
      overflow: 'hidden',
      boxShadow: 'var(--shadow-md)'
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '6px 14px',
        background: 'rgba(0, 0, 0, 0.2)',
        borderBottom: '1px solid rgba(255, 255, 255, 0.05)',
        fontSize: '0.75rem',
        color: 'var(--text-secondary)',
        fontFamily: 'var(--font-code)'
      }}>
        <span>{filename || language.toUpperCase()}</span>
        <button
          onClick={handleCopy}
          style={{
            background: 'none',
            border: 'none',
            color: 'var(--text-secondary)',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '4px',
            outline: 'none'
          }}
        >
          {copied ? <Check size={12} style={{ color: '#10b981' }} /> : <Copy size={12} />}
          <span>{copied ? 'Copied' : 'Copy'}</span>
        </button>
      </div>
      <pre style={{
        margin: '0',
        padding: '16px',
        overflowX: 'auto',
        fontSize: '0.85rem',
        color: 'var(--code-text)',
        fontFamily: 'var(--font-code)',
        lineHeight: '1.5'
      }}>
        <code>{code.trim()}</code>
      </pre>
    </div>
  );
};

// ==========================================
// 8. CodeComparison Component
// ==========================================
export const CodeComparison = ({ before, after, beforeLabel = 'Standard Python', afterLabel = 'Agent Pattern' }) => (
  <div style={{
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
    gap: '16px',
    margin: '24px 0'
  }}>
    <div>
      <div style={{ fontSize: '0.8rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '6px', color: 'var(--text-secondary)' }}>
        {beforeLabel}
      </div>
      <CodeBlock code={before} />
    </div>
    <div>
      <div style={{ fontSize: '0.8rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '6px', color: 'var(--accent-color)' }}>
        {afterLabel}
      </div>
      <CodeBlock code={after} />
    </div>
  </div>
);

// ==========================================
// 9. Timeline & TimelineItem
// ==========================================
export const Timeline = ({ children }) => (
  <div style={{
    position: 'relative',
    margin: '30px 0 30px 20px',
    paddingLeft: '24px',
    borderLeft: '2px solid var(--border-color)',
    display: 'flex',
    flexDirection: 'column',
    gap: '24px'
  }}>
    {children}
  </div>
);

export const TimelineItem = ({ title, time, children }) => (
  <div style={{ position: 'relative' }}>
    <div style={{
      position: 'absolute',
      left: '-33px',
      top: '4px',
      width: '16px',
      height: '16px',
      borderRadius: '50%',
      background: 'var(--accent-color)',
      border: '4px solid var(--bg-panel)',
      boxShadow: '0 0 0 2px var(--border-color)'
    }} />
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
      <h5 style={{ margin: '0', fontSize: '0.95rem', fontWeight: '700', color: 'var(--text-primary)' }}>{title}</h5>
      {time && <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', background: 'var(--hover-bg)', padding: '2px 8px', borderRadius: '10px' }}>{time}</span>}
    </div>
    <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: '1.5' }}>{children}</div>
  </div>
);

// ==========================================
// 10. StepByStep & Step
// ==========================================
export const StepByStep = ({ children }) => {
  const steps = React.Children.toArray(children);
  const [activeStep, setActiveStep] = useState(0);

  return (
    <div style={{
      border: '1px solid var(--border-color)',
      borderRadius: '10px',
      margin: '24px 0',
      background: 'var(--bg-panel)',
      boxShadow: 'var(--shadow-sm)'
    }}>
      {/* Steps Headers Progress */}
      <div style={{
        display: 'flex',
        borderBottom: '1px solid var(--border-color)',
        background: 'var(--hover-bg)',
        padding: '10px 16px',
        alignItems: 'center',
        gap: '12px',
        overflowX: 'auto'
      }}>
        {steps.map((_, idx) => (
          <button
            key={idx}
            onClick={() => setActiveStep(idx)}
            style={{
              padding: '6px 12px',
              border: 'none',
              borderRadius: '20px',
              background: activeStep === idx ? 'var(--accent-color)' : 'rgba(0,0,0,0.05)',
              color: activeStep === idx ? 'var(--accent-text)' : 'var(--text-secondary)',
              fontWeight: '700',
              fontSize: '0.75rem',
              cursor: 'pointer',
              transition: 'all 0.2s'
            }}
          >
            Step {idx + 1}
          </button>
        ))}
      </div>
      
      {/* Step Body */}
      <div style={{ padding: '24px' }}>
        <h5 style={{ fontSize: '1.05rem', fontWeight: '700', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{
            display: 'inline-flex',
            width: '24px',
            height: '24px',
            borderRadius: '50%',
            background: 'var(--accent-color)',
            color: 'var(--accent-text)',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '0.8rem',
            fontWeight: '800'
          }}>{activeStep + 1}</span>
          {steps[activeStep].props.title}
        </h5>
        <div style={{ fontSize: '0.9rem', lineHeight: '1.6' }}>
          {steps[activeStep].props.children}
        </div>
        
        {/* Next/Prev buttons */}
        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '20px', borderTop: '1px solid var(--border-color)', paddingTop: '16px' }}>
          <button
            disabled={activeStep === 0}
            onClick={() => setActiveStep(activeStep - 1)}
            style={{
              background: 'none',
              border: '1px solid var(--border-color)',
              color: activeStep === 0 ? 'var(--text-secondary)' : 'var(--text-primary)',
              padding: '6px 14px',
              borderRadius: '6px',
              cursor: activeStep === 0 ? 'not-allowed' : 'pointer',
              fontSize: '0.8rem',
              opacity: activeStep === 0 ? 0.5 : 1
            }}
          >
            Previous Step
          </button>
          <button
            disabled={activeStep === steps.length - 1}
            onClick={() => setActiveStep(activeStep + 1)}
            style={{
              background: 'var(--accent-color)',
              border: 'none',
              color: 'var(--accent-text)',
              padding: '6px 14px',
              borderRadius: '6px',
              cursor: activeStep === steps.length - 1 ? 'not-allowed' : 'pointer',
              fontSize: '0.8rem',
              opacity: activeStep === steps.length - 1 ? 0.5 : 1,
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            Next Step
            <ArrowRight size={12} />
          </button>
        </div>
      </div>
    </div>
  );
};

export const Step = ({ children }) => <div>{children}</div>;

// ==========================================
// 11. Quiz Component
// ==========================================
// (Note: The premium Quiz component is declared as Component #49 to avoid redeclaration issues)

// ==========================================
// 12. FlashCards Component
// ==========================================
// (Note: The premium FlashCards component is declared as Component #35 to avoid redeclaration issues)

// ==========================================
// 13. InteractiveExample Component
// ==========================================
export const InteractiveExample = ({ initialCode, instruction, language = 'python' }) => {
  const [code, setCode] = useState(initialCode ? initialCode.trim() : '');
  const [output, setOutput] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [success, setSuccess] = useState(null);
  const handleRun = async () => {
    setIsRunning(true);
    setSuccess(null);
    try {
      const response = await fetch('/api/playground/run-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, language })
      });
      const data = await response.json();
      if (data.success) {
        setSuccess(true);
        setOutput(data.stdout || data.stderr ? `${data.stdout}${data.stderr}` : 'Executed successfully (no stdout).');
      } else {
        setSuccess(false);
        setOutput(data.stderr || 'Execution failed.');
      }
    } catch (e) {
      setSuccess(false);
      setOutput(`Error running script: ${e.message}`);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div style={{
      border: '1px solid var(--border-color)',
      borderRadius: '12px',
      margin: '28px 0',
      overflow: 'hidden',
      background: 'var(--bg-panel)',
      boxShadow: 'var(--shadow-md)'
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '10px 18px',
        background: 'var(--hover-bg)',
        borderBottom: '1px solid var(--border-color)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.85rem', fontWeight: '700', color: 'var(--text-primary)' }}>
          <Terminal size={16} />
          <span>Interactive Playground ({language.toUpperCase()})</span>
        </div>
        <button
          onClick={handleRun}
          disabled={isRunning}
          style={{
            background: 'var(--accent-color)',
            color: 'var(--accent-text)',
            border: 'none',
            padding: '5px 12px',
            borderRadius: '4px',
            cursor: isRunning ? 'not-allowed' : 'pointer',
            fontSize: '0.75rem',
            fontWeight: '700',
            display: 'flex',
            alignItems: 'center',
            gap: '4px'
          }}
        >
          {isRunning ? <RefreshCw size={12} className="loader-spinner" /> : <Play size={12} />}
          <span>{isRunning ? 'Running...' : 'Run Code'}</span>
        </button>
      </div>
      {instruction && (
        <div style={{ padding: '10px 18px', background: 'rgba(0,0,0,0.01)', borderBottom: '1px solid var(--border-color)', fontSize: '0.8rem', color: 'var(--text-secondary)', fontStyle: 'italic' }}>
          <strong>Task:</strong> {instruction}
        </div>
      )}
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        rows={6}
        spellCheck="false"
        style={{
          width: '100%',
          background: 'var(--code-bg)',
          color: 'var(--code-text)',
          border: 'none',
          padding: '16px',
          fontFamily: 'var(--font-code)',
          fontSize: '0.85rem',
          outline: 'none',
          resize: 'vertical',
          display: 'block'
        }}
      />
      {output && (
        <div className={`widget-console ${success === false ? 'console-error' : 'console-success'}`} style={{ borderTop: '1px solid var(--border-color)', borderRadius: '0 0 12px 12px' }}>
          <div className="console-header">Output:</div>
          <pre>{output}</pre>
        </div>
      )}
    </div>
  );
};

// ==========================================
// 14. KeyTakeaways Component
// ==========================================
// (Note: The premium KeyTakeaways component is declared as Component #37 to avoid redeclaration issues)

// ==========================================
// 15. InterviewQuestions & InterviewQuestion
// ==========================================
// (Note: The premium InterviewQuestions and InterviewQuestion components are declared as Components #50 and #51 to avoid redeclaration issues)

// ==========================================
// 16. PracticeProblem & Exercise
// ==========================================
// (Note: The premium PracticeProblem component is declared as Component #36 to avoid redeclaration issues)

export const Exercise = ({ title, instructions, initialCode, language = 'python' }) => (
  <div style={{
    border: '2px solid var(--border-color)',
    borderRadius: '12px',
    margin: '28px 0',
    padding: '20px',
    background: 'rgba(0, 0, 0, 0.01)'
  }}>
    <h5 style={{ margin: '0 0 10px 0', fontSize: '1rem', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '8px' }}>
      <Zap size={18} style={{ color: '#f59e0b' }} />
      <span>Coding Challenge: {title}</span>
    </h5>
    <div style={{ fontSize: '0.9rem', lineHeight: '1.5', marginBottom: '16px', color: 'var(--text-secondary)' }}>
      {instructions}
    </div>
    <InteractiveExample initialCode={initialCode} language={language} />
  </div>
);

// ==========================================
// 17. Checklist Component
// ==========================================
export const Checklist = ({ items }) => {
  const [checkedItems, setCheckedItems] = useState({});

  const toggle = (idx) => {
    setCheckedItems(prev => ({
      ...prev,
      [idx]: !prev[idx]
    }));
  };

  const listItems = Array.isArray(items) ? items : (typeof items === 'string' ? items.split('\n').map(i => i.replace(/^\s*-\s*/, '').trim()).filter(Boolean) : []);

  return (
    <div style={{
      border: '1px solid var(--border-color)',
      borderRadius: '8px',
      padding: '16px 20px',
      margin: '20px 0',
      background: 'var(--hover-bg)'
    }}>
      <h6 style={{ margin: '0 0 12px 0', fontSize: '0.85rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Task Checklist</h6>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {listItems.map((item, idx) => (
          <div
            key={idx}
            onClick={() => toggle(idx)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              cursor: 'pointer',
              fontSize: '0.875rem',
              color: checkedItems[idx] ? 'var(--text-secondary)' : 'var(--text-primary)',
              textDecoration: checkedItems[idx] ? 'line-through' : 'none'
            }}
          >
            <input
              type="checkbox"
              checked={!!checkedItems[idx]}
              onChange={() => {}}
              style={{
                width: '16px',
                height: '16px',
                accentColor: 'var(--accent-color)',
                cursor: 'pointer'
              }}
            />
            <span>{item}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

// ==========================================
// 18. CopyCommand Component
// ==========================================
export const CopyCommand = ({ command }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(command);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      background: 'var(--code-bg)',
      borderRadius: '6px',
      padding: '8px 12px',
      margin: '12px 0',
      border: '1px solid var(--border-color)',
      justifyContent: 'space-between'
    }}>
      <code style={{ fontSize: '0.8rem', color: 'var(--code-text)', fontFamily: 'var(--font-code)' }}>{command}</code>
      <button
        onClick={handleCopy}
        style={{
          background: 'none',
          border: 'none',
          color: 'var(--text-secondary)',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          outline: 'none'
        }}
      >
        {copied ? <Check size={14} style={{ color: '#10b981' }} /> : <Copy size={14} />}
      </button>
    </div>
  );
};

// ==========================================
// 19. NextTopic Component
// ==========================================
// (Note: The premium NextTopic banner component is declared as Component #38 to avoid redeclaration issues)

// ==========================================
// 20. DecoratorVisualizer Component
// ==========================================
// (Note: The premium DecoratorVisualizer component is declared as Component #43 to avoid redeclaration issues)

// ==========================================
// 21. AgentArchitectureDiagram Component
// ==========================================
export const AgentArchitectureDiagram = () => (
  <div style={{
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '12px',
    margin: '30px 0',
    padding: '24px',
    background: 'var(--hover-bg)',
    borderRadius: '12px',
    border: '1px solid var(--border-color)'
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
      <Layers size={18} style={{ color: 'var(--accent-color)' }} />
      <span style={{ fontSize: '0.9rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Agent Runtime Block Architecture</span>
    </div>
    
    <div style={{
      display: 'flex',
      flexWrap: 'wrap',
      justifyContent: 'center',
      alignItems: 'center',
      gap: '12px',
      width: '100%',
      maxWidth: '640px'
    }}>
      <div style={{ width: '120px', padding: '12px', background: 'var(--bg-panel)', border: '2px solid var(--accent-color)', borderRadius: '8px', textAlign: 'center', fontWeight: '700', fontSize: '0.8rem', boxShadow: 'var(--shadow-sm)' }}>
        USER INPUT
      </div>
      <ArrowRight size={16} style={{ color: 'var(--text-secondary)' }} />
      <div style={{ width: '120px', padding: '12px', background: 'rgba(139, 92, 246, 0.1)', border: '2px dashed var(--accent-color)', borderRadius: '8px', textAlign: 'center', fontWeight: '700', fontSize: '0.8rem', color: 'var(--text-primary)' }}>
        AGENT INTERFACE
      </div>
      <ArrowRight size={16} style={{ color: 'var(--text-secondary)' }} />
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        <div style={{ width: '140px', padding: '10px', background: 'rgba(59, 130, 246, 0.1)', border: '1px solid #3b82f6', borderRadius: '8px', textAlign: 'center', fontWeight: '600', fontSize: '0.75rem' }}>
          🧠 Planner (Execution Engine)
        </div>
        <div style={{ width: '140px', padding: '10px', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid #10b981', borderRadius: '8px', textAlign: 'center', fontWeight: '600', fontSize: '0.75rem' }}>
          💾 Memory (DynamoDB/RAM)
        </div>
        <div style={{ width: '140px', padding: '10px', background: 'rgba(245, 158, 11, 0.1)', border: '1px solid #f59e0b', borderRadius: '8px', textAlign: 'center', fontWeight: '600', fontSize: '0.75rem' }}>
          🛠️ Tools / Integrations
        </div>
      </div>
      <ArrowRight size={16} style={{ color: 'var(--text-secondary)' }} />
      <div style={{ width: '120px', padding: '12px', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid #ef4444', borderRadius: '8px', textAlign: 'center', fontWeight: '700', fontSize: '0.8rem' }}>
        LLM INFERENCE
      </div>
    </div>
  </div>
);

// ==========================================
// 22. WorkflowVisualizer Component
// ==========================================
export const WorkflowVisualizer = ({ title = 'Multi-Agent Supervisor Flow', steps }) => {
  const stepItems = Array.isArray(steps) ? steps : (typeof steps === 'string' ? steps.split('\n').map(s => s.replace(/^\s*-\s*/, '').trim()).filter(Boolean) : []);
  return (
    <div style={{
      border: '1px solid var(--border-color)',
      borderRadius: '12px',
      margin: '24px 0',
      padding: '20px',
      background: 'var(--bg-panel)',
      boxShadow: 'var(--shadow-sm)'
    }}>
      <h6 style={{ margin: '0 0 16px 0', fontSize: '0.9rem', fontWeight: '700', color: 'var(--text-primary)' }}>{title}</h6>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        {stepItems.map((step, idx) => (
          <div key={idx} style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <span style={{
              display: 'flex',
              width: '24px',
              height: '24px',
              borderRadius: '50%',
              background: 'var(--accent-color)',
              color: 'var(--accent-text)',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '0.75rem',
              fontWeight: '800'
            }}>{idx + 1}</span>
            <div style={{
              flexGrow: '1',
              padding: '10px 14px',
              background: 'var(--hover-bg)',
              border: '1px solid var(--border-color)',
              borderRadius: '6px',
              fontSize: '0.85rem'
            }}>
              {step}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// ==========================================
// 23. ExecutionTimeline Component
// ==========================================
export const ExecutionTimeline = ({ tasks }) => {
  const taskItems = Array.isArray(tasks) ? tasks : [];
  return (
    <div style={{
      border: '1px solid var(--border-color)',
      borderRadius: '12px',
      margin: '24px 0',
      padding: '20px',
      background: 'var(--bg-panel)'
    }}>
      <h6 style={{ margin: '0 0 16px 0', fontSize: '0.85rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Execution Timeline Visualizer</h6>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {taskItems.map((task, idx) => (
          <div key={idx} style={{ display: 'grid', gridTemplateColumns: '120px 1fr', gap: '12px', alignItems: 'center' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: '600', color: 'var(--text-primary)', wordBreak: 'break-all' }}>{task.name}</span>
            <div style={{ height: '24px', background: 'var(--hover-bg)', borderRadius: '4px', position: 'relative', overflow: 'hidden', border: '1px solid var(--border-color)' }}>
              <div style={{
                position: 'absolute',
                left: `${task.start || 0}%`,
                width: `${task.duration || 100}%`,
                height: '100%',
                background: task.color || 'var(--accent-color)',
                borderRadius: '4px',
                display: 'flex',
                alignItems: 'center',
                paddingLeft: '8px',
                fontSize: '0.75rem',
                color: '#fff',
                fontWeight: '700'
              }}>
                {task.duration}% time
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// ==========================================
// 24. ComparisonTable Component
// ==========================================
export const ComparisonTable = ({ headers, rows }) => {
  const headList = Array.isArray(headers) ? headers : [];
  const rowList = Array.isArray(rows) ? rows : [];
  return (
    <div style={{ overflowX: 'auto', margin: '24px 0', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem', background: 'var(--bg-panel)' }}>
        <thead>
          <tr style={{ background: 'var(--hover-bg)', borderBottom: '1px solid var(--border-color)' }}>
            {headList.map((h, idx) => (
              <th key={idx} style={{ padding: '10px 14px', fontWeight: '700', textAlign: 'left', borderRight: '1px solid var(--border-color)' }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rowList.map((row, rIdx) => (
            <tr key={rIdx} style={{ borderBottom: rIdx === rowList.length - 1 ? 'none' : '1px solid var(--border-color)' }}>
              {row.map((cell, cIdx) => (
                <td key={cIdx} style={{ padding: '10px 14px', borderRight: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

// ==========================================
// 25. ProgressTracker Component
// ==========================================
export const ProgressTracker = ({ currentSection, totalSections }) => {
  const percent = Math.min(100, Math.max(0, Math.round((currentSection / totalSections) * 100)));
  return (
    <div style={{
      position: 'sticky',
      top: '0',
      zIndex: '10',
      background: 'var(--bg-panel)',
      borderBottom: '1px solid var(--border-color)',
      padding: '10px 24px',
      margin: '-40px -48px 24px -48px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      backdropFilter: 'blur(var(--glass-blur))'
    }}>
      <span style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--text-secondary)' }}>
        Course Progress: {percent}% Completed
      </span>
    </div>
  );
};

// ==========================================
// 26. WhyItMatters Component
// ==========================================
export const WhyItMatters = ({ children }) => (
  <div className="why-it-matters-card">
    <div className="card-header">
      <Zap size={18} className="icon-gold" />
      <span>Why It Matters</span>
    </div>
    <div className="card-content">{children}</div>
  </div>
);

// ==========================================
// 27. ConceptCard Component
// ==========================================
export const ConceptCard = ({ title, children }) => (
  <div className="concept-overview-card">
    <div className="card-title">{title}</div>
    <div className="card-content">{children}</div>
  </div>
);

// ==========================================
// 28. RealWorldExample Component
// ==========================================
export const RealWorldExample = ({ title, children }) => (
  <div className="real-world-example-card">
    <div className="card-header">
      <Cpu size={18} className="icon-purple" />
      <span>Real-World Scenario: {title}</span>
    </div>
    <div className="card-content">{children}</div>
  </div>
);

// ==========================================
// 29. InteractiveDiagram Component
// ==========================================
export const InteractiveDiagram = ({ title, children }) => (
  <div className="interactive-diagram-card">
    <div className="diagram-header">{title}</div>
    <div className="diagram-body">{children}</div>
  </div>
);

// ==========================================
// 30. SyntaxTabs Component
// ==========================================
export const SyntaxTabs = ({ tabs, children }) => {
  const [activeTab, setActiveTab] = useState(0);
  const tabList = Array.isArray(tabs) ? tabs : [];
  return (
    <div className="syntax-tabs-container">
      <div className="tabs-header">
        {tabList.map((tab, idx) => (
          <button
            key={idx}
            className={`tab-btn ${activeTab === idx ? 'active' : ''}`}
            onClick={() => setActiveTab(idx)}
          >
            {tab}
          </button>
        ))}
      </div>
      <div className="tab-content">
        {React.Children.toArray(children)[activeTab]}
      </div>
    </div>
  );
};

// ==========================================
// 31. CodeExplanation Component
// ==========================================
export const CodeExplanation = ({ children }) => (
  <div className="code-explanation-box">
    <div className="explanation-title">Code Breakdown</div>
    <div className="explanation-content">{children}</div>
  </div>
);

// ==========================================
// 32. ExecutionVisualizer Component
// ==========================================
export const ExecutionVisualizer = ({ title, steps }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const stepItems = Array.isArray(steps) ? steps : [];
  return (
    <div className="execution-visualizer-card">
      <div className="card-header">
        <Terminal size={16} />
        <span>Execution Visualizer: {title}</span>
      </div>
      {stepItems.length > 0 && (
        <div className="visualizer-body">
          <div className="step-display">
            Step {currentStep + 1} of {stepItems.length}: {stepItems[currentStep].label}
          </div>
          <div className="console-display">
            <pre>{stepItems[currentStep].output}</pre>
          </div>
          <div className="nav-buttons">
            <button onClick={() => setCurrentStep(Math.max(0, currentStep - 1))} disabled={currentStep === 0}>Prev</button>
            <button onClick={() => setCurrentStep(Math.min(stepItems.length - 1, currentStep + 1))} disabled={currentStep === stepItems.length - 1}>Next</button>
          </div>
        </div>
      )}
    </div>
  );
};

// ==========================================
// 33. BestPractices Component
// ==========================================
export const BestPractices = ({ children }) => {
  const items = React.Children.toArray(children).map(child => {
    if (typeof child === 'string') {
      return child.split('\n').map(c => c.replace(/^-\s*/, '').trim()).filter(Boolean);
    }
    return child;
  }).flat();
  return (
    <div className="best-practices-card">
      <div className="card-header">
        <CheckCircle size={18} className="icon-green" />
        <span>Best Practices</span>
      </div>
      <ul>
        {items.map((item, idx) => (
          <li key={idx}>✓ {item}</li>
        ))}
      </ul>
    </div>
  );
};

// ==========================================
// 34. CommonMistakes Component
// ==========================================
export const CommonMistakes = ({ children }) => {
  const items = React.Children.toArray(children).map(child => {
    if (typeof child === 'string') {
      return child.split('\n').map(c => c.replace(/^-\s*/, '').trim()).filter(Boolean);
    }
    return child;
  }).flat();
  return (
    <div className="common-mistakes-card">
      <div className="card-header">
        <AlertTriangle size={18} className="icon-orange" />
        <span>Common Mistakes & Gotchas</span>
      </div>
      <ul>
        {items.map((item, idx) => (
          <li key={idx}>✗ {item}</li>
        ))}
      </ul>
    </div>
  );
};

// ==========================================
// 35. FlashCards Component
// ==========================================
export const FlashCards = ({ cards }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const cardList = Array.isArray(cards) ? cards : [];

  if (cardList.length === 0) return null;

  return (
    <div className="flashcards-widget">
      <div className="flashcards-header">
        <span>Active Recall Flashcards</span>
        <span>{currentIndex + 1} / {cardList.length}</span>
      </div>
      <div 
        className={`flashcard-container ${isFlipped ? 'flipped' : ''}`}
        onClick={() => setIsFlipped(!isFlipped)}
      >
        <div className="card-inner">
          <div className="card-front">
            <div className="card-side-label">Question</div>
            <div className="card-text">{cardList[currentIndex].question}</div>
            <div className="click-hint">Click to reveal answer</div>
          </div>
          <div className="card-back">
            <div className="card-side-label">Answer</div>
            <div className="card-text">{cardList[currentIndex].answer}</div>
            <div className="click-hint">Click to show question</div>
          </div>
        </div>
      </div>
      <div className="flashcard-nav">
        <button 
          onClick={() => { setIsFlipped(false); setCurrentIndex(Math.max(0, currentIndex - 1)); }}
          disabled={currentIndex === 0}
        >
          Previous
        </button>
        <button 
          onClick={() => { setIsFlipped(false); setCurrentIndex(Math.min(cardList.length - 1, currentIndex + 1)); }}
          disabled={currentIndex === cardList.length - 1}
        >
          Next
        </button>
      </div>
    </div>
  );
};

// ==========================================
// 36. PracticeProblem Component
// ==========================================
export const PracticeProblem = ({ title, description, hint, solution }) => {
  const [showHint, setShowHint] = useState(false);
  const [showSolution, setShowSolution] = useState(false);
  return (
    <div className="practice-problem-card">
      <div className="card-header">
        <Lightbulb size={18} className="icon-purple" />
        <span>Practice Exercise: {title}</span>
      </div>
      <div className="card-body">
        <p className="problem-description">{description}</p>
        <div className="action-buttons">
          {hint && <button onClick={() => setShowHint(!showHint)} className="btn-secondary">{showHint ? "Hide Hint" : "Show Hint"}</button>}
          <button onClick={() => setShowSolution(!showSolution)} className="btn-primary">{showSolution ? "Hide Solution" : "Reveal Solution"}</button>
        </div>
        {showHint && hint && (
          <div className="hint-box">
            <strong>Hint:</strong> {hint}
          </div>
        )}
        {showSolution && (
          <div className="solution-box">
            <strong>Model Solution:</strong>
            <pre className="solution-code"><code>{solution}</code></pre>
          </div>
        )}
      </div>
    </div>
  );
};

// ==========================================
// 37. KeyTakeaways Component
// ==========================================
export const KeyTakeaways = ({ children }) => {
  const items = React.Children.toArray(children).map(child => {
    if (typeof child === 'string') {
      return child.split('\n').map(c => c.replace(/^-\s*/, '').trim()).filter(Boolean);
    }
    return child;
  }).flat();
  return (
    <div className="key-takeaways-card">
      <div className="card-header">
        <Award size={18} className="icon-green" />
        <span>Key Takeaways</span>
      </div>
      <ul>
        {items.map((item, idx) => (
          <li key={idx}>{item}</li>
        ))}
      </ul>
    </div>
  );
};

// ==========================================
// 38. NextTopic Component
// ==========================================
export const NextTopic = ({ title, href }) => (
  <div className="next-topic-banner">
    <div className="banner-left">
      <span className="banner-subtitle">UP NEXT</span>
      <span className="banner-title">{title}</span>
    </div>
    <a href={href} className="doc-link banner-btn">
      <span>Continue</span>
      <ArrowRight size={14} />
    </a>
  </div>
);

// ==========================================
// 39. MemoryVisualizer Component
// ==========================================
export const MemoryVisualizer = () => {
  const [step, setStep] = useState(0);
  const steps = [
    {
      code: "x = [1, 2]",
      explanation: "A list object [1, 2] is created in heap memory at address 0x7f03. The variable 'x' is bound in the stack scope, pointing to this heap address. The list object has a reference count of 1.",
      stack: [{ name: 'x', address: '0x7f03' }],
      heap: [{ address: '0x7f03', value: '[1, 2]', refCount: 1 }]
    },
    {
      code: "y = x",
      explanation: "Variable 'y' is bound in the stack. Rather than copying the list, 'y' points to the SAME memory address 0x7f03. The list reference count increments to 2. Both variables now refer to the same list.",
      stack: [{ name: 'x', address: '0x7f03' }, { name: 'y', address: '0x7f03' }],
      heap: [{ address: '0x7f03', value: '[1, 2]', refCount: 2 }]
    },
    {
      code: "x.append(3)",
      explanation: "The list object at address 0x7f03 is mutated in-place to [1, 2, 3]. Because both 'x' and 'y' reference this same address, print(y) will reflect this change. No new references are created.",
      stack: [{ name: 'x', address: '0x7f03' }, { name: 'y', address: '0x7f03' }],
      heap: [{ address: '0x7f03', value: '[1, 2, 3]', refCount: 2 }]
    },
    {
      code: "x = None",
      explanation: "Variable 'x' is rebound to None. The reference counter of list 0x7f03 decreases to 1. The list remains in memory because 'y' still references it. If y is also unbound, the ref count hits 0 and GC reclaims the memory.",
      stack: [{ name: 'x', address: 'None' }, { name: 'y', address: '0x7f03' }],
      heap: [{ address: '0x7f03', value: '[1, 2, 3]', refCount: 1 }]
    }
  ];

  const current = steps[step];

  return (
    <div className="memory-visualizer-card widget-card">
      <div className="widget-header">
        <div className="widget-title">
          <Cpu size={16} />
          <span>Interactive Memory Visualizer</span>
        </div>
      </div>
      <div className="visualizer-container">
        <div className="code-display">
          {steps.map((s, idx) => (
            <div key={idx} className={`code-line ${step === idx ? 'active' : ''}`}>
              <span>{s.code}</span>
            </div>
          ))}
        </div>
        <div className="visual-memory-grid">
          <div className="memory-box stack-box">
            <div className="box-title">Stack (Variables)</div>
            <div className="box-content">
              {current.stack.map((item, idx) => (
                <div key={idx} className="stack-var">
                  <span className="var-name">{item.name}</span>
                  <span className="var-arrow">➔</span>
                  <span className="var-address">{item.address}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="memory-box heap-box">
            <div className="box-title">Heap (Objects)</div>
            <div className="box-content">
              {current.heap.map((item, idx) => (
                <div key={idx} className="heap-obj">
                  <div className="obj-addr">{item.address}</div>
                  <div className="obj-val">{item.value}</div>
                  <div className="obj-ref">Ref count: {item.refCount}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
        <div className="explanation-panel">
          <p>{current.explanation}</p>
        </div>
        <div className="visualizer-controls">
          <button onClick={() => setStep(Math.max(0, step - 1))} disabled={step === 0}>Previous Step</button>
          <button onClick={() => setStep(Math.min(steps.length - 1, step + 1))} disabled={step === steps.length - 1}>Next Step</button>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 40. FunctionExecutionVisualizer Component
// ==========================================
export const FunctionExecutionVisualizer = () => {
  const [step, setStep] = useState(0);
  const steps = [
    {
      title: "Initial Call",
      explanation: "The user triggers factorial(3). Python allocates a new stack frame for factorial(n=3) and initiates computation.",
      frames: [{ name: "factorial(n=3)", status: "Executing" }]
    },
    {
      title: "First Recursion Frame",
      explanation: "factorial(3) calls factorial(2). A second frame factorial(n=2) is pushed onto the stack, pausing the execution of the first frame.",
      frames: [{ name: "factorial(n=2)", status: "Executing" }, { name: "factorial(n=3)", status: "Paused" }]
    },
    {
      title: "Base Case Reached",
      explanation: "factorial(2) calls factorial(1). Frame factorial(n=1) is pushed. Since n <= 1, it immediately hits the base case and returns 1.",
      frames: [{ name: "factorial(n=1)", status: "Returning: 1" }, { name: "factorial(n=2)", status: "Paused" }, { name: "factorial(n=3)", status: "Paused" }]
    },
    {
      title: "Popping Base Frame",
      explanation: "factorial(1) returns 1 and its frame is popped. factorial(2) resumes, multiplying 2 * (factorial(1) return value) = 2.",
      frames: [{ name: "factorial(n=2)", status: "Returning: 2" }, { name: "factorial(n=3)", status: "Paused" }]
    },
    {
      title: "Final Return",
      explanation: "factorial(2) returns 2 and is popped. factorial(3) resumes, calculating 3 * 2 = 6, returning 6 to the caller.",
      frames: [{ name: "factorial(n=3)", status: "Returning: 6" }]
    }
  ];

  const current = steps[step];

  return (
    <div className="function-visualizer-card widget-card">
      <div className="widget-header">
        <div className="widget-title">
          <Layers size={16} />
          <span>Call Stack & Frame Visualizer</span>
        </div>
      </div>
      <div className="visualizer-container">
        <div className="stack-frames-display">
          {current.frames.map((frame, idx) => (
            <div key={idx} className={`stack-frame-item ${frame.status.includes('Returning') ? 'returning' : ''} ${frame.status === 'Paused' ? 'paused' : 'active'}`}>
              <div className="frame-name">{frame.name}</div>
              <div className="frame-status">{frame.status}</div>
            </div>
          ))}
          {current.frames.length === 0 && <div className="empty-stack">Stack Empty</div>}
        </div>
        <div className="explanation-panel">
          <strong>{current.title}</strong>
          <p>{current.explanation}</p>
        </div>
        <div className="visualizer-controls">
          <button onClick={() => setStep(Math.max(0, step - 1))} disabled={step === 0}>Previous</button>
          <button onClick={() => setStep(Math.min(steps.length - 1, step + 1))} disabled={step === steps.length - 1}>Next</button>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 41. ObjectLifecycleVisualizer Component
// ==========================================
export const ObjectLifecycleVisualizer = () => {
  const [step, setStep] = useState(0);
  const steps = [
    {
      title: "1. Allocating Memory (__new__)",
      description: "When Agent('Alice') is called, Python executes the static method __new__. It allocates raw memory on the heap for the instance. At this point, the instance is blank.",
      action: "Blank Instance created at 0x01A2",
      attrs: "{}"
    },
    {
      title: "2. Setting Instance Attributes (__init__)",
      description: "Python passes the newly created instance reference (0x01A2) as the first argument 'self' to __init__('Alice'). __init__ assigns attributes to the instance namespace.",
      action: "self.name = 'Alice' assigned",
      attrs: '{"name": "Alice"}'
    },
    {
      title: "3. Constructor Return",
      description: "With initialization complete, Python returns the completed instance reference (0x01A2) back to the caller, binding it to the variable.",
      action: "alice = 0x01A2",
      attrs: '{"name": "Alice"}'
    }
  ];

  return (
    <div className="lifecycle-visualizer-card widget-card">
      <div className="widget-header">
        <div className="widget-title">
          <RefreshCw size={16} />
          <span>Object Instantiation Lifecycle</span>
        </div>
      </div>
      <div className="visualizer-container">
        <div className="lifecycle-flow">
          {steps.map((s, idx) => (
            <div key={idx} className={`flow-step ${step === idx ? 'active' : ''}`} onClick={() => setStep(idx)}>
              <span className="step-num">{idx + 1}</span>
              <span className="step-title">{s.title.split(' ')[1] || s.title}</span>
            </div>
          ))}
        </div>
        <div className="lifecycle-body">
          <div className="lifecycle-explanation">
            <strong>{steps[step].title}</strong>
            <p>{steps[step].description}</p>
          </div>
          <div className="lifecycle-state">
            <div className="state-row">
              <strong>Action:</strong> <span className="highlight-text">{steps[step].action}</span>
            </div>
            <div className="state-row">
              <strong>Namespace Attributes:</strong> <code className="inline-code">{steps[step].attrs}</code>
            </div>
          </div>
        </div>
        <div className="visualizer-controls">
          <button onClick={() => setStep(Math.max(0, step - 1))} disabled={step === 0}>Previous</button>
          <button onClick={() => setStep(Math.min(steps.length - 1, step + 1))} disabled={step === steps.length - 1}>Next</button>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 42. InheritanceDiagram Component
// ==========================================
export const InheritanceDiagram = () => {
  const [searchTerm, setSearchTerm] = useState('');
  
  const mro = [
    { name: "ToolAgent", methods: ["run_task()"], desc: "Child class inherits from Agent and ToolUser" },
    { name: "Agent", methods: ["execute()", "log()"], desc: "Base class for core execution logic" },
    { name: "ToolUser", methods: ["use_tool()", "execute()"], desc: "Mixin class for accessing external tools" },
    { name: "object", methods: ["__init__()", "__str__()"], desc: "Root base class of all Python objects" }
  ];

  const getLookupIndex = () => {
    if (!searchTerm.trim()) return -1;
    const query = searchTerm.toLowerCase().replace('()', '');
    for (let i = 0; i < mro.length; i++) {
      if (mro[i].methods.some(m => m.toLowerCase().includes(query))) {
        return i;
      }
    }
    return -1;
  };

  const lookupIdx = getLookupIndex();

  return (
    <div className="inheritance-diagram-card widget-card">
      <div className="widget-header">
        <div className="widget-title">
          <Layers size={16} />
          <span>Multiple Inheritance & MRO Lookup</span>
        </div>
      </div>
      <div className="visualizer-container">
        <div className="search-mro-box">
          <input 
            type="text" 
            placeholder="Search method (e.g. execute, use_tool, run_task)..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="widget-select"
            style={{ width: '100%', marginBottom: '14px', height: '36px', padding: '8px' }}
          />
        </div>
        {lookupIdx !== -1 && (
          <div className="mro-result-alert alert-box alert-success" style={{ marginBottom: '16px', padding: '10px 14px' }}>
            Method resolved at: <strong>{mro[lookupIdx].name}</strong> (MRO Priority)
          </div>
        )}
        <div className="mro-tree">
          {mro.map((cls, idx) => {
            const isResolvedHere = idx === lookupIdx;
            const hasPassed = lookupIdx !== -1 && idx < lookupIdx;
            return (
              <div key={idx} className="mro-node-wrapper">
                <div className={`mro-node ${isResolvedHere ? 'resolved' : ''} ${hasPassed ? 'passed' : ''}`}>
                  <div className="node-class-name">{cls.name}</div>
                  <div className="node-methods">Methods: {cls.methods.join(', ')}</div>
                  <div className="node-desc">{cls.desc}</div>
                </div>
                {idx < mro.length - 1 && <div className="mro-arrow">↓ MRO Resolution Path</div>}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 43. DecoratorVisualizer Component
// ==========================================
export const DecoratorVisualizer = () => {
  const [step, setStep] = useState(0);
  const steps = [
    {
      title: "1. Definition Phase",
      explanation: "The decorator function log_call(func) is defined, taking the target function 'func' as input, and defining a wrapper function.",
      code: `def log_call(func):
    def wrapper(*args, **kwargs):
        print("Pre-execution log...")
        res = func(*args, **kwargs)
        print("Post-execution log...")
        return res
    return wrapper`
    },
    {
      title: "2. Decoration Phase",
      explanation: "Using @log_call wraps compile_report(). At compile/import time, Python replaces compile_report with log_call(compile_report), yielding the wrapper.",
      code: `@log_call
def compile_report():
    print("Executing core function...")`
    },
    {
      title: "3. Execution (Wrapper Intercept)",
      explanation: "Calling compile_report() actually runs the wrapper. The wrapper executes first, running logging or configuration, before forwarding parameters.",
      code: `# Calling compile_report() triggers wrapper:
print("Pre-execution log...")`
    },
    {
      title: "4. Core Invocation & Exit",
      explanation: "The wrapper invokes the original compile_report(), gathers its return value, runs the post-log hook, and returns the result.",
      code: `res = func(*args, **kwargs) # Runs compile_report()
print("Post-execution log...")`
    }
  ];

  return (
    <div className="decorator-visualizer-card widget-card">
      <div className="widget-header">
        <div className="widget-title">
          <Zap size={16} />
          <span>Decorator Execution Lifecycle</span>
        </div>
      </div>
      <div className="visualizer-container">
        <div className="lifecycle-body">
          <div className="lifecycle-explanation">
            <strong>{steps[step].title}</strong>
            <p>{steps[step].explanation}</p>
          </div>
          <div className="lifecycle-code-block">
            <pre><code className="code-block">{steps[step].code}</code></pre>
          </div>
        </div>
        <div className="visualizer-controls">
          <button onClick={() => setStep(Math.max(0, step - 1))} disabled={step === 0}>Previous</button>
          <button onClick={() => setStep(Math.min(steps.length - 1, step + 1))} disabled={step === steps.length - 1}>Next</button>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 44. AsyncExecutionTimeline Component
// ==========================================
export const AsyncExecutionTimeline = () => {
  const [frame, setFrame] = useState(0);
  const frames = [
    {
      loop: "Idle / Scheduling Task A",
      taskA: "Running: Initializing web request client",
      taskB: "Pending / Queued",
      desc: "Task A starts execution. It runs synchronously until it reaches the first 'await' networking line."
    },
    {
      loop: "Awaiting Task A (Yielded to loop)",
      taskA: "Suspended: Awaiting HTTP server response (Non-blocking I/O)",
      taskB: "Running: Starts executing CPU math calculation",
      desc: "Task A reaches 'await response.get()', yielding control. The Event Loop schedules Task B. While Task A waits, Task B runs."
    },
    {
      loop: "Scheduling Task A callback",
      taskA: "Completed: Received payload",
      taskB: "Suspended: Awaiting database commit hook",
      desc: "Task B finishes or yields. The network I/O completes. Task A's response callback is pushed back into the call queue."
    }
  ];

  const current = frames[frame];

  return (
    <div className="async-visualizer-card widget-card">
      <div className="widget-header">
        <div className="widget-title">
          <Clock size={16} />
          <span>Async Event Loop Timeline</span>
        </div>
      </div>
      <div className="visualizer-container">
        <div className="timeline-tracks">
          <div className="track-row">
            <div className="track-label">🔄 Event Loop</div>
            <div className="track-state highlight-text">{current.loop}</div>
          </div>
          <div className="track-row">
            <div className="track-label">⚡ Task A (API)</div>
            <div className={`track-state status-badge ${current.taskA.includes('Running') ? 'active' : current.taskA.includes('Completed') ? 'completed' : 'suspended'}`}>
              {current.taskA}
            </div>
          </div>
          <div className="track-row">
            <div className="track-label">⚡ Task B (DB)</div>
            <div className={`track-state status-badge ${current.taskB.includes('Running') ? 'active' : current.taskB.includes('Pending') ? 'suspended' : 'suspended'}`}>
              {current.taskB}
            </div>
          </div>
        </div>
        <div className="explanation-panel">
          <p>{current.desc}</p>
        </div>
        <div className="visualizer-controls">
          <button onClick={() => setFrame(Math.max(0, frame - 1))} disabled={frame === 0}>Previous Frame</button>
          <button onClick={() => setFrame(Math.min(frames.length - 1, frame + 1))} disabled={frame === frames.length - 1}>Next Frame</button>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 45. ResourceLifecycleVisualizer Component
// ==========================================
export const ResourceLifecycleVisualizer = () => {
  const [step, setStep] = useState(0);
  const steps = [
    {
      title: "1. Entering Context (__enter__)",
      explanation: "When entering a 'with' block, Python triggers __enter__ on the manager object. It allocates, configures, or opens the resource (like a file or db) and returns it.",
      code: "with DatabaseConnection() as conn:",
      action: "conn = __enter__() runs. Connection opened."
    },
    {
      title: "2. Working inside Context",
      explanation: "Operations run securely inside the scope. If any statement throws an error, Python halts execution and redirects straight to the resource cleanup hook.",
      code: "    conn.query('SELECT * FROM agents')",
      action: "Query executes on the active connection."
    },
    {
      title: "3. Leaving Context (__exit__)",
      explanation: "Regardless of success or failure, Python guarantees __exit__ executes. It closes handles, releases sockets, and cleans up system resources.",
      code: "# Exiting the indented block scope:",
      action: "__exit__(exc_type, exc_val, exc_tb) runs. Connection closed."
    }
  ];

  return (
    <div className="resource-visualizer-card widget-card">
      <div className="widget-header">
        <div className="widget-title">
          <Lock size={16} />
          <span>Context Manager Resource Lifecycle</span>
        </div>
      </div>
      <div className="visualizer-container">
        <div className="lifecycle-body">
          <div className="lifecycle-explanation">
            <strong>{steps[step].title}</strong>
            <p>{steps[step].explanation}</p>
          </div>
          <div className="lifecycle-code-block">
            <pre><code className="code-block">{steps[step].code}</code></pre>
          </div>
          <div className="lifecycle-state" style={{ marginTop: '12px' }}>
            <strong>Action:</strong> <span className="highlight-text">{steps[step].action}</span>
          </div>
        </div>
        <div className="visualizer-controls">
          <button onClick={() => setStep(Math.max(0, step - 1))} disabled={step === 0}>Previous</button>
          <button onClick={() => setStep(Math.min(steps.length - 1, step + 1))} disabled={step === steps.length - 1}>Next</button>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 46. AgentExecutionFlow Component
// ==========================================
export const AgentExecutionFlow = () => {
  const [step, setStep] = useState(0);
  const steps = [
    {
      label: "User Prompt",
      desc: "The system accepts a text prompt, e.g., 'Summarize current sales figures for the regional offices.'",
      details: "Configures system variables and passes prompt to the planner interface."
    },
    {
      label: "Planner Module",
      desc: "The Planner decides what steps or sub-tasks are needed, referencing short-term session states.",
      details: "Formulates a list of actions: [fetch_sales_data, generate_markdown_summary]."
    },
    {
      label: "LLM Orchestration",
      desc: "The planner invokes the language model to parse query structures, routing parameters, and context bounds.",
      details: "Invokes model anthropic.claude-3-haiku to generate specific tool payload schema."
    },
    {
      label: "Tool Invocation",
      desc: "The model determines a tool execution is required, sending structured JSON parameters to the tool registry.",
      details: "Action: Invoke get_database_records(table='sales', filter='regional')."
    },
    {
      label: "Tool Execution",
      desc: "The local system runs the database query or API request in a sandbox environment and collects results.",
      details: "Stdout output: [{'office': 'West', 'sales': 420000}, {'office': 'East', 'sales': 510000}]."
    },
    {
      label: "Response Generation",
      desc: "The raw tool outputs are fed back to the LLM to compile a clean, final human-readable response.",
      details: "Final Answer: 'West sales are $420k, East sales are $510k. Total sales represent $930k.'"
    }
  ];

  return (
    <div className="agent-flow-card widget-card">
      <div className="widget-header">
        <div className="widget-title">
          <Cpu size={16} style={{ color: 'var(--accent-color)' }} />
          <span>Agent Execution & Planning Flow</span>
        </div>
      </div>
      <div className="visualizer-container">
        <div className="agent-stepper">
          {steps.map((s, idx) => {
            const isActive = idx === step;
            return (
              <div 
                key={idx} 
                className={`stepper-node ${isActive ? 'active' : ''}`}
                onClick={() => setStep(idx)}
              >
                <div className="node-dot">{idx + 1}</div>
                <div className="node-label">{s.label}</div>
              </div>
            );
          })}
        </div>
        <div className="step-explanation-box">
          <div className="step-name">{steps[step].label} Details</div>
          <p className="step-desc">{steps[step].desc}</p>
          <div className="step-system-info">
            <strong>System Actions:</strong>
            <pre><code>{steps[step].details}</code></pre>
          </div>
        </div>
        <div className="visualizer-controls">
          <button onClick={() => setStep(Math.max(0, step - 1))} disabled={step === 0}>Previous Step</button>
          <button onClick={() => setStep(Math.min(steps.length - 1, step + 1))} disabled={step === steps.length - 1}>Next Step</button>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 47. InteractivePlayground Component
// ==========================================
export const InteractivePlayground = ({ initialCode }) => {
  const [code, setCode] = useState(initialCode ? initialCode.trim() : '');
  const [output, setOutput] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [success, setSuccess] = useState(null);
  const [explanation, setExplanation] = useState('');

  const handleRun = async () => {
    setIsRunning(true);
    setSuccess(null);
    setExplanation('');
    try {
      const response = await fetch('/api/playground/run-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
      });
      const data = await response.json();
      if (data.success) {
        setSuccess(true);
        setOutput(data.stdout || data.stderr ? `${data.stdout}${data.stderr}` : 'Executed successfully with no output.');
      } else {
        setSuccess(false);
        setOutput(data.stderr || 'Execution failed.');
      }
    } catch (e) {
      setSuccess(false);
      setOutput(`Error running script: ${e.message}`);
    } finally {
      setIsRunning(false);
    }
  };

  const handleExplain = () => {
    const lowerCode = code.toLowerCase();
    let explanationText = "";
    if (lowerCode.includes('def') && lowerCode.includes('wrapper')) {
      explanationText = "• This code sets up a standard Python Decorator wrapper.\n• The wrapper intercepts calls to the target function.\n• It executes some pre-hooks (like printing logs), calls the original function, then executes post-hooks.";
    } else if (lowerCode.includes('async') && lowerCode.includes('await')) {
      explanationText = "• This code uses Python asyncio primitives for non-blocking execution.\n• The 'async' keyword registers a coroutine.\n• 'await' pauses the execution of this coroutine and returns control back to the Event Loop, allowing other tasks to run.";
    } else if (lowerCode.includes('with') && lowerCode.includes('class')) {
      explanationText = "• This code implements a Context Manager.\n• The 'with' statement calls __enter__() to open the connection.\n• When exiting the code block, it executes __exit__() to safely release/close the resources.";
    } else if (lowerCode.includes('class') && lowerCode.includes('self')) {
      explanationText = "• This code declares a custom Class.\n• __init__ is the initializer method that configures the initial attributes of an object when created.\n• 'self' represents the instance pointer of the object.";
    } else {
      explanationText = "• This is an executable Python script.\n• Python is dynamically typed, evaluating and running code line-by-line.\n• It allocates heap space for values and variables dynamically.";
    }
    setExplanation(explanationText);
  };

  return (
    <div className="playground-card widget-card">
      <div className="widget-header">
        <div className="widget-title">
          <Terminal size={16} />
          <span>Interactive Code Sandbox</span>
        </div>
        <div className="header-actions">
          <button onClick={() => setCode(initialCode || '')} className="widget-btn-icon" title="Reset Code">Reset</button>
          <button 
            onClick={() => {
              navigator.clipboard.writeText(code);
            }} 
            className="widget-btn-icon" 
            title="Copy Code"
          >
            Copy
          </button>
        </div>
      </div>
      <div className="playground-body">
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          className="playground-editor"
          spellCheck="false"
          rows={7}
        />
        <div className="playground-controls">
          <button onClick={handleRun} disabled={isRunning} className="btn-run">
            {isRunning ? <RefreshCw size={14} className="loader-spinner" /> : <Play size={14} />}
            <span>Run Code</span>
          </button>
          <button onClick={handleExplain} className="btn-explain">Explain Output</button>
        </div>
        {output && (
          <div className={`widget-console ${success === false ? 'console-error' : 'console-success'}`}>
            <div className="console-header">Console Output</div>
            <pre>{output}</pre>
          </div>
        )}
        {explanation && (
          <div className="explanation-box" style={{ marginTop: '12px', borderLeft: '3px solid var(--accent-color)', padding: '10px 14px', background: 'rgba(139, 92, 246, 0.05)' }}>
            <strong style={{ display: 'block', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--accent-color)', marginBottom: '6px' }}>AI Code Breakdown</strong>
            <p style={{ whiteSpace: 'pre-line', fontSize: '0.85rem', color: 'var(--text-secondary)', margin: '0' }}>{explanation}</p>
          </div>
        )}
      </div>
    </div>
  );
};

// ==========================================
// 48. CodeExplainer Component
// ==========================================
export const CodeExplainer = ({ code, lines }) => {
  const [activeLine, setActiveLine] = useState(null);
  const codeLines = code ? code.trim().split('\n') : [];
  const lineDetails = Array.isArray(lines) ? lines : [];

  return (
    <div className="code-explainer-card widget-card">
      <div className="widget-header">
        <div className="widget-title">
          <Code size={16} />
          <span>Click any line to dissect</span>
        </div>
      </div>
      <div className="explainer-container">
        <div className="explainer-code-pane">
          {codeLines.map((line, idx) => {
            const isClickable = lineDetails[idx] !== undefined;
            return (
              <div 
                key={idx} 
                className={`explainer-line ${activeLine === idx ? 'active' : ''} ${isClickable ? 'clickable' : ''}`}
                onClick={() => isClickable && setActiveLine(idx)}
              >
                <span className="line-num">{idx + 1}</span>
                <span className="line-text">{line || ' '}</span>
              </div>
            );
          })}
        </div>
        <div className="explainer-details-pane">
          {activeLine !== null && lineDetails[activeLine] ? (
            <div className="details-box">
              <div className="details-header">Line {activeLine + 1} Anatomy</div>
              <div className="details-content">
                <p><strong>Operation:</strong> {lineDetails[activeLine].operation}</p>
                <p><strong>Variables/Scope:</strong> {lineDetails[activeLine].scope || 'Local namespace'}</p>
                <p><strong>Details:</strong> {lineDetails[activeLine].explanation}</p>
              </div>
            </div>
          ) : (
            <div className="details-placeholder">
              Click on a highlighted line of code to inspect scope variables, object types, and reference paths.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 49. Quiz Component
// ==========================================
export const Quiz = ({ questions, question, options, answerIndex, correctIndex, explanation }) => {
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [scores, setScores] = useState(null);

  let qList = [];
  if (Array.isArray(questions)) {
    qList = questions;
  } else if (question) {
    qList = [{
      question,
      options: Array.isArray(options) ? options : [],
      correctIndex: typeof answerIndex !== 'undefined' ? answerIndex : correctIndex,
      explanation,
      type: 'multiple'
    }];
  }

  if (qList.length === 0) return null;

  const handleSelectOption = (qIdx, optIdx) => {
    if (submitted) return;
    setAnswers(prev => ({ ...prev, [qIdx]: optIdx }));
  };

  const handleTextChange = (qIdx, val) => {
    if (submitted) return;
    setAnswers(prev => ({ ...prev, [qIdx]: val }));
  };

  const handleSubmit = () => {
    let correctCount = 0;
    qList.forEach((q, idx) => {
      const userAns = answers[idx];
      if (q.type === 'fill') {
        const cleanedUser = (userAns || '').trim().toLowerCase();
        const cleanedCorrect = q.correctAnswer.toLowerCase();
        if (cleanedUser === cleanedCorrect) correctCount++;
      } else {
        if (userAns === q.correctIndex) correctCount++;
      }
    });
    setScores(correctCount);
    setSubmitted(true);
  };

  const handleReset = () => {
    setAnswers({});
    setSubmitted(false);
    setScores(null);
  };

  return (
    <div className="quiz-card widget-card">
      <div className="widget-header">
        <div className="widget-title">
          <HelpCircle size={16} />
          <span>Interactive Quiz Verification</span>
        </div>
      </div>
      <div className="quiz-body">
        {qList.map((q, qIdx) => {
          const userAns = answers[qIdx];
          const isCorrect = q.type === 'fill' 
            ? (userAns || '').trim().toLowerCase() === q.correctAnswer.toLowerCase()
            : userAns === q.correctIndex;

          return (
            <div key={qIdx} className="quiz-question-block">
              <div className="question-text">{qIdx + 1}. {q.question}</div>
              
              {q.type === 'multiple' && (
                <div className="options-grid">
                  {q.options.map((opt, optIdx) => {
                    const isSelected = userAns === optIdx;
                    let optClass = '';
                    if (submitted) {
                      if (optIdx === q.correctIndex) optClass = 'option-correct';
                      else if (isSelected) optClass = 'option-incorrect';
                    } else if (isSelected) {
                      optClass = 'option-selected';
                    }
                    return (
                      <button
                        key={optIdx}
                        className={`quiz-option-btn ${optClass}`}
                        onClick={() => handleSelectOption(qIdx, optIdx)}
                        disabled={submitted}
                      >
                        {opt}
                      </button>
                    );
                  })}
                </div>
              )}

              {q.type === 'tf' && (
                <div className="options-grid flex-row">
                  {["True", "False"].map((opt, optIdx) => {
                    const isSelected = userAns === optIdx;
                    let optClass = '';
                    if (submitted) {
                      if (optIdx === q.correctIndex) optClass = 'option-correct';
                      else if (isSelected) optClass = 'option-incorrect';
                    } else if (isSelected) {
                      optClass = 'option-selected';
                    }
                    return (
                      <button
                        key={optIdx}
                        className={`quiz-option-btn tf-btn ${optClass}`}
                        onClick={() => handleSelectOption(qIdx, optIdx)}
                        disabled={submitted}
                      >
                        {opt}
                      </button>
                    );
                  })}
                </div>
              )}

              {q.type === 'fill' && (
                <div className="fill-input-wrapper">
                  <input
                    type="text"
                    placeholder="Type your answer..."
                    value={userAns || ''}
                    onChange={(e) => handleTextChange(qIdx, e.target.value)}
                    disabled={submitted}
                    className="widget-select"
                    style={{ width: '100%', height: '36px', padding: '8px' }}
                  />
                  {submitted && (
                    <div className={`answer-feedback ${isCorrect ? 'text-green' : 'text-red'}`} style={{ marginTop: '6px', fontSize: '0.85rem' }}>
                      {isCorrect ? "Correct!" : `Incorrect. Correct answer: ${q.correctAnswer}`}
                    </div>
                  )}
                </div>
              )}

              {submitted && q.explanation && (
                <div className="question-explanation">
                  <strong>Explanation:</strong> {q.explanation}
                </div>
              )}
            </div>
          );
        })}
        
        <div className="quiz-controls-row">
          {!submitted ? (
            <button onClick={handleSubmit} className="btn-primary" style={{ padding: '8px 16px', borderRadius: '4px', cursor: 'pointer' }}>Submit Quiz</button>
          ) : (
            <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
              <div className="quiz-score-badge" style={{ fontWeight: '700', fontSize: '0.9rem' }}>
                Score: {scores} / {qList.length}
              </div>
              <button onClick={handleReset} className="btn-secondary" style={{ padding: '8px 16px', borderRadius: '4px', cursor: 'pointer' }}>Retry</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 50. InterviewQuestion Component
// ==========================================
export const InterviewQuestion = ({ question, q, difficulty, answer, a, followUp }) => {
  const [isOpen, setIsOpen] = useState(false);
  const displayQuestion = question || q || '';
  const displayAnswer = answer || a || '';

  // Auto-classify difficulty to show Beginner, Medium, and Advanced levels
  let displayDifficulty = difficulty;
  if (!displayDifficulty) {
    const text = displayQuestion.toLowerCase();
    if (
      text.includes('mro') ||
      text.includes('inheritance') ||
      text.includes('__exit__') ||
      text.includes('asyncio') ||
      text.includes('event loop') ||
      text.includes('decorator') ||
      text.includes('blocking io') ||
      text.includes('concurrency') ||
      text.includes('multiprocessing') ||
      text.includes('thread') ||
      text.includes('tool registration') ||
      text.includes('schema') ||
      text.includes('reflection') ||
      text.includes('wraps') ||
      text.includes('exit__')
    ) {
      displayDifficulty = 'Advanced';
    } else if (
      text.includes('dynamic typing') ||
      text.includes('variable') ||
      text.includes('operator') ||
      text.includes('control flow') ||
      text.includes('loop') ||
      text.includes('if __name__') ||
      text.includes('pathlib') ||
      text.includes('pip install')
    ) {
      displayDifficulty = 'Beginner';
    } else {
      displayDifficulty = 'Medium';
    }
  }

  return (
    <div className="interview-q-item">
      <button className="q-header-btn" onClick={() => setIsOpen(!isOpen)}>
        <div className="q-title-row">
          <span className={`difficulty-badge ${displayDifficulty.toLowerCase()}`}>{displayDifficulty}</span>
          <span className="q-text">{displayQuestion}</span>
        </div>
        {isOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
      </button>
      {isOpen && (
        <div className="q-body-content">
          <div className="answer-section">
            <strong>Model Answer:</strong>
            <p>{displayAnswer}</p>
          </div>
          {followUp && (
            <div className="followup-section">
              <strong>Follow-up Questions:</strong>
              <p>{followUp}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};


// ==========================================
// 51. InterviewQuestions Component
// ==========================================
export const InterviewQuestions = ({ children }) => (
  <div className="interview-questions-card widget-card">
    <div className="widget-header">
      <div className="widget-title">
        <HelpCircle size={16} />
        <span>Developer Interview Mode</span>
      </div>
    </div>
    <div className="interview-list-container">{children}</div>
  </div>
);
