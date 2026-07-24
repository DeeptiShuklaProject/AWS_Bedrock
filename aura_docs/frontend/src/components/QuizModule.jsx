import React, { useState } from 'react';
import { Award, CheckCircle2, XCircle, RefreshCw, BookOpen, Sparkles } from 'lucide-react';

const QUIZ_QUESTIONS = [
  {
    id: 1,
    category: "Core AWS & IAM",
    question: "What is the primary function of AWS IAM (Identity and Access Management)?",
    options: [
      "To automatically scale EC2 server instances based on traffic demand.",
      "To securely control authentication and authorization for AWS services and resources.",
      "To store relational structured data across multiple availability zones.",
      "To cache static web assets at global edge locations using CloudFront."
    ],
    correctAnswer: 1,
    explanation: "AWS IAM lets you define who (authentication) can perform actions on which AWS resources (authorization) using permissions policies."
  },
  {
    id: 2,
    category: "Core AWS & IAM",
    question: "In AWS IAM, what is the best practice recommendation regarding Root user access?",
    options: [
      "Use the root account for daily administrative tasks.",
      "Share root credentials with senior engineering team members.",
      "Lock down root credentials, enable MFA, and create individual IAM users/roles for daily tasks.",
      "Disable MFA on root account to prevent lockout."
    ],
    correctAnswer: 2,
    explanation: "AWS security best practice mandates locking down the root user credentials, enabling MFA, and using IAM policies/roles for daily tasks."
  },
  {
    id: 3,
    category: "Amazon EC2 & VPC",
    question: "Which VPC component enables instances in a private subnet to connect to the internet while preventing incoming requests from the internet?",
    options: [
      "Internet Gateway (IGW)",
      "NAT Gateway",
      "VPC Peering Connection",
      "Route Table"
    ],
    correctAnswer: 1,
    explanation: "A NAT Gateway allows instances in a private subnet to initiate outbound IPv4 connections to the internet for updates while keeping them shielded from unsolicited inbound connections."
  },
  {
    id: 4,
    category: "Amazon EC2 & VPC",
    question: "What is the key difference between Security Groups and Network ACLs (NACLs) in AWS VPC?",
    options: [
      "Security Groups operate at the subnet level and are stateless; NACLs operate at the instance level and are stateful.",
      "Security Groups operate at the instance level and are stateful; NACLs operate at the subnet level and are stateless.",
      "Security Groups only support ALLOW rules; NACLs only support DENY rules.",
      "Security Groups require an Internet Gateway to function."
    ],
    correctAnswer: 1,
    explanation: "Security Groups act as a stateful firewall for instances (inbound rules automatically allow return traffic). NACLs act as stateless sub-net boundary firewalls evaluating rules in numbered order."
  },
  {
    id: 5,
    category: "Amazon Bedrock & GenAI",
    question: "What is Amazon Bedrock Knowledge Bases primarily used for?",
    options: [
      "Fine-tuning open-source foundation models from scratch on custom GPUs.",
      "Connecting foundation models to proprietary company data sources to implement Retrieval-Augmented Generation (RAG).",
      "Managing Docker container registries for GenAI microservices.",
      "Monitoring AWS infrastructure metrics using Machine Learning logs."
    ],
    correctAnswer: 1,
    explanation: "Amazon Bedrock Knowledge Bases automates the end-to-end RAG workflow, chunking, embedding, storing in vector stores, and querying data to enrich model responses."
  },
  {
    id: 6,
    category: "Amazon Bedrock & GenAI",
    question: "In GenAI models, what does the 'Temperature' parameter control?",
    options: [
      "The physical CPU temperature of the AWS server hosting the model.",
      "The degree of randomness or creativity in the model's generated responses.",
      "The maximum number of concurrent tokens allowed in a prompt.",
      "The response streaming speed in milliseconds."
    ],
    correctAnswer: 1,
    explanation: "Temperature controls response randomness: lower values (e.g. 0.1) produce deterministic, factual outputs; higher values (e.g. 0.8) produce more creative responses."
  },
  {
    id: 7,
    category: "Amazon Bedrock & GenAI",
    question: "What capability do Amazon Bedrock Agents provide to Foundation Models?",
    options: [
      "They allow models to execute multi-step business logic by calling AWS Lambda functions and API tools autonomously.",
      "They compress model size to run offline on mobile devices.",
      "They automate billing and invoice collection for AI usage.",
      "They generate synthetic dataset images."
    ],
    correctAnswer: 0,
    explanation: "Bedrock Agents break down user prompts, orchestrate multi-step workflows, query knowledge bases, and execute Lambda functions/APIs to fulfill tasks."
  },
  {
    id: 8,
    category: "Serverless & AWS Lambda",
    question: "What is a 'Cold Start' in AWS Lambda?",
    options: [
      "A hardware failure in an AWS availability zone.",
      "The latency delay when Lambda initializes a new execution environment upon receiving an initial request.",
      "Running Lambda functions inside a local Docker container for testing.",
      "Compiling Python code before deployment."
    ],
    correctAnswer: 1,
    explanation: "A Cold Start occurs when Lambda must spin up a fresh execution container, download your code, and initialize runtimes before executing your handler function."
  },
  {
    id: 9,
    category: "Serverless & AWS Lambda",
    question: "How can developers mitigate Lambda cold start latency for latency-sensitive applications?",
    options: [
      "Increase function timeout limit to 15 minutes.",
      "Enable Provisioned Concurrency to pre-initialize execution environments.",
      "Store all data in S3 instead of DynamoDB.",
      "Use HTTP Basic Auth."
    ],
    correctAnswer: 1,
    explanation: "Provisioned Concurrency keeps a designated number of execution environments warm and ready to respond immediately without cold start delays."
  },
  {
    id: 10,
    category: "Containers & DevOps",
    question: "What is the main benefit of AWS Fargate when running ECS or EKS container workloads?",
    options: [
      "It provides free unlimited storage for Docker images.",
      "It is a serverless compute engine that removes the need to provision and manage EC2 servers for containers.",
      "It replaces Docker with virtual machine hypervisors.",
      "It automatically writes Kubernetes YAML manifests."
    ],
    correctAnswer: 1,
    explanation: "AWS Fargate lets you run containers without managing underlying EC2 instances, provisioning clusters, or patching host OS layers."
  },
  {
    id: 11,
    category: "Containers & DevOps",
    question: "Which AWS service is a managed Docker container registry for storing and managing container images?",
    options: [
      "Amazon EKS",
      "Amazon ECR (Elastic Container Registry)",
      "AWS CodeDeploy",
      "Amazon S3"
    ],
    correctAnswer: 1,
    explanation: "Amazon ECR is a fully managed container registry that makes it easy to store, manage, share, and deploy Docker container images."
  },
  {
    id: 12,
    category: "Security & Operations",
    question: "According to the AWS Shared Responsibility Model, which responsibility belongs exclusively to AWS?",
    options: [
      "Customer data encryption and IAM policy configuration.",
      "Physical security of data centers and hypervisor infrastructure.",
      "Application code updates and bug fixes.",
      "Operating system security patching on EC2 instances."
    ],
    correctAnswer: 1,
    explanation: "AWS is responsible for 'Security OF the Cloud' (physical infrastructure, hardware, hypervisor, facilities), while customers are responsible for 'Security IN the Cloud' (data, OS, IAM)."
  },
  {
    id: 13,
    category: "Security & Operations",
    question: "Which service records all AWS API calls and configuration changes for auditing and governance?",
    options: [
      "Amazon CloudWatch",
      "AWS CloudTrail",
      "AWS GuardDuty",
      "AWS Trusted Advisor"
    ],
    correctAnswer: 1,
    explanation: "AWS CloudTrail logs and continuously monitors account activity related to API calls across your AWS infrastructure for compliance and security auditing."
  },
  {
    id: 14,
    category: "Security & Operations",
    question: "What is the role of Amazon CloudWatch in AWS architecture?",
    options: [
      "To store relational SQL database snapshots.",
      "To collect metrics, logs, set alarms, and monitor performance across AWS resources.",
      "To route DNS domain requests to server IP addresses.",
      "To manage SSL/TLS certificates."
    ],
    correctAnswer: 1,
    explanation: "Amazon CloudWatch provides monitoring and operational data in the form of logs, metrics, and alarms for AWS applications and services."
  },
  {
    id: 15,
    category: "Architectural Patterns",
    question: "What is the primary benefit of designing applications using loose coupling (e.g. SQS queues between services)?",
    options: [
      "It lowers network bandwidth costs to zero.",
      "It ensures failures in one component do not cascade and cause widespread failure across the entire application.",
      "It eliminates the need for database storage.",
      "It guarantees synchronous request execution."
    ],
    correctAnswer: 1,
    explanation: "Decoupled microservice architectures isolate components using queues (SQS) or event bridges so that temporary outages in one service do not break dependent services."
  },
  {
    id: 16,
    category: "Architectural Patterns",
    question: "What is Multi-AZ deployment designed to protect against in AWS Cloud Architecture?",
    options: [
      "Physical data center failures or localized outages in a single Availability Zone.",
      "Global fiber optic cable cuts across continents.",
      "Distributed Denial of Service (DDoS) SYN floods.",
      "Source code syntax errors."
    ],
    correctAnswer: 0,
    explanation: "Deploying applications across multiple Availability Zones (Multi-AZ) ensures high availability and automatic failover if one physical data center facility experiences an outage."
  },
  {
    id: 17,
    category: "Storage & Databases",
    question: "Which AWS storage service provides a fully managed, scalable NFS file system that can be mounted simultaneously by thousands of EC2 instances?",
    options: [
      "Amazon EBS (Elastic Block Store)",
      "Amazon EFS (Elastic File System)",
      "Amazon S3 Glacier",
      "AWS Snowball"
    ],
    correctAnswer: 1,
    explanation: "Amazon EFS provides serverless, fully elastic NFS storage accessible by multiple Linux EC2 instances and ECS containers concurrently."
  },
  {
    id: 18,
    category: "Storage & Databases",
    question: "What type of database is Amazon DynamoDB?",
    options: [
      "A relational PostgreSQL database.",
      "A fully managed serverless NoSQL key-value and document database.",
      "A graph database for social networking.",
      "An in-memory Redis cache."
    ],
    correctAnswer: 1,
    explanation: "Amazon DynamoDB is a serverless, single-digit millisecond NoSQL key-value database designed for internet-scale applications."
  },
  {
    id: 19,
    category: "DevOps & Infrastructure as Code",
    question: "What is the purpose of Infrastructure as Code (IaC) tools like Terraform or AWS CloudFormation?",
    options: [
      "To automatically convert Python scripts into Java code.",
      "To provision, manage, and version cloud infrastructure using declarative code files.",
      "To compile frontend React code into static HTML.",
      "To monitor CPU usage on virtual machines."
    ],
    correctAnswer: 1,
    explanation: "IaC enables developers to define infrastructure configuration in code files, enabling version control, repeatable deployments, and automated provisioning."
  },
  {
    id: 20,
    category: "Architectural Patterns",
    question: "Which AWS service is a global Content Delivery Network (CDN) service that securely delivers data, videos, and APIs with low latency?",
    options: [
      "Amazon Route 53",
      "Amazon CloudFront",
      "AWS Direct Connect",
      "AWS Transit Gateway"
    ],
    correctAnswer: 1,
    explanation: "Amazon CloudFront speeds up distribution of static and dynamic web content by serving request responses from global Edge Locations closest to end users."
  }
];

