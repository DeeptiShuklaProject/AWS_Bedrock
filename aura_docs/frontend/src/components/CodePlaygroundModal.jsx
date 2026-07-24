import React, { useState, useEffect } from 'react';
import { 
  Terminal, 
  Play, 
  RefreshCw, 
  X, 
  Copy, 
  Check, 
  Sparkles, 
  Code2, 
  Layers,
  Trash2
} from 'lucide-react';

const PRESET_TEMPLATES = [
  {
    name: "Amazon Bedrock API Call (Boto3)",
    code: `import boto3
import json

# Initialize AWS Bedrock Runtime client
bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

prompt_data = "Explain AWS Lambda cold starts in 3 bullet points."
print(f"Prompt: {prompt_data}\\n")
print("Executing Bedrock model call...")
# Simulated Bedrock Output for Playground demo
print("Response: 1. Initialization overhead 2. Container spinup delay 3. Mitigated by Provisioned Concurrency")
`
  },
  {
    name: "AWS S3 Bucket & IAM Policy",
    code: `import json

bucket_name = "aura-docs-production-analytics-data"
iam_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": ["s3:GetObject", "s3:ListBucket"],
        "Resource": [f"arn:aws:s3:::{bucket_name}", f"arn:aws:s3:::{bucket_name}/*"]
    }]
}

print(f"Bucket ARN: arn:aws:s3:::{bucket_name}")
print("Generated IAM Policy Document:")
print(json.dumps(iam_policy, indent=2))
`
  },
  {
    name: "AWS EC2 Instance Health Calculator",
    code: `instances = [
    {"id": "i-0a1b2c3d4e", "state": "running", "type": "t3.xlarge", "az": "us-east-1a"},
    {"id": "i-0f9e8d7c6b", "state": "stopped", "type": "m5.large", "az": "us-east-1b"},
    {"id": "i-1122334455", "state": "running", "type": "c5.2xlarge", "az": "us-east-1a"}
]

running_count = sum(1 for i in instances if i['state'] == 'running')
print(f"Total Provisioned EC2 Instances: {len(instances)}")
print(f"Active Running Instances: {running_count}")
for inst in instances:
    print(f" -> Instance {inst['id']} [{inst['type']}] - Status: {inst['state'].upper()}")
`
  }
];

