import React, { useState } from 'react';
import { 
  Copy, 
  Check, 
  Play, 
  Download, 
  Maximize2, 
  Minimize2, 
  ChevronDown, 
  ChevronUp, 
  HelpCircle, 
  Terminal, 
  Code2, 
  RefreshCw 
} from 'lucide-react';

export const InteractiveCodeBlock = ({ 
  code = '', 
  language = 'python', 
  title = '', 
  highlightLines = [] 
}) => {
  const [copied, setCopied] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showExplanation, setShowExplanation] = useState(false);
  const [selectedLine, setSelectedLine] = useState(null);
  const [isRunning, setIsRunning] = useState(false);
  const [output, setOutput] = useState(null);

  const lines = code.trim().split('\n');
  const isLongCode = lines.length > 18;

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const extMap = { python: 'py', py: 'py', javascript: 'js', js: 'js', json: 'json', bash: 'sh', shell: 'sh' };
    const ext = extMap[language.toLowerCase()] || 'txt';
    const blob = new Blob([code], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `code_snippet.${ext}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleRunCode = async () => {
    setIsRunning(true);
    setOutput(null);
    try {
      const response = await fetch('/api/playground/run-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
      });
      const data = await response.json();
      if (data.success) {
        setOutput({ success: true, text: data.stdout || data.stderr || 'Executed cleanly (no output).' });
      } else {
        setOutput({ success: false, text: data.stderr || 'Execution failed.' });
      }
    } catch (e) {
      setOutput({ success: false, text: `Execution error: ${e.message}` });
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className={`interactive-code-container ${isFullscreen ? 'fullscreen-overlay' : ''}`}>
      {/* Code Block Top Control Header */}
      <div className="code-block-header">
        <div className="code-lang-info">
          <div className="code-lang-badge">
            <Code2 size={13} />
            <span>{language.toUpperCase()}</span>
          </div>
          {title && <span className="code-block-title">{title}</span>}
          <span className="code-line-count">{lines.length} lines</span>
        </div>

        <div className="code-actions">
          {/* Explain Line Toggle */}
          <button 
            onClick={() => setShowExplanation(!showExplanation)}
            className={`code-action-btn ${showExplanation ? 'active' : ''}`}
            title="Toggle line explanations"
          >
            <HelpCircle size={14} />
            <span>Explain</span>
          </button>

          {/* Run Snippet (for Python/Bash) */}
          {(language.toLowerCase().includes('py') || language.toLowerCase().includes('script')) && (
            <button 
              onClick={handleRunCode}
              disabled={isRunning}
              className="code-action-btn run-btn"
              title="Run python code snippet"
            >
              {isRunning ? <RefreshCw size={14} className="loader-spinner" /> : <Play size={14} />}
              <span>Run Snippet</span>
            </button>
          )}

          {/* Download */}
          <button 
            onClick={handleDownload}
            className="code-action-btn"
            title="Download snippet"
          >
            <Download size={14} />
          </button>

          {/* Copy */}
          <button 
            onClick={handleCopy}
            className="code-action-btn"
            title="Copy code"
          >
            {copied ? <Check size={14} color="#10b981" /> : <Copy size={14} />}
            <span>{copied ? "Copied" : "Copy"}</span>
          </button>

          {/* Fullscreen */}
          <button 
            onClick={() => setIsFullscreen(!isFullscreen)}
            className="code-action-btn"
            title={isFullscreen ? "Exit Fullscreen" : "Fullscreen"}
          >
            {isFullscreen ? <Minimize2 size={14} /> : <Maximize2 size={14} />}
          </button>
        </div>
      </div>

      {/* Code Content Container */}
      <div className={`code-body-wrapper ${!isExpanded && isLongCode && !isFullscreen ? 'collapsed-height' : ''}`}>
        <table className="code-table">
          <tbody>
            {lines.map((lineText, idx) => {
              const lineNum = idx + 1;
              const isHighlighted = highlightLines.includes(lineNum) || selectedLine === lineNum;
              return (
                <tr 
                  key={idx} 
                  className={`code-line-row ${isHighlighted ? 'highlighted-row' : ''}`}
                  onClick={() => setSelectedLine(selectedLine === lineNum ? null : lineNum)}
                >
                  <td className="line-num">{lineNum}</td>
                  <td className="line-code">
                    <code>{lineText}</code>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Expand/Collapse Banner for Long Snippets */}
      {isLongCode && !isFullscreen && (
        <button 
          onClick={() => setIsExpanded(!isExpanded)}
          className="code-expand-banner"
        >
          {isExpanded ? (
            <>
              <ChevronUp size={14} />
              <span>Collapse Code Block</span>
            </>
          ) : (
            <>
              <ChevronDown size={14} />
              <span>Show Full Code ({lines.length} lines)</span>
            </>
          )}
        </button>
      )}

      {/* Line Explanation Drawer */}
      {showExplanation && (
        <div className="line-explanation-box">
          <div className="explanation-header">
            <HelpCircle size={14} />
            <span>
              {selectedLine 
                ? `Explanation for Line ${selectedLine}` 
                : 'Click any line in the code block above for detailed walkthrough:'}
            </span>
          </div>
          <div className="explanation-body">
            {selectedLine ? (
              <p>
                Line {selectedLine} contains: <code>{lines[selectedLine - 1]}</code>
                <br />
                <em>This line initializes the execution logic or parameters for the agent runtime environment.</em>
              </p>
            ) : (
              <p>
                This code snippet demonstrates standard production patterns for Amazon Bedrock AgentCore.
                Select any line number to view its line-by-line function.
              </p>
            )}
          </div>
        </div>
      )}

      {/* Execution Console Output */}
      {output && (
        <div className={`code-output-console ${output.success ? 'output-success' : 'output-error'}`}>
          <div className="console-title-bar">
            <Terminal size={14} />
            <span>Execution Output</span>
          </div>
          <pre>{output.text}</pre>
        </div>
      )}
    </div>
  );
};
