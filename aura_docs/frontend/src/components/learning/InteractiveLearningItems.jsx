import React, { useState } from 'react';
import { 
  HelpCircle, 
  CheckCircle2, 
  XCircle, 
  RotateCw, 
  Sparkles, 
  Award, 
  ChevronDown, 
  ChevronUp, 
  Eye, 
  EyeOff, 
  BrainCircuit, 
  FileText 
} from 'lucide-react';

// ==========================================
// 1. Interactive Knowledge Check (Quiz Component)
// ==========================================
export const KnowledgeCheck = ({ 
  question = "What is the primary function of Amazon Bedrock AgentCore Runtime?", 
  options = [
    "A. Provide a serverless UI dashboard for LLMs",
    "B. Provide code-first microVM container isolation for autonomous AI agent execution",
    "C. Manage DNS routing for AWS API Gateway",
    "D. Compile Python code into C++ binaries"
  ],
  correctIndex = 1,
  explanation = "Bedrock AgentCore provides MicroVM containerized sandbox environments with strict tenant isolation to execute code-first autonomous agents and tools securely on AWS."
}) => {
  const [selectedIndex, setSelectedIndex] = useState(null);
  const [submitted, setSubmitted] = useState(false);

  const handleSelect = (idx) => {
    if (submitted) return;
    setSelectedIndex(idx);
    setSubmitted(true);
  };

  const resetQuiz = () => {
    setSelectedIndex(null);
    setSubmitted(false);
  };

  return (
    <div className="knowledge-check-card">
      <div className="kc-header">
        <BrainCircuit size={18} className="kc-icon text-indigo-400" />
        <span className="kc-title">KNOWLEDGE CHECK & QUIZ</span>
      </div>

      <p className="kc-question">{question}</p>

      <div className="kc-options-list">
        {options.map((opt, idx) => {
          const isSelected = selectedIndex === idx;
          const isCorrect = idx === correctIndex;
          
          let btnClass = "kc-option-btn";
          if (submitted) {
            if (isCorrect) btnClass += " correct";
            else if (isSelected) btnClass += " incorrect";
          }

          return (
            <button
              key={idx}
              onClick={() => handleSelect(idx)}
              className={btnClass}
              disabled={submitted}
            >
              <div className="option-indicator">
                {submitted && isCorrect ? (
                  <CheckCircle2 size={16} className="text-emerald-500" />
                ) : submitted && isSelected && !isCorrect ? (
                  <XCircle size={16} className="text-rose-500" />
                ) : (
                  <div className="option-bullet">{String.fromCharCode(65 + idx)}</div>
                )}
              </div>
              <span className="option-text">{opt}</span>
            </button>
          );
        })}
      </div>

      {submitted && (
        <div className={`kc-feedback-box ${selectedIndex === correctIndex ? 'feedback-correct' : 'feedback-incorrect'}`}>
          <div className="feedback-status">
            {selectedIndex === correctIndex ? (
              <>
                <CheckCircle2 size={16} />
                <span>Spot On! Correct Answer.</span>
              </>
            ) : (
              <>
                <XCircle size={16} />
                <span>Not quite! Review the explanation below:</span>
              </>
            )}
          </div>
          <p className="feedback-explanation">{explanation}</p>
          <button onClick={resetQuiz} className="kc-reset-btn">
            <RotateCw size={13} />
            <span>Try Again</span>
          </button>
        </div>
      )}
    </div>
  );
};

// ==========================================
// 2. Interview Question Component
// ==========================================
export const InterviewQuestion = ({ 
  question = "How does Bedrock AgentCore enforce tenant isolation during tool execution?",
  difficulty = "ADVANCED",
  idealAnswer = "Bedrock AgentCore provisions dedicated MicroVM container environments per session. Each tool call or sandbox code execution runs inside an isolated environment with restricted IAM role permissions, preventing cross-tenant data leakage.",
  keyPoints = [
    "MicroVM container isolation per execution session",
    "Scoped IAM execution roles with least-privilege policies",
    "Short-lived temporary credential tokens for tool gateways",
    "No persistent local storage across unauthenticated sessions"
  ]
}) => {
  const [showAnswer, setShowAnswer] = useState(false);

  return (
    <div className="interview-q-card">
      <div className="iq-header">
        <div className="iq-title-group">
          <Award size={18} className="iq-icon text-amber-400" />
          <div>
            <span className="iq-badge">{difficulty} INTERVIEW QUESTION</span>
            <h4 className="iq-question">{question}</h4>
          </div>
        </div>
        <button 
          onClick={() => setShowAnswer(!showAnswer)}
          className="iq-reveal-btn"
        >
          {showAnswer ? <EyeOff size={14} /> : <Eye size={14} />}
          <span>{showAnswer ? "Hide Ideal Answer" : "Reveal Ideal Answer"}</span>
        </button>
      </div>

      {showAnswer && (
        <div className="iq-answer-box">
          <div className="answer-section-title">
            <Sparkles size={14} className="text-amber-400" />
            <span>Principal Engineer Ideal Response:</span>
          </div>
          <p className="ideal-answer-text">{idealAnswer}</p>

          <div className="answer-key-points">
            <span className="points-title">Key Architectural Points to Mention in Interview:</span>
            <ul>
              {keyPoints.map((pt, i) => (
                <li key={i}>
                  <CheckCircle2 size={14} className="text-emerald-400 flex-shrink-0" />
                  <span>{pt}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export const InterviewQuestions = ({ questions = [] }) => {
  return (
    <div className="interview-group-container">
      {questions.map((q, i) => (
        <InterviewQuestion key={i} {...q} />
      ))}
    </div>
  );
};

// ==========================================
// 3. Interactive FlashCard Component
// ==========================================
export const FlashCard = ({ 
  front = "What is the ReAct (Reasoning + Acting) loop in Bedrock AgentCore?", 
  back = "ReAct is an iterative prompting pattern where the LLM generates a Thought, selects an Action (Tool call), receives an Observation (Tool output), and repeats until reaching the final Answer." 
}) => {
  const [flipped, setFlipped] = useState(false);

  return (
    <div className="flashcard-container" onClick={() => setFlipped(!flipped)}>
      <div className={`flashcard-inner ${flipped ? 'flipped' : ''}`}>
        <div className="flashcard-front">
          <div className="fc-tag">CLICK TO FLIP</div>
          <BrainCircuit size={28} className="fc-icon text-indigo-400" />
          <p className="fc-text">{front}</p>
        </div>
        <div className="flashcard-back">
          <div className="fc-tag">KEY CONCEPT ANSWER</div>
          <p className="fc-text">{back}</p>
        </div>
      </div>
    </div>
  );
};

export const FlashCards = ({ cards = [] }) => {
  return (
    <div className="flashcards-grid">
      {cards.map((c, idx) => (
        <FlashCard key={idx} front={c.front} back={c.back} />
      ))}
    </div>
  );
};

export const QuickRevision = ({ items = [] }) => {
  return (
    <div className="quick-revision-card">
      <div className="qr-header">
        <FileText size={18} className="text-indigo-400" />
        <span>QUICK REVISION SUMMARY</span>
      </div>
      <ul className="qr-list">
        {items.map((item, idx) => (
          <li key={idx}>
            <Sparkles size={14} className="text-indigo-400" />
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};