const CodePlaygroundModal = ({ isOpen, onClose, initialCode = '' }) => {
  const [code, setCode] = useState(initialCode || PRESET_TEMPLATES[0].code);
  const [output, setOutput] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [isSuccess, setIsSuccess] = useState(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (initialCode) {
      setCode(initialCode);
    }
  }, [initialCode]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!isOpen) return;
      if (e.key === 'Escape') onClose();
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        handleRunCode();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, code]);

  const handleRunCode = async () => {
    if (!code.trim()) return;
    setIsRunning(true);
    setIsSuccess(null);
    setOutput("Executing script in Python runtime sandbox...");

    try {
      const response = await fetch('/api/playground/run-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
      });
      const data = await response.json();
      
      if (data.success) {
        setIsSuccess(true);
        const result = (data.stdout || '') + (data.stderr || '');
        setOutput(result || 'Execution completed with 0 errors (no output printed).');
      } else {
        setIsSuccess(false);
        setOutput((data.stdout || '') + '\n' + (data.stderr || 'Execution failed.'));
      }
    } catch (e) {
      setIsSuccess(false);
      setOutput(`Error connecting to Python execution server: ${e.message}`);
    } finally {
      setIsRunning(false);
    }
  };

  const handleCopyCode = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div 
        style={{
          width: '95%',
          maxWidth: '1150px',
          height: '85vh',
          background: '#0b0f19',
          border: '1px solid var(--border-color)',
          borderRadius: '24px',
          boxShadow: 'var(--shadow-lg)',
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden'
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Top Playground Header Bar */}
        <div style={{ padding: '16px 24px', background: 'var(--bg-surface)', borderBottom: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ width: '40px', height: '40px', borderRadius: '12px', background: 'var(--primary-gradient)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff' }}>
              <Terminal size={20} />
            </div>
            <div>
              <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.2rem', fontWeight: 800, color: 'var(--text-primary)', margin: 0, display: 'flex', alignItems: 'center', gap: '10px' }}>
                Interactive Code Playground
                <span className="brand-badge" style={{ background: 'rgba(56,189,248,0.2)', color: 'var(--accent-cyan)', border: '1px solid rgba(56,189,248,0.4)' }}>
                  TRY IT YOURSELF
                </span>
              </h3>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', margin: 0 }}>
                Write, test, and execute Python & AWS SDK code snippets live
              </p>
            </div>
          </div>

          {/* Action Toolbar */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <button 
              onClick={handleRunCode} 
              disabled={isRunning}
              className="quiz-launch-btn"
              style={{ padding: '10px 24px', fontSize: '0.92rem' }}
            >
              {isRunning ? <RefreshCw size={16} className="animate-spin" /> : <Play size={16} />}
              <span>Run Code</span>
              <kbd style={{ fontSize: '0.68rem', background: 'rgba(0,0,0,0.3)', padding: '2px 6px', borderRadius: '4px', fontFamily: 'var(--font-mono)' }}>ctrl ↵</kbd>
            </button>

            <button 
              onClick={onClose}
              style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', padding: '6px' }}
            >
              <X size={22} />
            </button>
          </div>
        </div>

        {/* Template Selector Bar */}
        <div style={{ padding: '10px 24px', background: '#0d1527', borderBottom: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '16px', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Layers size={15} style={{ color: 'var(--accent-indigo)' }} />
            <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-secondary)' }}>Code Templates:</span>
            {PRESET_TEMPLATES.map((tmpl, idx) => (
              <button
                key={idx}
                onClick={() => {
                  setCode(tmpl.code);
                  setOutput('');
                  setIsSuccess(null);
                }}
                style={{
                  padding: '5px 12px',
                  borderRadius: '8px',
                  background: 'var(--bg-card)',
                  border: '1px solid var(--border-color)',
                  color: 'var(--text-primary)',
                  fontSize: '0.8rem',
                  fontWeight: 600,
                  cursor: 'pointer'
                }}
              >
                {tmpl.name}
              </button>
            ))}
          </div>

          <div style={{ display: 'flex', gap: '8px' }}>
            <button
              onClick={handleCopyCode}
              style={{ padding: '5px 10px', borderRadius: '8px', background: 'transparent', border: '1px solid var(--border-color)', color: 'var(--text-secondary)', fontSize: '0.8rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}
            >
              {copied ? <Check size={14} style={{ color: 'var(--accent-emerald)' }} /> : <Copy size={14} />}
              <span>{copied ? 'Copied!' : 'Copy'}</span>
            </button>
            <button
              onClick={() => {
                setCode('');
                setOutput('');
                setIsSuccess(null);
              }}
              style={{ padding: '5px 10px', borderRadius: '8px', background: 'transparent', border: '1px solid var(--border-color)', color: 'var(--accent-rose)', fontSize: '0.8rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}
            >
              <Trash2 size={14} />
              <span>Clear</span>
            </button>
          </div>
        </div>

        {/* Dual Editor & Terminal Output Workspace */}
        <div style={{ flex: 1, display: 'grid', gridTemplateColumns: '1fr 1fr', overflow: 'hidden' }}>
          {/* Left Code Editor Pane */}
          <div style={{ display: 'flex', flexDirection: 'column', borderRight: '1px solid var(--border-color)', background: '#070a12' }}>
            <div style={{ padding: '8px 16px', background: 'var(--bg-app)', borderBottom: '1px solid var(--border-color)', fontSize: '0.78rem', fontWeight: 800, color: 'var(--text-muted)', textTransform: 'uppercase', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Code2 size={14} style={{ color: 'var(--accent-indigo)' }} />
              <span>Python Code Editor</span>
            </div>
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="# Write or paste Python / AWS Boto3 code here..."
              style={{
                flex: 1,
                width: '100%',
                padding: '20px',
                background: 'transparent',
                fontFamily: 'var(--font-mono)',
                fontSize: '0.98rem',
                color: '#34d399',
                border: 'none',
                outline: 'none',
                resize: 'none',
                lineHeight: 1.6
              }}
              spellCheck="false"
            />
          </div>

          {/* Right Terminal Console Output Pane */}
          <div style={{ display: 'flex', flexDirection: 'column', background: '#05070e' }}>
            <div style={{ padding: '8px 16px', background: 'var(--bg-app)', borderBottom: '1px solid var(--border-color)', fontSize: '0.78rem', fontWeight: 800, color: 'var(--text-muted)', textTransform: 'uppercase', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Terminal size={14} style={{ color: 'var(--accent-cyan)' }} />
                <span>Console Execution Output</span>
              </div>
              {isSuccess !== null && (
                <span style={{
                  fontSize: '0.7rem',
                  fontWeight: 800,
                  padding: '2px 8px',
                  borderRadius: '10px',
                  background: isSuccess ? 'rgba(16,185,129,0.2)' : 'rgba(244,63,94,0.2)',
                  color: isSuccess ? '#6ee7b7' : '#fda4af'
                }}>
                  {isSuccess ? 'STATUS: 200 OK' : 'STATUS: EXECUTION ERROR'}
                </span>
              )}
            </div>

            <div style={{ flex: 1, padding: '20px', overflowY: 'auto', fontFamily: 'var(--font-mono)', fontSize: '0.92rem', color: isSuccess === false ? '#fda4af' : '#e2e8f0', lineHeight: 1.6 }}>
              {output ? (
                <pre style={{ whiteSpace: 'pre-wrap', margin: 0 }}>{output}</pre>
              ) : (
                <div style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)', textAlign: 'center' }}>
                  <Sparkles size={32} style={{ color: 'var(--accent-indigo)', marginBottom: '12px' }} />
                  <p style={{ fontWeight: 600, fontSize: '0.95rem' }}>Ready to Execute Code</p>
                  <p style={{ fontSize: '0.82rem', marginTop: '4px' }}>Click "Run Code" or press <kbd style={{ padding: '2px 6px', borderRadius: '4px', background: 'var(--bg-card)' }}>ctrl + enter</kbd> to run</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CodePlaygroundModal;