const QuizModule = ({ onBackToDocs }) => {
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [userAnswers, setUserAnswers] = useState({});

  const categories = ['All', ...new Set(QUIZ_QUESTIONS.map(q => q.category))];

  const filteredQuestions = selectedCategory === 'All'
    ? QUIZ_QUESTIONS
    : QUIZ_QUESTIONS.filter(q => q.category === selectedCategory);

  const handleSelectOption = (questionId, optionIdx) => {
    setUserAnswers(prev => ({ ...prev, [questionId]: optionIdx }));
  };

  const resetQuiz = () => {
    setUserAnswers({});
  };

  const totalAnswered = Object.keys(userAnswers).length;
  const correctCount = Object.keys(userAnswers).reduce((acc, qId) => {
    const question = QUIZ_QUESTIONS.find(q => q.id === parseInt(qId));
    if (question && userAnswers[qId] === question.correctAnswer) {
      return acc + 1;
    }
    return acc;
  }, 0);

  const percentage = totalAnswered > 0 ? Math.round((correctCount / totalAnswered) * 100) : 0;

  return (
    <div className="quiz-wrapper">
      {/* Score Header Banner */}
      <div className="quiz-score-banner">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontSize: '0.75rem', fontWeight: 800, color: 'var(--accent-orange)', marginBottom: '8px' }}>
              <Award size={16} />
              <span>Interactive Knowledge Check</span>
            </div>
            <h1 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.8rem', fontWeight: 900, color: 'var(--text-primary)' }}>
              20+ Practice Quiz Challenges
            </h1>
          </div>

          <div style={{ display: 'flex', gap: '12px' }}>
            <button onClick={resetQuiz} className="secondary-cta-btn" style={{ padding: '8px 16px', fontSize: '0.8rem' }}>
              <RefreshCw size={14} />
              <span>Reset Score</span>
            </button>
            <button onClick={onBackToDocs} className="primary-cta-btn" style={{ padding: '8px 16px', fontSize: '0.8rem' }}>
              <BookOpen size={14} />
              <span>Read Docs</span>
            </button>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="quiz-stats-grid">
          <div className="stat-box">
            <span style={{ fontSize: '0.72rem', color: 'var(--text-secondary)' }}>Total Questions</span>
            <div className="stat-val" style={{ color: 'var(--text-primary)' }}>{QUIZ_QUESTIONS.length}</div>
          </div>
          <div className="stat-box">
            <span style={{ fontSize: '0.72rem', color: 'var(--text-secondary)' }}>Answered</span>
            <div className="stat-val" style={{ color: 'var(--accent-cyan)' }}>{totalAnswered} / {QUIZ_QUESTIONS.length}</div>
          </div>
          <div className="stat-box">
            <span style={{ fontSize: '0.72rem', color: 'var(--text-secondary)' }}>Correct Score</span>
            <div className="stat-val" style={{ color: 'var(--accent-emerald)' }}>{correctCount}</div>
          </div>
          <div className="stat-box">
            <span style={{ fontSize: '0.72rem', color: 'var(--text-secondary)' }}>Accuracy Rate</span>
            <div className="stat-val" style={{ color: 'var(--accent-orange)' }}>{percentage}%</div>
          </div>
        </div>
      </div>

      {/* Category Pills */}
      <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '4px' }}>
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            style={{
              padding: '6px 14px',
              borderRadius: '10px',
              fontSize: '0.78rem',
              fontWeight: 700,
              whiteSpace: 'nowrap',
              cursor: 'pointer',
              background: selectedCategory === cat ? 'var(--accent-indigo)' : 'var(--bg-card)',
              color: selectedCategory === cat ? '#ffffff' : 'var(--text-secondary)',
              border: '1px solid var(--border-color)'
            }}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Questions List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {filteredQuestions.map((q, idx) => {
          const isAnswered = userAnswers[q.id] !== undefined;
          const selectedOption = userAnswers[q.id];
          const isCorrect = selectedOption === q.correctAnswer;

          return (
            <div key={q.id} className="quiz-card">
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ fontWeight: 800, fontSize: '0.85rem', color: 'var(--accent-indigo)', fontFamily: 'var(--font-mono)' }}>
                    Q{idx + 1}
                  </span>
                  <span className="category-tag">{q.category}</span>
                </div>

                {isAnswered && (
                  <span style={{
                    fontSize: '0.75rem',
                    fontWeight: 800,
                    padding: '2px 8px',
                    borderRadius: '12px',
                    background: isCorrect ? 'rgba(16,185,129,0.2)' : 'rgba(244,63,94,0.2)',
                    color: isCorrect ? '#6ee7b7' : '#fda4af'
                  }}>
                    {isCorrect ? 'Correct!' : 'Incorrect'}
                  </span>
                )}
              </div>

              <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-primary)', lineHeight: 1.5 }}>
                {q.question}
              </h3>

              {/* Options */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {q.options.map((opt, optIdx) => {
                  let optionClass = 'quiz-option-btn';
                  if (isAnswered) {
                    if (optIdx === q.correctAnswer) optionClass += ' correct';
                    else if (optIdx === selectedOption && !isCorrect) optionClass += ' incorrect';
                  }

                  return (
                    <button
                      key={optIdx}
                      onClick={() => handleSelectOption(q.id, optIdx)}
                      disabled={isAnswered}
                      className={optionClass}
                    >
                      <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, color: 'var(--text-muted)' }}>
                        {String.fromCharCode(65 + optIdx)}.
                      </span>
                      <span style={{ flex: 1 }}>{opt}</span>
                    </button>
                  );
                })}
              </div>

              {/* Explanation Box */}
              {isAnswered && (
                <div className="explanation-box">
                  <div style={{ fontWeight: 800, color: 'var(--accent-indigo)', marginBottom: '4px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <Sparkles size={14} />
                    <span>Explanation:</span>
                  </div>
                  <p>{q.explanation}</p>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default QuizModule;
