import React, { useState, useMemo, useEffect, useRef } from 'react';
import { parseMarkdown } from '../utils/markdownParser';
import { 
  Play, Send, Sliders, Code, Database, RefreshCw, 
  Edit3, Check, Search, Star, Compass, ChevronRight 
} from 'lucide-react';
import mermaid from 'mermaid';
import * as Interactive from './InteractiveComponents';

// Map MDX tags to React widgets
const componentMap = {
  Badge: Interactive.Badge,
  LearningObjectives: Interactive.LearningObjectives,
  WhyItMatters: Interactive.WhyItMatters,
  ConceptOverviewCard: Interactive.ConceptCard,
  ConceptCard: Interactive.ConceptCard,
  RealWorldExample: Interactive.RealWorldExample,
  InteractiveDiagram: Interactive.InteractiveDiagram,
  SyntaxTabs: Interactive.SyntaxTabs,
  CodeExplanation: Interactive.CodeExplanation,
  InteractiveExample: Interactive.InteractiveExample,
  InteractivePlayground: Interactive.InteractivePlayground,
  ExecutionVisualizer: Interactive.ExecutionVisualizer,
  MemoryVisualizer: Interactive.MemoryVisualizer,
  BestPractices: Interactive.BestPractices,
  CommonMistakes: Interactive.CommonMistakes,
  Quiz: Interactive.Quiz,
  Flashcards: Interactive.FlashCards,
  FlashCards: Interactive.FlashCards,
  PracticeExercise: Interactive.PracticeProblem,
  PracticeProblem: Interactive.PracticeProblem,
  InterviewQuestions: Interactive.InterviewQuestions,
  InterviewQuestion: Interactive.InterviewQuestion,
  InterviewAccordion: Interactive.InterviewQuestions,
  KeyTakeaways: Interactive.KeyTakeaways,
  NextTopic: Interactive.NextTopic,
  
  // Custom Visualizers
  DecoratorVisualizer: Interactive.DecoratorVisualizer,
  FunctionExecutionVisualizer: Interactive.FunctionExecutionVisualizer,
  ObjectLifecycleVisualizer: Interactive.ObjectLifecycleVisualizer,
  InheritanceDiagram: Interactive.InheritanceDiagram,
  AsyncExecutionTimeline: Interactive.AsyncExecutionTimeline,
  ResourceLifecycleVisualizer: Interactive.ResourceLifecycleVisualizer,
  AgentExecutionFlow: Interactive.AgentExecutionFlow,
  CodeExplainer: Interactive.CodeExplainer,
  
  // Existing utilities
  InfoCard: Interactive.InfoCard,
  Tip: Interactive.Tip,
  Warning: Interactive.Warning,
  Callout: Interactive.Callout,
  ExpandableSection: Interactive.ExpandableSection,
  Accordion: Interactive.Accordion,
  AccordionItem: Interactive.AccordionItem,
  Tabs: Interactive.Tabs,
  Tab: Interactive.Tab,
  CodeBlock: Interactive.CodeBlock,
  CodeComparison: Interactive.CodeComparison,
  Timeline: Interactive.Timeline,
  TimelineItem: Interactive.TimelineItem,
  StepByStep: Interactive.StepByStep,
  Step: Interactive.Step,
  Checklist: Interactive.Checklist,
  CopyCommand: Interactive.CopyCommand,
  AgentArchitectureDiagram: Interactive.AgentArchitectureDiagram,
  WorkflowVisualizer: Interactive.WorkflowVisualizer,
  ExecutionTimeline: Interactive.ExecutionTimeline,
  ComparisonTable: Interactive.ComparisonTable,
  ProgressTracker: Interactive.ProgressTracker
};

