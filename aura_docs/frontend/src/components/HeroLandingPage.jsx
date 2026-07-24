import React from 'react';
import { 
  Search, 
  Award, 
  Cloud, 
  Cpu, 
  ShieldCheck, 
  Box, 
  Zap, 
  ArrowRight, 
  Sparkles,
  Terminal
} from 'lucide-react';

const CATEGORIES = [
  {
    title: "Phase 01: Core AWS",
    icon: Cloud,
    badge: "Foundations",
    description: "Master EC2, VPC networking, IAM security, S3 storage, and cloud infrastructure essentials."
  },
  {
    title: "Phase 02: Modern App Dev",
    icon: Zap,
    badge: "Serverless & APIs",
    description: "Build serverless microservices with AWS Lambda, API Gateway, EventBridge, and DynamoDB."
  },
  {
    title: "Phase 03: Containers & DevOps",
    icon: Box,
    badge: "Docker & Kubernetes",
    description: "Deploy microservices with Amazon ECS, Fargate, ECR, Terraform IaC, and CI/CD pipelines."
  },
  {
    title: "Phase 04: Security & Ops",
    icon: ShieldCheck,
    badge: "Governance & Auditing",
    description: "Implement security controls, KMS encryption, CloudTrail auditing, and CloudWatch telemetry."
  },
  {
    title: "Phase 05: Architect Level",
    icon: Cpu,
    badge: "Enterprise Architecture",
    description: "Design fault-tolerant Multi-AZ architectures, disaster recovery, and high availability systems."
  },
  {
    title: "Phase 06: GenAI & Bedrock",
    icon: Sparkles,
    badge: "AI Agents & RAG",
    description: "Leverage Foundation Models, RAG Knowledge Bases, and Bedrock Agents for AI applications."
  }
];

const HeroLandingPage = ({ navItems = [], onOpenSearch, onOpenQuizzes, onOpenPlayground, onSelectDoc }) => {
  // Dynamically find first valid document for a module from navItems tree
  const getCategoryDoc = (index) => {
    if (!Array.isArray(navItems) || navItems.length === 0) return null;

    const getFirstFile = (node) => {
      if (!node) return null;
      if (node.href || node.path) return node.href || node.path;
      const children = node.contents || node.children || [];
      for (const child of children) {
        const found = getFirstFile(child);
        if (found) return found;
      }
      return null;
    };

    const phaseStr = `Phase 0${index + 1}`;
    const matchedNode = navItems.find(item => {
      const t = (item.title || item.name || '').toLowerCase();
      return t.includes(phaseStr.toLowerCase()) || t.includes(`phase ${index + 1}`);
    });

    if (matchedNode) {
      const doc = getFirstFile(matchedNode);
      if (doc) return doc;
    }

    if (navItems[index]) {
      const doc = getFirstFile(navItems[index]);
      if (doc) return doc;
    }

    for (const item of navItems) {
      const doc = getFirstFile(item);
      if (doc) return doc;
    }

    return null;
  };

  return (
    <div className="hero-wrapper">
      {/* Hero Banner Card */}
      <div className="hero-banner-card">
        <div className="hero-glow-1" />
        <div className="hero-glow-2" />

        <div style={{ position: 'relative', zIndex: 10 }}>
          <div className="hero-pill-badge">
            <Sparkles size={14} style={{ color: 'var(--accent-cyan)' }} />
            <span>Interactive Developer Documentation Portal</span>
          </div>

          <h1 className="hero-headline">
            Master Cloud & AI Architecture <br />
            <span className="gradient-text">With Interactive Documentation</span>
          </h1>

          <p className="hero-description">
            Comprehensive reference guides, live Python code playgrounds, architecture diagrams, and 20+ interactive practice quizzes—all in one place.
          </p>

          <div className="hero-cta-group">
            <button onClick={onOpenSearch} className="primary-cta-btn">
              <Search size={18} />
              <span>Search All Documentation</span>
              <kbd style={{ fontSize: '0.65rem', background: 'rgba(0,0,0,0.25)', padding: '2px 6px', borderRadius: '4px', fontFamily: 'var(--font-mono)' }}>ctrl K</kbd>
            </button>

            <button onClick={onOpenPlayground} className="secondary-cta-btn" style={{ borderColor: 'var(--accent-cyan)', color: 'var(--accent-cyan)' }}>
              <Terminal size={18} />
              <span>Open Code Playground</span>
            </button>

            <button onClick={onOpenQuizzes} className="secondary-cta-btn">
              <Award size={18} style={{ color: 'var(--accent-orange)' }} />
              <span>Try 20+ Practice Quizzes</span>
            </button>
          </div>
        </div>
      </div>

      {/* Module Categories Grid */}
      <div>
        <h2 className="module-section-title">Documentation Modules</h2>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
          Explore structured learning paths and comprehensive AWS guides
        </p>

        <div className="category-grid">
          {CATEGORIES.map((cat, idx) => {
            const Icon = cat.icon;
            const docPath = getCategoryDoc(idx);

            return (
              <div
                key={idx}
                onClick={() => {
                  if (docPath) onSelectDoc(docPath);
                }}
                className="category-card"
              >
                <div>
                  <div className="category-card-top">
                    <div className="category-icon-box">
                      <Icon size={22} />
                    </div>
                    <span className="category-tag">{cat.badge}</span>
                  </div>

                  <h3 className="category-card-title">{cat.title}</h3>
                  <p className="category-card-desc">{cat.description}</p>
                </div>

                <div className="category-card-link">
                  <span>Start Reading</span>
                  <ArrowRight size={14} />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Interactive Code Playground Promo Banner */}
      <div className="promo-banner-card">
        <div>
          <div style={{ fontSize: '0.78rem', fontWeight: 800, color: 'var(--accent-cyan)', textTransform: 'uppercase', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Terminal size={16} />
            <span>Interactive Code Execution Engine</span>
          </div>
          <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.4rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '6px' }}>
            Test AWS Boto3 & Python Code Live in Your Browser
          </h3>
          <p style={{ fontSize: '0.98rem', color: 'var(--text-secondary)' }}>
            Experiment with pre-built AWS Bedrock, IAM policy, S3, and EC2 Python scripts with live console output.
          </p>
        </div>

        <button onClick={onOpenPlayground} className="primary-cta-btn" style={{ padding: '14px 28px', fontSize: '0.95rem', shrink: 0 }}>
          Launch Code Playground
        </button>
      </div>
    </div>
  );
};

export default HeroLandingPage;
