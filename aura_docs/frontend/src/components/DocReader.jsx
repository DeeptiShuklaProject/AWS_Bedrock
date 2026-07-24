import React, { useState, useMemo, useEffect, useRef } from 'react';
import { parseMarkdown } from '../utils/markdownParser';
import { 
  Play, 
  Code, 
  RefreshCw, 
  ChevronLeft, 
  ChevronRight, 
  BookOpen, 
  ArrowUp
} from 'lucide-react';
import mermaid from 'mermaid';

mermaid.initialize({
  startOnLoad: false,
  theme: 'dark',
  securityLevel: 'loose',
  fontFamily: 'Inter, system-ui, sans-serif'
});

const CodePlaygroundWidget = ({ initialCode }) => {
  const [code, setCode] = useState(initialCode ? initialCode.trim() : '');
  const [output, setOutput] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [success, setSuccess] = useState(null);

  const handleRunCode = async () => {
    setIsRunning(true);
    setSuccess(null);
    try {
      const response = await fetch('/api/playground/run-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
      });
      const data = await response.json();
      if (data.success) {
        setSuccess(true);
        setOutput(data.stdout || data.stderr ? `${data.stdout}${data.stderr}` : 'Code executed successfully.');
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
    <div style={{ margin: '20px 0', background: '#0b0f19', border: '1px solid var(--border-color)', borderRadius: '12px', overflow: 'hidden' }}>
      <div style={{ padding: '10px 16px', background: 'var(--bg-card)', borderBottom: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.8rem', fontWeight: 700, color: 'var(--accent-indigo)' }}>
          <Code size={15} />
          <span>Interactive Python Console</span>
        </div>
        <button 
          onClick={handleRunCode} 
          disabled={isRunning}
          className="primary-cta-btn"
          style={{ padding: '4px 12px', fontSize: '0.75rem' }}
        >
          {isRunning ? <RefreshCw size={12} className="animate-spin" /> : <Play size={12} />}
          <span>Run Code</span>
        </button>
      </div>
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        rows={6}
        style={{ width: '100%', padding: '16px', background: 'transparent', fontFamily: 'var(--font-mono)', fontSize: '0.85rem', color: '#34d399', border: 'none', outline: 'none', resize: 'vertical' }}
        spellCheck="false"
      />
      {output && (
        <div style={{ padding: '14px 16px', fontFamily: 'var(--font-mono)', fontSize: '0.8rem', borderTop: '1px solid var(--border-color)', background: success === false ? 'rgba(244,63,94,0.15)' : 'rgba(15,23,42,0.9)', color: success === false ? '#fda4af' : '#6ee7b7' }}>
          <div style={{ fontSize: '0.68rem', fontWeight: 800, textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: '4px' }}>Output:</div>
          <pre style={{ whiteSpace: 'pre-wrap', margin: 0 }}>{output}</pre>
        </div>
      )}
    </div>
  );
};

const MermaidDiagram = ({ code }) => {
  const [svg, setSvg] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;
    const renderDiagram = async () => {
      try {
        const id = `mermaid-${Math.random().toString(36).substring(2, 9)}`;
        const { svg: svgOutput } = await mermaid.render(id, code);
        if (isMounted) {
          setSvg(svgOutput);
          setError(null);
        }
      } catch (err) {
        if (isMounted) setError(err.message || 'Failed to render diagram.');
      }
    };

    renderDiagram();
    return () => { isMounted = false; };
  }, [code]);

  if (error) {
    return (
      <div style={{ margin: '20px 0', padding: '16px', borderRadius: '12px', background: 'rgba(244,63,94,0.15)', border: '1px solid rgba(244,63,94,0.3)', color: '#fda4af', fontSize: '0.8rem', fontFamily: 'var(--font-mono)' }}>
        <strong>Diagram Error:</strong>
        <pre style={{ whiteSpace: 'pre-wrap', marginTop: '6px' }}>{error}</pre>
      </div>
    );
  }

  return (
    <div style={{ margin: '24px 0', padding: '24px', background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '16px', overflowX: 'auto', display: 'flex', justifyContent: 'center' }}>
      <div dangerouslySetInnerHTML={{ __html: svg }} />
    </div>
  );
};

const DocReader = ({ 
  activeDoc, 
  docContent, 
  isLoading, 
  onSelectDoc, 
  navItems = [],
  onExtractHeadings,
  onOpenImage,
  onOpenPlayground
}) => {
  const contentRef = useRef(null);

  useEffect(() => {
    if (!docContent) {
      if (onExtractHeadings) onExtractHeadings([]);
      return;
    }

    const headingRegex = /^(#{1,4})\s+(.*)$/gm;
    const extracted = [];
    let match;

    while ((match = headingRegex.exec(docContent)) !== null) {
      const level = match[1].length;
      const text = match[2].trim();
      const id = text
        .toLowerCase()
        .trim()
        .replace(/<[^>]*>/g, '')
        .replace(/[^\w\s-]/g, '')
        .replace(/[\s_]+/g, '-')
        .replace(/^-+|-+$/g, '');
      extracted.push({ level, text, id });
    }

    if (onExtractHeadings) onExtractHeadings(extracted);
  }, [docContent, onExtractHeadings]);

  const handleContentClick = (e) => {
    const img = e.target.closest('img');
    if (img && onOpenImage) {
      e.preventDefault();
      onOpenImage(img.getAttribute('src'), img.getAttribute('alt'));
      return;
    }

    const link = e.target.closest('a');
    if (link && link.classList.contains('doc-link')) {
      const href = link.getAttribute('href');
      const isExternal = href && (href.startsWith('http') || href.startsWith('//'));
      const isAnchor = href && href.startsWith('#');

      if (href && !isExternal && !isAnchor) {
        e.preventDefault();
        let resolvedPath = href;
        if (activeDoc && activeDoc.includes('/')) {
          const activeDir = activeDoc.substring(0, activeDoc.lastIndexOf('/'));
          resolvedPath = `${activeDir}/${href}`;
        }
        
        const parts = resolvedPath.split('/');
        const stack = [];
        for (const part of parts) {
          if (part === '.' || part === '') continue;
          if (part === '..') stack.pop();
          else stack.push(part);
        }
        onSelectDoc(stack.join('/'));
      }
    }
  };

  const flattenNavItems = (items) => {
    let list = [];
    if (!Array.isArray(items)) return list;

    items.forEach(item => {
      if (item.href || item.path) {
        list.push({
          title: item.title || item.name,
          path: item.href || item.path
        });
      }
      const kids = item.contents || item.children;
      if (Array.isArray(kids)) list = list.concat(flattenNavItems(kids));
    });
    return list;
  };

  const allPages = useMemo(() => flattenNavItems(navItems), [navItems]);
  const currentIndex = allPages.findIndex(p => p.path === activeDoc);
  const prevPage = currentIndex > 0 ? allPages[currentIndex - 1] : null;
  const nextPage = currentIndex >= 0 && currentIndex < allPages.length - 1 ? allPages[currentIndex + 1] : null;

  const renderSegments = useMemo(() => {
    if (!docContent) return null;

    const segments = [];
    let lastIndex = 0;
    let match;
    const blockRegex = /```(?:widget:([a-zA-Z0-9_-]+)|(mermaid))\n([\s\S]*?)\n```/g;

    while ((match = blockRegex.exec(docContent)) !== null) {
      const textBefore = docContent.substring(lastIndex, match.index);
      if (textBefore.trim()) segments.push({ type: 'markdown', content: textBefore });

      if (match[2] === 'mermaid') {
        segments.push({ type: 'mermaid', content: match[3] });
      } else {
        segments.push({ type: 'widget', widgetType: match[1], content: match[3] });
      }
      lastIndex = blockRegex.lastIndex;
    }

    const textAfter = docContent.substring(lastIndex);
    if (textAfter.trim() || segments.length === 0) {
      segments.push({ type: 'markdown', content: textAfter });
    }

    return segments;
  }, [docContent]);

  if (isLoading) {
    return (
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justify: 'center', padding: '60px', color: 'var(--text-secondary)' }}>
        <div style={{ width: '32px', height: '32px', border: '3px solid var(--accent-indigo)', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
        <p style={{ marginTop: '16px', fontSize: '0.88rem', fontWeight: 600 }}>Loading documentation...</p>
      </div>
    );
  }

  const pathParts = activeDoc ? activeDoc.split('/') : [];

  return (
    <div className="doc-canvas" onClick={handleContentClick}>
      {/* Breadcrumb */}
      {pathParts.length > 0 && (
        <div className="breadcrumb-trail">
          <BookOpen size={14} style={{ color: 'var(--accent-indigo)' }} />
          {pathParts.map((part, idx) => (
            <React.Fragment key={idx}>
              {idx > 0 && <span>/</span>}
              <span style={{ color: idx === pathParts.length - 1 ? 'var(--text-primary)' : 'var(--text-secondary)', fontWeight: idx === pathParts.length - 1 ? 700 : 400 }}>
                {part.replace('.md', '').replace(/_/g, ' ')}
              </span>
            </React.Fragment>
          ))}
        </div>
      )}

      {/* Article Content */}
      <article ref={contentRef} className="doc-content">
        {renderSegments && renderSegments.map((segment, idx) => {
          if (segment.type === 'markdown') {
            const html = parseMarkdown(segment.content);
            return (
              <div key={idx} dangerouslySetInnerHTML={{ __html: html }} />
            );
          } else if (segment.type === 'mermaid') {
            return <MermaidDiagram key={idx} code={segment.content} />;
          } else if (segment.widgetType === 'code') {
            return <CodePlaygroundWidget key={idx} initialCode={segment.content} />;
          } else {
            return null;
          }
        })}
      </article>

      {/* Prev / Next Footer Buttons */}
      <div style={{ marginTop: '48px', paddingTop: '24px', borderTop: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '16px' }}>
        {prevPage ? (
          <button onClick={() => onSelectDoc(prevPage.path)} className="secondary-cta-btn" style={{ padding: '10px 16px', fontSize: '0.82rem' }}>
            <ChevronLeft size={16} />
            <div style={{ textAlign: 'left' }}>
              <div style={{ fontSize: '0.65rem', textTransform: 'uppercase', color: 'var(--text-muted)' }}>Previous</div>
              <div>{prevPage.title}</div>
            </div>
          </button>
        ) : <div />}

        <button onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })} className="secondary-cta-btn" style={{ padding: '8px 14px', fontSize: '0.78rem' }}>
          <ArrowUp size={14} />
          <span>Top</span>
        </button>

        {nextPage ? (
          <button onClick={() => onSelectDoc(nextPage.path)} className="secondary-cta-btn" style={{ padding: '10px 16px', fontSize: '0.82rem' }}>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '0.65rem', textTransform: 'uppercase', color: 'var(--text-muted)' }}>Next</div>
              <div>{nextPage.title}</div>
            </div>
            <ChevronRight size={16} />
          </button>
        ) : <div />}
      </div>
    </div>
  );
};

export default DocReader;