function parseMDXContent(content) {
  const tagRegex = /(<\/?[A-Z][A-Za-z0-9_]*(?:\s+[a-zA-Z0-9_-]+=(?:"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|\[[^\]]*\]|{(?:[^{}]|(?:{[^{}]*}))*}|{[^}]+}|\d+|true|false))*?\s*\/?>)/g;
  const tokens = content.split(tagRegex);
  
  const root = { type: 'root', children: [] };
  const stack = [root];
  
  for (let i = 0; i < tokens.length; i++) {
    const token = tokens[i];
    if (!token) continue;
    
    if (token.startsWith('<') && token.endsWith('>')) {
      const isClosing = token.startsWith('</');
      const isSelfClosing = token.endsWith('/>');
      
      const nameMatch = token.match(/^<\/?([A-Z][A-Za-z0-9_]*)/);
      const tagName = nameMatch ? nameMatch[1] : '';
      
      if (isClosing) {
        if (stack.length > 1 && stack[stack.length - 1].type === tagName) {
          stack.pop();
        }
      } else {
        const props = {};
        const propRegex = /([a-zA-Z0-9_-]+)=(?:"((?:[^"\\]|\\.)*)"|'((?:[^'\\]|\\.)*)'|\[([^\]]*)\]|{([^}]*)}|([^\s>]+))/g;
        let propMatch;
        while ((propMatch = propRegex.exec(token)) !== null) {
          const key = propMatch[1];
          const doubleQuoted = propMatch[2];
          const singleQuoted = propMatch[3];
          const bracketed = propMatch[4];
          const braced = propMatch[5];
          const simple = propMatch[6];
          
          if (doubleQuoted !== undefined) {
            try {
              props[key] = JSON.parse('"' + doubleQuoted + '"');
            } catch (e) {
              props[key] = doubleQuoted;
            }
          } else if (singleQuoted !== undefined) {
            props[key] = singleQuoted.replace(/\\'/g, "'").replace(/\\\\/g, "\\");
          } else if (bracketed !== undefined) {
            try {
              props[key] = JSON.parse('[' + bracketed + ']');
            } catch (e) {
              props[key] = bracketed;
            }
          } else if (braced !== undefined) {
            const val = braced.trim();
            if ((val.startsWith('[') && val.endsWith(']')) || (val.startsWith('{') && val.endsWith('}'))) {
              try {
                props[key] = JSON.parse(val);
              } catch (e) {
                try {
                  props[key] = Function(`return ${val}`)();
                } catch (err) {
                  props[key] = val;
                }
              }
            } else if (val === 'true') props[key] = true;
            else if (val === 'false') props[key] = false;
            else if (!isNaN(val) && val !== '') props[key] = Number(val);
            else props[key] = val;
          } else if (simple !== undefined) {
            const val = simple.trim();
            if (val === 'true') props[key] = true;
            else if (val === 'false') props[key] = false;
            else if (!isNaN(val) && val !== '') props[key] = Number(val);
            else props[key] = val;
          }
        }
        
        const node = {
          type: tagName,
          props: props,
          children: []
        };
        
        stack[stack.length - 1].children.push(node);
        
        if (!isSelfClosing) {
          stack.push(node);
        }
      }
    } else {
      stack[stack.length - 1].children.push({
        type: 'text',
        content: token
      });
    }
  }
  
  return root.children;
}

const getYoutubeId = (url) => {
  if (!url) return null;
  const match = url.match(/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/);
  return match ? match[1] : null;
};

// ==========================================
// 1. Code Playground Widget
// ==========================================
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
        setOutput(data.stdout || data.stderr ? `${data.stdout}${data.stderr}` : 'Code executed successfully (no output).');
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
    <div className="widget-card code-widget">
      <div className="widget-header">
        <div className="widget-title">
          <Code size={16} />
          <span>Interactive Python Console</span>
        </div>
        <button 
          onClick={handleRunCode} 
          className="widget-btn run-btn"
          disabled={isRunning}
        >
          {isRunning ? <RefreshCw size={14} className="loader-spinner" /> : <Play size={14} />}
          <span>Run Snippet</span>
        </button>
      </div>
      <textarea
        className="widget-textarea code-editor"
        value={code}
        onChange={(e) => setCode(e.target.value)}
        rows={6}
        spellCheck="false"
      />
      {output && (
        <div className={`widget-console ${success === false ? 'console-error' : 'console-success'}`}>
          <div className="console-header">Output:</div>
          <pre>{output}</pre>
        </div>
      )}
    </div>
  );
};

// ==========================================
// 2. Bedrock API Playground Widget
// ==========================================
const ApiPlaygroundWidget = ({ rawData }) => {
  let config = {};
  try {
    config = JSON.parse(rawData);
  } catch (e) {
    config = {};
  }

  const [modelId, setModelId] = useState(config.modelId || 'anthropic.claude-3-haiku-20240307-v1:0');
  const [prompt, setPrompt] = useState(config.prompt || 'Explain the concept of temperature in LLMs in one sentence.');
  const [temperature, setTemperature] = useState(config.temperature || 0.7);
  const [maxTokens, setMaxTokens] = useState(config.maxTokens || 300);
  const [output, setOutput] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [success, setSuccess] = useState(null);

  const handleRunInference = async () => {
    setIsRunning(true);
    setSuccess(null);
    try {
      const response = await fetch('/api/playground/invoke', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model_id: modelId, prompt, temperature, max_tokens: maxTokens })
      });
      const data = await response.json();
      if (data.success) {
        setSuccess(true);
        setOutput(data.output);
      } else {
        setSuccess(false);
        setOutput(`Error: ${data.error}`);
      }
    } catch (e) {
      setSuccess(false);
      setOutput(`Connection Error: ${e.message}`);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="widget-card api-widget">
      <div className="widget-header">
        <div className="widget-title">
          <Database size={16} />
          <span>Bedrock API Playground (Local AWS Client)</span>
        </div>
        <button 
          onClick={handleRunInference} 
          className="widget-btn run-btn"
          disabled={isRunning}
        >
          {isRunning ? <RefreshCw size={14} className="loader-spinner" /> : <Send size={14} />}
          <span>Send Payload</span>
        </button>
      </div>

      <div className="widget-body">
        <div className="widget-field">
          <label>Model ID:</label>
          <select 
            value={modelId} 
            onChange={(e) => setModelId(e.target.value)}
            className="widget-select"
          >
            <option value="anthropic.claude-3-haiku-20240307-v1:0">Claude 3 Haiku</option>
            <option value="anthropic.claude-3-sonnet-20240229-v1:0">Claude 3 Sonnet</option>
            <option value="meta.llama3-8b-instruct-v1:0">Llama 3 8B Instruct</option>
            <option value="amazon.titan-text-express-v1">Titan Text Express</option>
          </select>
        </div>

        <div className="widget-field">
          <label>Prompt:</label>
          <textarea
            className="widget-textarea prompt-editor"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows={2}
          />
        </div>

        <div className="widget-row">
          <div className="widget-field flex-1">
            <label>Temperature: {temperature}</label>
            <input 
              type="range" 
              min="0.0" 
              max="1.0" 
              step="0.1" 
              value={temperature}
              onChange={(e) => setTemperature(parseFloat(e.target.value))}
              className="widget-slider"
            />
          </div>
          <div className="widget-field flex-1">
            <label>Max Tokens: {maxTokens}</label>
            <input 
              type="range" 
              min="50" 
              max="1000" 
              step="50" 
              value={maxTokens}
              onChange={(e) => setMaxTokens(parseInt(e.target.value))}
              className="widget-slider"
            />
          </div>
        </div>
      </div>

      {output && (
        <div className={`widget-console ${success === false ? 'console-error' : 'console-success'}`}>
          <div className="console-header">Model Response:</div>
          <pre style={{ whiteSpace: 'pre-wrap' }}>{output}</pre>
        </div>
      )}
    </div>
  );
};

