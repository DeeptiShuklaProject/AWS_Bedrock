import React, { useState } from 'react';
import { 
  Cpu, 
  Database, 
  Key, 
  Layers, 
  Radio, 
  Terminal, 
  Globe, 
  Box, 
  Cloud, 
  Play, 
  RotateCcw, 
  CheckCircle, 
  ArrowRight, 
  Activity, 
  ShieldAlert 
} from 'lucide-react';

export const ArchitectureDiagram = ({ title = "Amazon Bedrock AgentCore Runtime Architecture" }) => {
  const [activeStep, setActiveStep] = useState(0);
  const [isSimulating, setIsSimulating] = useState(false);

  const steps = [
    {
      id: "client",
      name: "Client Application",
      service: "User App / SDK",
      icon: <Globe size={20} className="text-blue-400" />,
      desc: "Sends prompt request & execution metadata to Amazon Bedrock AgentCore endpoint.",
      payload: "{ \"prompt\": \"Analyze S3 logs and run diagnostic code\", \"sessionId\": \"sess-8821\" }"
    },
    {
      id: "gateway",
      name: "AgentCore Gateway",
      service: "AWS IAM & Gateway",
      icon: <Key size={20} className="text-amber-400" />,
      desc: "Authenticates request using IAMSigV4, inspects tenant isolation policies, and routes traffic.",
      payload: "Authorization: AWS4-HMAC-SHA256 Credential=AKIA... Target=BedrockAgentRuntime"
    },
    {
      id: "runtime",
      name: "AgentCore Runtime",
      service: "MicroVM Container",
      icon: <Cpu size={20} className="text-purple-400" />,
      desc: "Isolated MicroVM container executes autonomous LLM planning loop and tools orchestrator.",
      payload: "State: Execution Active | Model: Claude 3.5 Sonnet | Planning: ReAct Loop"
    },
    {
      id: "tools",
      name: "Tool Sandbox & Code",
      service: "Code Interpreter / Lambda",
      icon: <Terminal size={20} className="text-emerald-400" />,
      desc: "Secure sandbox runs Python code snippets and invokes external API tools dynamically.",
      payload: "Executing: python sandbox_exec.py | Result: [Log output 200 OK]"
    },
    {
      id: "memory",
      name: "Agent Memory Engine",
      service: "DynamoDB / Vector Store",
      icon: <Database size={20} className="text-cyan-400" />,
      desc: "Persists conversation history, session state, and semantic vector embeddings across turns.",
      payload: "Session Saved: 4 Turns | Vector Search Score: 0.94 Similarity"
    }
  ];

  const handleSimulate = () => {
    setIsSimulating(true);
    let step = 0;
    setActiveStep(0);
    const interval = setInterval(() => {
      step++;
      if (step < steps.length) {
        setActiveStep(step);
      } else {
        clearInterval(interval);
        setIsSimulating(false);
      }
    }, 1400);
  };

  return (
    <div className="architecture-visualizer-card">
      <div className="arch-header">
        <div className="arch-title-group">
          <Activity size={18} className="arch-header-icon" />
          <div>
            <h3 className="arch-title">{title}</h3>
            <span className="arch-subtitle">Interactive Step-by-Step Architecture & Data Flow Visualizer</span>
          </div>
        </div>
        <button 
          onClick={handleSimulate}
          disabled={isSimulating}
          className="arch-simulate-btn"
        >
          {isSimulating ? <RotateCcw size={14} className="loader-spinner" /> : <Play size={14} />}
          <span>{isSimulating ? 'Simulating Traffic...' : 'Simulate Workflow'}</span>
        </button>
      </div>

      {/* Nodes Flow Bar */}
      <div className="arch-flow-nodes">
        {steps.map((step, idx) => {
          const isActive = idx === activeStep;
          const isPassed = idx < activeStep;

          return (
            <React.Fragment key={step.id}>
              <div 
                onClick={() => setActiveStep(idx)}
                className={`arch-node-box ${isActive ? 'active' : ''} ${isPassed ? 'passed' : ''}`}
              >
                <div className="node-icon-wrapper">
                  {step.icon}
                </div>
                <span className="node-name">{step.name}</span>
                <span className="node-service">{step.service}</span>
                {isActive && <div className="node-active-pulse" />}
              </div>
              {idx < steps.length - 1 && (
                <div className={`arch-flow-connector ${isPassed ? 'passed-line' : ''}`}>
                  <ArrowRight size={16} />
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>

      {/* Step Detail Inspector Box */}
      <div className="arch-detail-inspector">
        <div className="inspector-header">
          <div className="inspector-step-num">Step {activeStep + 1} of {steps.length}</div>
          <h4 className="inspector-step-name">{steps[activeStep].name}</h4>
        </div>
        <p className="inspector-desc">{steps[activeStep].desc}</p>

        <div className="inspector-payload-box">
          <div className="payload-tag">SIMULATED PAYLOAD & RUNTIME STATE</div>
          <code>{steps[activeStep].payload}</code>
        </div>
      </div>
    </div>
  );
};

export const WorkflowVisualizer = ({ title = "Agentic Execution Workflow" }) => {
  return <ArchitectureDiagram title={title} />;
};

export const ServiceFlow = ({ title = "AWS Service Flow" }) => {
  return <ArchitectureDiagram title={title} />;
};

export const CloudDiagram = ({ title = "Cloud Infrastructure Overview" }) => {
  return <ArchitectureDiagram title={title} />;
};

export const ExecutionTimeline = ({ title = "Execution Timeline" }) => {
  return <ArchitectureDiagram title={title} />;
};