// ==========================================
// 3. Model Parameter Tester Widget
// ==========================================
const ModelParamTesterWidget = ({ rawData }) => {
  let initialConfig = {};
  try {
    initialConfig = JSON.parse(rawData);
  } catch (e) {
    initialConfig = {};
  }

  const [temp, setTemp] = useState(initialConfig.temperature || 0.7);
  const [topP, setTopP] = useState(initialConfig.topP || 0.9);
  const [model, setModel] = useState(initialConfig.modelId || 'anthropic.claude-3-sonnet');

  const simulatedPayload = useMemo(() => {
    return JSON.stringify({
      modelId: model,
      inferenceConfig: {
        temperature: temp,
        topP: topP,
        maxTokens: 500
      }
    }, null, 2);
  }, [temp, topP, model]);

  return (
    <div className="widget-card tester-widget">
      <div className="widget-header">
        <div className="widget-title">
          <Sliders size={16} />
          <span>Live Parameter Configurator</span>
        </div>
      </div>
      <div className="widget-row">
        <div className="widget-params flex-1">
          <div className="widget-field">
            <label>Model Profile:</label>
            <select 
              value={model} 
              onChange={(e) => setModel(e.target.value)}
              className="widget-select"
            >
              <option value="anthropic.claude-3-sonnet">Claude 3 Sonnet</option>
              <option value="meta.llama3-70b">Llama 3 70B</option>
              <option value="mistral.mixtral-8x7b">Mixtral 8x7B</option>
            </select>
          </div>

          <div className="widget-field">
            <label>Temperature: {temp}</label>
            <input 
              type="range" 
              min="0.0" 
              max="1.0" 
              step="0.05" 
              value={temp}
              onChange={(e) => setTemp(parseFloat(e.target.value))}
              className="widget-slider"
            />
          </div>

          <div className="widget-field">
            <label>Top P: {topP}</label>
            <input 
              type="range" 
              min="0.0" 
              max="1.0" 
              step="0.05" 
              value={topP}
              onChange={(e) => setTopP(parseFloat(e.target.value))}
              className="widget-slider"
            />
          </div>
        </div>

        <div className="widget-payload flex-1">
          <div className="payload-header">Simulated API Payload:</div>
          <pre className="payload-code">{simulatedPayload}</pre>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 4. Transcript Timeline Widget
// ==========================================
const TranscriptTimelineWidget = ({ rawData, selectedKb }) => {
  let config = {};
  try {
    config = JSON.parse(rawData);
  } catch (e) {
    config = {};
  }

  const { transcriptPath } = config;
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentSeconds, setCurrentSeconds] = useState(0);
  const [shouldAutoplay, setShouldAutoplay] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeIndex, setActiveIndex] = useState(0);
  const [userNotes, setUserNotes] = useState({});
  const [editingNoteSec, setEditingNoteSec] = useState(null);
  const [tempNoteText, setTempNoteText] = useState('');

  useEffect(() => {
    if (!selectedKb || !transcriptPath) return;

    setShouldAutoplay(false);

    const fetchTranscript = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`/api/kbs/${selectedKb}/document?path=${encodeURIComponent(transcriptPath)}`);
        if (!response.ok) throw new Error('Transcript file not found');
        const resJson = await response.json();
        const parsed = JSON.parse(resJson.content);
        setData(parsed);
        if (parsed.timeline && parsed.timeline.length > 0) {
          setCurrentSeconds(parsed.timeline[0].seconds || 0);
          
          const loadedNotes = {};
          parsed.timeline.forEach(item => {
            const saved = localStorage.getItem(`transcript-note-${transcriptPath}-${item.seconds}`);
            if (saved) {
              loadedNotes[item.seconds] = saved;
            }
          });
          setUserNotes(loadedNotes);
        }
      } catch (err) {
        console.error('Failed to load transcript:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTranscript();
  }, [transcriptPath, selectedKb]);

  const saveNote = (sec, text) => {
    if (text.trim() === '') {
      localStorage.removeItem(`transcript-note-${transcriptPath}-${sec}`);
      setUserNotes(prev => {
        const updated = { ...prev };
        delete updated[sec];
        return updated;
      });
    } else {
      localStorage.setItem(`transcript-note-${transcriptPath}-${sec}`, text);
      setUserNotes(prev => ({ ...prev, [sec]: text }));
    }
  };

  const videoId = data ? getYoutubeId(data.video_url) : null;

  const filteredTimeline = useMemo(() => {
    if (!data || !data.timeline) return [];
    if (!searchQuery.trim()) return data.timeline;
    const query = searchQuery.toLowerCase();
    return data.timeline.filter(
      item =>
        item.label.toLowerCase().includes(query) ||
        item.text.toLowerCase().includes(query)
    );
  }, [data, searchQuery]);

  if (loading) {
    return (
      <div className="widget-card flex items-center justify-center p-6" style={{ minHeight: '100px', gap: '12px' }}>
        <RefreshCw size={18} className="loader-spinner" />
        <span style={{ color: 'var(--text-secondary)' }}>Loading transcript timeline...</span>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="widget-card" style={{ borderLeft: '3px solid var(--danger)' }}>
        <div className="console-error" style={{ padding: '12px' }}>
          Failed to load transcript timeline: <strong>{error || 'No data'}</strong>
        </div>
      </div>
    );
  }

  return (
    <div className="widget-card transcript-widget">
      <div className="widget-header">
        <div className="widget-title">
          <Play size={16} />
          <span>{data.title} ({data.duration})</span>
        </div>
      </div>

      <div className="widget-body" style={{ flexDirection: 'column', gap: '16px' }}>
        {videoId && (
          <div className="video-player-container" style={{ borderRadius: '8px', overflow: 'hidden', border: '1px solid var(--border-color)', boxShadow: '0 4px 12px rgba(0,0,0,0.15)' }}>
            <iframe
              width="100%"
              height="360"
              src={`https://www.youtube.com/embed/${videoId}?start=${currentSeconds}${shouldAutoplay ? '&autoplay=1' : ''}`}
              title={data.title}
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              allowFullScreen
              style={{ display: 'block' }}
            ></iframe>
          </div>
        )}

        <div className="transcript-search-box" style={{ position: 'relative' }}>
          <input
            type="text"
            placeholder="Search transcript topics or content..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="widget-textarea"
            style={{ height: '36px', padding: '8px 12px', fontSize: '0.9rem', borderRadius: '6px' }}
          />
        </div>

        <div className="timeline-list" style={{ maxHeight: '350px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '8px', paddingRight: '4px' }}>
          {filteredTimeline.length === 0 ? (
            <div style={{ padding: '16px', textAlign: 'center', color: 'var(--text-secondary)' }}>
              No matches found for "{searchQuery}"
            </div>
          ) : (
            filteredTimeline.map((item, idx) => {
              const isActive = item.seconds === currentSeconds;
              return (
                <div
                  key={idx}
                  onClick={() => {
                    setCurrentSeconds(item.seconds);
                    setActiveIndex(idx);
                    setShouldAutoplay(true);
                  }}
                  className={`timeline-item ${isActive ? 'active' : ''}`}
                  style={{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '4px',
                    padding: '10px 14px',
                    borderRadius: '6px',
                    background: isActive ? 'var(--hover-bg)' : 'rgba(255, 255, 255, 0.02)',
                    borderLeft: isActive ? '3px solid var(--accent-color)' : '3px solid transparent',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontWeight: '600', color: isActive ? 'var(--accent-color)' : 'var(--text-primary)', fontSize: '0.95rem' }}>
                      {item.label}
                    </span>
                    <span 
                      className="badge" 
                      style={{ 
                        fontSize: '0.8rem', 
                        padding: '2px 8px', 
                        borderRadius: '10px', 
                        background: isActive ? 'var(--accent-color)' : 'var(--border-color)', 
                        color: isActive ? '#fff' : 'var(--text-secondary)',
                        fontWeight: '600'
                      }}
                    >
                      {item.timestamp}
                    </span>
                  </div>
                  <p style={{ margin: '0', fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: '1.4' }}>
                     {item.text}
                  </p>

                  {userNotes[item.seconds] && (
                    <div 
                      onClick={(e) => e.stopPropagation()} 
                      style={{ 
                        marginTop: '8px', 
                        padding: '8px 10px', 
                        borderRadius: '6px', 
                        background: 'rgba(99, 102, 241, 0.08)', 
                        borderLeft: '3px solid var(--accent-color)', 
                        fontSize: '0.85rem' 
                      }}
                    >
                      <strong style={{ color: 'var(--accent-color)', display: 'block', fontSize: '0.75rem', marginBottom: '2px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>My Understanding</strong>
                      <span style={{ color: 'var(--text-primary)', whiteSpace: 'pre-wrap' }}>{userNotes[item.seconds]}</span>
                    </div>
                  )}

                  {editingNoteSec === item.seconds ? (
                    <div 
                      onClick={(e) => e.stopPropagation()} 
                      style={{ 
                        marginTop: '8px', 
                        display: 'flex', 
                        flexDirection: 'column', 
                        gap: '6px' 
                      }}
                    >
                      <textarea
                        value={tempNoteText}
                        onChange={(e) => setTempNoteText(e.target.value)}
                        placeholder="Type your notes or key takeaways here..."
                        className="widget-textarea"
                        style={{ 
                          height: '60px', 
                          padding: '6px 8px', 
                          fontSize: '0.8rem', 
                          borderRadius: '4px',
                          border: '1px solid var(--accent-color)',
                          background: 'rgba(0,0,0,0.2)',
                          color: 'var(--text-primary)',
                          outline: 'none',
                          resize: 'vertical'
                        }}
                      />
                      <div style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
                        <button 
                          onClick={() => setEditingNoteSec(null)}
                          style={{ 
                            background: 'rgba(255,255,255,0.05)', 
                            border: '1px solid var(--border-color)', 
                            color: 'var(--text-secondary)', 
                            padding: '3px 8px', 
                            borderRadius: '4px', 
                            fontSize: '0.75rem', 
                            cursor: 'pointer' 
                          }}
                        >
                          Cancel
                        </button>
                        <button 
                          onClick={() => {
                            saveNote(item.seconds, tempNoteText);
                            setEditingNoteSec(null);
                          }}
                          style={{ 
                            background: 'var(--accent-color)', 
                            border: 'none', 
                            color: '#fff', 
                            padding: '3px 8px', 
                            borderRadius: '4px', 
                            fontSize: '0.75rem', 
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '4px'
                          }}
                        >
                          <Check size={12} />
                          Save
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '6px' }}>
                      <button 
                        onClick={(e) => {
                          e.stopPropagation();
                          setEditingNoteSec(item.seconds);
                          setTempNoteText(userNotes[item.seconds] || '');
                        }}
                        style={{
                          background: 'none',
                          border: 'none',
                          color: 'var(--accent-color)',
                          fontSize: '0.75rem',
                          cursor: 'pointer',
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '4px',
                          opacity: 0.8,
                          padding: '2px 4px',
                          borderRadius: '4px',
                          transition: 'opacity 0.2s'
                        }}
                        onMouseEnter={(e) => e.target.style.opacity = 1}
                        onMouseLeave={(e) => e.target.style.opacity = 0.8}
                      >
                        <Edit3 size={12} />
                        {userNotes[item.seconds] ? 'Edit Understanding' : 'Add Understanding'}
                      </button>
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 5. Interactive Widget Router
// ==========================================
const InteractiveWidget = ({ type, rawData, selectedKb }) => {
  switch (type) {
    case 'code-playground':
      return <CodePlaygroundWidget initialCode={rawData} />;
    case 'api-playground':
      return <ApiPlaygroundWidget rawData={rawData} />;
    case 'model-param-tester':
      return <ModelParamTesterWidget rawData={rawData} />;
    case 'transcript-timeline':
      return <TranscriptTimelineWidget rawData={rawData} selectedKb={selectedKb} />;
    default:
      return (
        <div className="widget-card" style={{ borderLeft: '3px solid var(--danger)' }}>
          <div className="console-error" style={{ padding: '12px' }}>
            Unsupported widget type: <strong>{type}</strong>
          </div>
        </div>
      );
  }
};

// ==========================================
// 5.5 Mermaid Diagram Renderer
// ==========================================
const MermaidDiagram = ({ code }) => {
  const [svg, setSvg] = useState('');
  const [error, setError] = useState(null);
  const elementId = useRef(`mermaid-${Math.floor(Math.random() * 1000000)}`);

  useEffect(() => {
    let active = true;
    const renderChart = async () => {
      try {
        setError(null);
        mermaid.initialize({
          startOnLoad: false,
          theme: 'dark',
          securityLevel: 'loose',
          themeVariables: {
            background: '#1e1e2e',
            primaryColor: '#bb9af7',
            primaryTextColor: '#c0caf5',
            lineColor: '#565f89'
          }
        });
        await mermaid.parse(code);
        const { svg: renderedSvg } = await mermaid.render(elementId.current, code);
        if (active) {
          setSvg(renderedSvg);
        }
      } catch (err) {
        console.error("Mermaid parse error:", err);
        if (active) {
          setError(err.message || 'Failed to parse Mermaid diagram.');
        }
      }
    };

    renderChart();
    return () => {
      active = false;
    };
  }, [code]);

  if (error) {
    return (
      <div className="widget-card" style={{ borderLeft: '3px solid var(--danger)', margin: '16px 0' }}>
        <div className="console-error" style={{ padding: '12px', fontSize: '0.85rem' }}>
          <strong>Mermaid Diagram Error:</strong>
          <pre style={{ marginTop: '8px', whiteSpace: 'pre-wrap', fontFamily: 'monospace', fontSize: '0.8rem' }}>{error}</pre>
        </div>
      </div>
    );
  }

  if (!svg) {
    return (
      <div className="widget-card" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '24px', margin: '16px 0' }}>
        <div className="loader-spinner" style={{ width: '20px', height: '20px' }}></div>
      </div>
    );
  }

  return (
    <div 
      className="mermaid-diagram-container"
      style={{
        background: 'rgba(30, 30, 46, 0.4)',
        border: '1px solid var(--border-color)',
        borderRadius: '8px',
        padding: '16px',
        margin: '16px 0',
        display: 'flex',
        justifyContent: 'center',
        overflowX: 'auto'
      }}
      dangerouslySetInnerHTML={{ __html: svg }} 
    />
  );
};

// Helper to resolve relative image paths
const resolveHtmlImages = (html, activeDoc, selectedKb) => {
  if (!html) return html;
  return html.replace(/<img\s+([^>]*?)src="([^"]+)"([^>]*?)>/gi, (match, prefix, src, suffix) => {
    if (src.startsWith('http://') || src.startsWith('https://') || src.startsWith('data:') || src.startsWith('/')) {
      return match;
    }
    let resolvedPath = src;
    if (activeDoc && activeDoc.includes('/')) {
      const activeDir = activeDoc.substring(0, activeDoc.lastIndexOf('/'));
      resolvedPath = `${activeDir}/${src}`;
    }
    const parts = resolvedPath.split('/');
    const stack = [];
    for (const part of parts) {
      if (part === '.' || part === '') continue;
      if (part === '..') {
        stack.pop();
      } else {
        stack.push(part);
      }
    }
    const finalPath = stack.join('/');
    const newSrc = `/api/kbs/${selectedKb}/document?path=${encodeURIComponent(finalPath)}`;
    return `<img ${prefix}src="${newSrc}"${suffix}>`;
  });
};

// ==========================================
// 6. Course Header Component
// ==========================================
const CourseHeader = ({ 
  title, 
  readingTime, 
  difficulty, 
  isCompleted, 
  isBookmarked, 
  toggleCompleted, 
  toggleBookmarked,
  progressPercentage
}) => {
  return (
    <div className="course-header-card">
      <div className="header-meta-top">
        <span className={`header-badge-difficulty diff-${difficulty.toLowerCase()}`}>
          {difficulty}
        </span>
        <span className="header-meta-item">⏱ {readingTime} min read</span>
        <span className="header-meta-item">🎯 Course Completed: {progressPercentage}%</span>
      </div>

      <div className="header-main-row">
        <h1 className="header-title">{title}</h1>
        <div className="header-actions">
          <button 
            className={`header-action-btn btn-bookmark ${isBookmarked ? 'active' : ''}`}
            onClick={toggleBookmarked}
            title={isBookmarked ? "Remove Bookmark" : "Bookmark Page"}
          >
            <Star size={14} className={isBookmarked ? "star-filled" : ""} />
            <span>{isBookmarked ? "Bookmarked" : "Bookmark"}</span>
          </button>
          <button 
            className={`header-action-btn btn-complete ${isCompleted ? 'active' : ''}`}
            onClick={toggleCompleted}
            title={isCompleted ? "Mark Incomplete" : "Mark Completed"}
          >
            <Check size={14} />
            <span>{isCompleted ? "Completed" : "Mark Done"}</span>
          </button>
        </div>
      </div>

      <div className="header-objectives-box">
        <div className="objectives-title">
          <Compass size={14} />
          <span>Interactive Learning Path</span>
        </div>
        <div className="objectives-content-grid">
          <div>
            <strong>Prerequisites:</strong> Basic logic syntax and programming variables.
          </div>
          <div>
            <strong>Skills You'll Master:</strong> Runtime visualizations, interactive quiz validations, sandboxed playground tests.
          </div>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 7. Main DocReader Coordinator
// ==========================================
const DocReader = ({ 
  activeDoc, 
  docContent, 
  isLoading, 
  onSelectDoc, 
  selectedKb, 
  theme,
  completedDocs,
  bookmarkedDocs,
  recentlyViewedDocs,
  toggleDocCompleted,
  toggleDocBookmarked,
  navItems
}) => {
  const [headings, setHeadings] = useState([]);
  const [activeHeading, setActiveHeading] = useState('');
  const [searchText, setSearchText] = useState('');

  // Extract outline / headings from document
  useEffect(() => {
    if (!docContent) {
      setHeadings([]);
      return;
    }
    const lines = docContent.split('\n');
    const gathered = [];
    lines.forEach(line => {
      const match = line.match(/^(#{2,3})\s+(.*)$/);
      if (match) {
        const level = match[1].length;
        const text = match[2].trim().replace(/\*\*|[#*`]/g, '');
        const id = text.toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]/g, '');
        gathered.push({ level, text, id });
      }
    });
    setHeadings(gathered);
  }, [docContent]);

  // Track active heading on scroll
  useEffect(() => {
    const handleScroll = () => {
      const headingElements = headings.map(h => document.getElementById(h.id)).filter(Boolean);
      let currentActive = '';
      for (const el of headingElements) {
        const rect = el.getBoundingClientRect();
        if (rect.top <= 160) {
          currentActive = el.id;
        } else {
          break;
        }
      }
      if (currentActive) {
        setActiveHeading(currentActive);
      } else if (headings.length > 0) {
        setActiveHeading(headings[0].id);
      }
    };

    const container = document.querySelector('.doc-panel');
    if (container) {
      container.addEventListener('scroll', handleScroll);
      handleScroll();
    }
    return () => {
      if (container) {
        container.removeEventListener('scroll', handleScroll);
      }
    };
  }, [headings]);

  // Scroll to anchor if present in URL
  useEffect(() => {
    if (!isLoading && activeDoc) {
      const hash = window.location.hash;
      if (hash) {
        const id = hash.replace('#', '');
        setTimeout(() => {
          const el = document.getElementById(id);
          if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }, 300);
      }
    }
  }, [isLoading, activeDoc]);

  // Segment-based parser that splits markdown text and inserts live React widgets / Mermaid diagrams
  const renderSegments = useMemo(() => {
    if (!docContent) return null;

    const segments = [];
    let lastIndex = 0;
    let match;
    const blockRegex = /```(?:widget:([a-zA-Z0-9_-]+)|(mermaid))\n([\s\S]*?)\n```/g;

    while ((match = blockRegex.exec(docContent)) !== null) {
      const textBefore = docContent.substring(lastIndex, match.index);
      if (textBefore.trim()) {
        segments.push({ type: 'markdown', content: textBefore });
      }
      
      if (match[2] === 'mermaid') {
        segments.push({
          type: 'mermaid',
          content: match[3]
        });
      } else {
        segments.push({
          type: 'widget',
          widgetType: match[1],
          content: match[3]
        });
      }
      
      lastIndex = blockRegex.lastIndex;
    }
    
    const textAfter = docContent.substring(lastIndex);
    if (textAfter.trim() || segments.length === 0) {
      segments.push({ type: 'markdown', content: textAfter });
    }

    return segments;
  }, [docContent]);

  // Page Search In-Page handlers
  const handlePageSearchNext = () => {
    if (!searchText) return;
    const found = window.find(searchText, false, false, true);
    if (!found) window.find(searchText, false, false, true);
  };

  const handlePageSearchPrev = () => {
    if (!searchText) return;
    const found = window.find(searchText, false, true, true);
    if (!found) window.find(searchText, false, true, true);
  };

  // Calculate stats for CourseHeader
  const pageTitle = useMemo(() => {
    if (!docContent) return 'Documentation';
    const firstLine = docContent.split('\n')[0] || '';
    if (firstLine.startsWith('# ')) {
      return firstLine.replace('# ', '').trim();
    }
    return 'Documentation';
  }, [docContent]);

  const readingTime = useMemo(() => {
    if (!docContent) return 1;
    const wordCount = docContent.split(/\s+/).length;
    return Math.max(1, Math.round(wordCount / 200));
  }, [docContent]);

  const difficulty = useMemo(() => {
    if (!activeDoc) return 'Beginner';
    const path = activeDoc.toLowerCase();
    const contentSize = docContent ? docContent.length : 0;
    if (path.includes('advanced') || path.includes('async') || path.includes('decorator') || contentSize > 15000) {
      return 'Advanced';
    }
    if (contentSize > 7000) {
      return 'Intermediate';
    }
    return 'Beginner';
  }, [activeDoc, docContent]);

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

  const overallProgressPercentage = useMemo(() => {
    const allLeafNodes = navItems ? navItems.reduce((acc, item) => [...acc, ...getLeafNodes(item)], []) : [];
    const totalCompleted = allLeafNodes.filter(l => completedDocs[l.href]).length;
    return allLeafNodes.length > 0 ? Math.round((totalCompleted / allLeafNodes.length) * 100) : 0;
  }, [navItems, completedDocs]);

  // Intercept relative link clicks
  const handleContentClick = (e) => {
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
          if (part === '..') {
            stack.pop();
          } else {
            stack.push(part);
          }
        }
        onSelectDoc(stack.join('/'));
      }
    }
  };

  if (isLoading) {
    return (
      <div className="doc-panel" style={{ alignItems: 'center', justifyContent: 'center' }}>
        <div className="loader-spinner" style={{ width: '32px', height: '32px' }}></div>
        <p style={{ marginTop: '16px', color: 'var(--text-secondary)' }}>Loading document...</p>
      </div>
    );
  }

  if (!activeDoc) {
    return (
      <div className="doc-panel">
        <div className="doc-welcome">
          <div className="welcome-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="80" height="80" fill="none" style={{ margin: '0 auto' }}>
              <defs>
                <linearGradient id="welcomeDiagGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#ff79c6" />
                  <stop offset="50%" stopColor="#bd93f9" />
                  <stop offset="100%" stopColor="#00f2fe" />
                </linearGradient>
                <radialGradient id="welcomePinkRadial" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stopColor="#ff79c6" stopOpacity="0.5" />
                  <stop offset="60%" stopColor="#bd93f9" stopOpacity="0.2" />
                  <stop offset="100%" stopColor="#bd93f9" stopOpacity="0" />
                </radialGradient>
                <radialGradient id="welcomeTealRadial" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stopColor="#00f2fe" stopOpacity="0.4" />
                  <stop offset="60%" stopColor="#50fa7b" stopOpacity="0.15" />
                  <stop offset="100%" stopColor="#50fa7b" stopOpacity="0" />
                </radialGradient>
              </defs>
              <circle className="aura-wave-1" cx="12" cy="12" r="9.5" fill="url(#welcomePinkRadial)" />
              <circle className="aura-wave-2" cx="12" cy="12" r="8.5" fill="url(#welcomeTealRadial)" />
              <path d="M5.5 6.5h6l3.5 3.5v9.5a1 1 0 0 1-1 1h-8.5a1 1 0 0 1-1-1v-13a1 1 0 0 1 1-1z" stroke="url(#welcomeDiagGrad)" strokeWidth="1.5" strokeLinejoin="round" opacity="0.45" />
              <path d="M8.5 3.5H14l3.5 3.5V17.5a1 1 0 0 1-1 1h-8a1 1 0 0 1-1-1V4.5a1 1 0 0 1 1-1z" stroke="url(#welcomeDiagGrad)" strokeWidth="1.8" strokeLinejoin="round" />
              <path d="M14 3.5V7h3.5" stroke="url(#welcomeDiagGrad)" strokeWidth="1.8" strokeLinejoin="round" />
              <path d="M11 9.5h3.5M11 12h3.5M11 14.5h2" stroke="url(#welcomeDiagGrad)" strokeWidth="1.5" strokeLinecap="round" />
            </svg>
          </div>
          <h1 className="welcome-title">AuraDocs</h1>
          <p className="welcome-desc">
            Select a document from the left navigation tree to begin reading, 
            or toggle the AI Assistant on the right to perform semantic questions across the guide.
          </p>
        </div>
      </div>
    );
  }

  const renderMdxNode = (node, key) => {
    if (node.type === 'text') {
      if (!node.content.trim()) return null;
      const html = resolveHtmlImages(parseMarkdown(node.content), activeDoc, selectedKb);
      return (
        <div
          key={key}
          dangerouslySetInnerHTML={{ __html: html }}
          style={{ display: 'contents' }}
        />
      );
    }

    const Comp = componentMap[node.type];
    if (!Comp) {
      return null;
    }

    const renderedChildren = node.children && node.children.length > 0
      ? node.children.map((child, cIdx) => renderMdxNode(child, `${key}-${cIdx}`))
      : null;

    return (
      <Comp key={key} {...node.props}>
        {renderedChildren}
      </Comp>
    );
  };

  return (
    <div className="doc-panel-wrapper">
      {/* Top Search-Within-Page Utility */}
      <div className="page-search-container">
        <div className="search-input-wrapper">
          <Search size={14} className="search-icon" />
          <input 
            type="text" 
            placeholder="Search within this page..." 
            value={searchText}
            onChange={(e) => {
              setSearchText(e.target.value);
            }}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
                handlePageSearchNext();
              }
            }}
          />
        </div>
        {searchText && (
          <div className="search-actions">
            <button onClick={handlePageSearchPrev} className="search-btn">Prev</button>
            <button onClick={handlePageSearchNext} className="search-btn">Next</button>
            <button onClick={() => setSearchText('')} className="search-btn clear-btn">Clear</button>
          </div>
        )}
      </div>

      <div className="doc-content-layout">
        {/* Document Column */}
        <div className="doc-panel" onClick={handleContentClick}>
          <article className="doc-content">
            {/* Auto-injected Course Header */}
            <CourseHeader 
              title={pageTitle}
              readingTime={readingTime}
              difficulty={difficulty}
              isCompleted={!!completedDocs[activeDoc]}
              isBookmarked={!!bookmarkedDocs[activeDoc]}
              toggleCompleted={() => toggleDocCompleted(activeDoc)}
              toggleBookmarked={() => toggleDocBookmarked(activeDoc)}
              progressPercentage={overallProgressPercentage}
            />

            {renderSegments && renderSegments.map((segment, idx) => {
              if (segment.type === 'markdown') {
                const nodes = parseMDXContent(segment.content);
                return (
                  <div key={idx} style={{ display: 'contents' }}>
                    {nodes.map((node, nIdx) => renderMdxNode(node, `${idx}-${nIdx}`))}
                  </div>
                );
              } else if (segment.type === 'mermaid') {
                return (
                  <MermaidDiagram 
                    key={idx} 
                    code={segment.content} 
                  />
                );
              } else {
                return (
                  <InteractiveWidget 
                    key={idx} 
                    type={segment.widgetType} 
                    rawData={segment.content} 
                    selectedKb={selectedKb}
                  />
                );
              }
            })}
          </article>
        </div>

        {/* Sticky Table of Contents Column */}
        {headings.length > 0 && (
          <aside className="doc-toc-panel">
            <div className="toc-title">On this page</div>
            <nav className="toc-list">
              {headings.map((h, i) => (
                <a 
                  key={i} 
                  href={`#${h.id}`}
                  onClick={(e) => {
                    e.preventDefault();
                    const el = document.getElementById(h.id);
                    if (el) {
                      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                  }}
                  className={`toc-item depth-${h.level} ${activeHeading === h.id ? 'active' : ''}`}
                >
                  <ChevronRight size={10} className="toc-arrow" />
                  <span>{h.text}</span>
                </a>
              ))}
            </nav>
          </aside>
        )}
      </div>
    </div>
  );
};

export default DocReader;
