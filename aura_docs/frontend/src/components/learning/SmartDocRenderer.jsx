import React, { useMemo } from 'react';
import { CourseHeader } from './CourseHeader';
import { InteractiveCodeBlock } from './InteractiveCodeBlock';
import { 
  ConceptCard, 
  WhyItMatters, 
  KeyTakeaways, 
  BestPractices, 
  CommonMistakes, 
  InfoCard, 
  WarningCard, 
  TipCard, 
  InterviewTip, 
  Accordion 
} from './LearningCards';
import { 
  ArchitectureDiagram, 
  WorkflowVisualizer, 
  ExecutionTimeline, 
  ServiceFlow, 
  CloudDiagram 
} from './ArchitectureVisualizers';
import { 
  KnowledgeCheck, 
  InterviewQuestion, 
  FlashCards, 
  QuickRevision 
} from './InteractiveLearningItems';
import { PageExperienceControls } from './PageExperienceControls';
import { parseMarkdown } from '../../utils/markdownParser';
import { Hash, Link as LinkIcon } from 'lucide-react';

export const SmartDocRenderer = ({ 
  docContent, 
  docPath, 
  selectedKb, 
  renderWidget, 
  renderMermaid 
}) => {
  // 1. Extract Headings for TOC & Section Anchors
  const headings = useMemo(() => {
    if (!docContent) return [];
    const matches = [];
    const lines = docContent.split('\n');
    lines.forEach(line => {
      const match = line.match(/^(#{1,4})\s+(.*)$/);
      if (match) {
        const level = match[1].length;
        const text = match[2].trim();
        const id = text.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-');
        matches.push({ level, text, id });
      }
    });
    return matches;
  }, [docContent]);

  const wordCount = useMemo(() => {
    return docContent ? docContent.split(/\s+/).length : 1000;
  }, [docContent]);

  const mainTitle = useMemo(() => {
    if (headings.length > 0) return headings[0].text;
    return docPath ? docPath.split('/').pop().replace(/\.md$/, '') : 'Documentation Module';
  }, [headings, docPath]);

  // Smooth scroll handler for TOC clicks
  const scrollToHeading = (id) => {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  // 2. Parse Markdown into Rich Structural Blocks
  const renderedContentBlocks = useMemo(() => {
    if (!docContent) return null;

    const lines = docContent.split('\n');
    const blocks = [];
    let i = 0;

    let inCode = false;
    let codeLang = '';
    let codeBuffer = [];
    let textBuffer = [];

    const flushText = () => {
      if (textBuffer.length > 0) {
        const textSegment = textBuffer.join('\n');
        if (textSegment.trim()) {
          blocks.push({ type: 'markdown_html', content: textSegment });
        }
        textBuffer = [];
      }
    };

    while (i < lines.length) {
      const line = lines[i];

      // Match ```widget:type or ```mermaid or standard code blocks ```
      if (line.trim().startsWith('```')) {
        flushText();
        if (inCode) {
          // Closing code block
          const fullCode = codeBuffer.join('\n');
          if (codeLang.startsWith('widget:')) {
            const widgetType = codeLang.replace('widget:', '');
            blocks.push({ type: 'widget', widgetType, content: fullCode });
          } else if (codeLang === 'mermaid') {
            blocks.push({ type: 'mermaid', content: fullCode });
          } else {
            blocks.push({ 
              type: 'code_block', 
              language: codeLang || 'code', 
              content: fullCode 
            });
          }
          codeBuffer = [];
          codeLang = '';
          inCode = false;
        } else {
          // Opening code block
          inCode = true;
          codeLang = line.trim().slice(3).trim();
          codeBuffer = [];
        }
        i++;
        continue;
      }

      if (inCode) {
        codeBuffer.push(line);
        i++;
        continue;
      }

      // Match Headings and attach interactive visualizers when relevant!
      const headingMatch = line.match(/^(#{1,4})\s+(.*)$/);
      if (headingMatch) {
        flushText();
        const level = headingMatch[1].length;
        const text = headingMatch[2].trim();
        const id = text.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-');
        
        blocks.push({ type: 'heading', level, text, id });

        // Auto-inject visualizers for architecture/workflow/runtime headings
        const lowerText = text.toLowerCase();
        if (
          lowerText.includes('architecture') || 
          lowerText.includes('runtime') || 
          lowerText.includes('workflow') || 
          lowerText.includes('how does it work') ||
          lowerText.includes('gateway') ||
          lowerText.includes('execution')
        ) {
          blocks.push({ type: 'visualizer', title: text });
        }

        // Auto-inject quiz/interview component if section title mentions quiz/interview
        if (lowerText.includes('quiz') || lowerText.includes('knowledge check')) {
          blocks.push({ type: 'knowledge_check' });
        } else if (lowerText.includes('interview')) {
          blocks.push({ type: 'interview_questions' });
        }

        i++;
        continue;
      }

      // Match Callouts / Alerts (> [!NOTE], etc.)
      const alertMatch = line.match(/^>\s+\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]/i);
      if (alertMatch) {
        flushText();
        const alertType = alertMatch[1].toUpperCase();
        let alertLines = [];
        i++;
        while (i < lines.length && lines[i].trim().startsWith('>')) {
          alertLines.push(lines[i].trim().slice(1).trim());
          i++;
        }
        blocks.push({ 
          type: 'alert', 
          alertType, 
          content: alertLines.join('\n') 
        });
        continue;
      }

      textBuffer.push(line);
      i++;
    }

    flushText();
    return blocks;
  }, [docContent]);

  return (
    <div className="smart-doc-renderer-container">
      {/* Top Page Experience Controls (Progress Bar, TOC, Keyboard Navigation) */}
      <PageExperienceControls headings={headings} onSelectHeading={scrollToHeading} />

      {/* Modern Course Header */}
      <CourseHeader 
        title={mainTitle}
        docPath={docPath}
        wordCount={wordCount}
        headings={headings}
        onSelectHeading={scrollToHeading}
      />

      {/* Rendered Document Content Stream */}
      <div className="smart-doc-stream">
        {renderedContentBlocks && renderedContentBlocks.map((block, index) => {
          if (block.type === 'heading') {
            const Tag = `h${Math.min(block.level + 1, 4)}`;
            return (
              <div key={index} id={block.id} className="smart-heading-wrapper">
                <Tag className={`smart-heading level-${block.level}`}>
                  <span>{block.text}</span>
                  <button 
                    onClick={() => scrollToHeading(block.id)} 
                    className="heading-anchor-btn"
                    title="Copy section link"
                  >
                    <Hash size={16} />
                  </button>
                </Tag>
              </div>
            );
          }

          if (block.type === 'code_block') {
            return (
              <InteractiveCodeBlock 
                key={index} 
                code={block.content} 
                language={block.language} 
              />
            );
          }

          if (block.type === 'widget') {
            return renderWidget ? renderWidget(block.widgetType, block.content) : null;
          }

          if (block.type === 'mermaid') {
            return renderMermaid ? renderMermaid(block.content) : null;
          }

          if (block.type === 'alert') {
            const htmlContent = parseMarkdown(block.content);
            const contentEl = <div dangerouslySetInnerHTML={{ __html: htmlContent }} />;

            switch (block.alertType) {
              case 'WARNING':
              case 'CAUTION':
                return <WarningCard key={index}>{contentEl}</WarningCard>;
              case 'TIP':
                return <TipCard key={index}>{contentEl}</TipCard>;
              case 'IMPORTANT':
                return <InfoCard key={index}>{contentEl}</InfoCard>;
              default:
                return <InfoCard key={index}>{contentEl}</InfoCard>;
            }
          }

          if (block.type === 'visualizer') {
            return <ArchitectureDiagram key={index} title={`${block.title} Visual Flow`} />;
          }

          if (block.type === 'knowledge_check') {
            return <KnowledgeCheck key={index} />;
          }

          if (block.type === 'interview_questions') {
            return <InterviewQuestion key={index} />;
          }

          if (block.type === 'markdown_html') {
            const parsedHtml = parseMarkdown(block.content);
            return (
              <div 
                key={index} 
                className="smart-markdown-paragraph"
                dangerouslySetInnerHTML={{ __html: parsedHtml }} 
              />
            );
          }

          return null;
        })}
      </div>
    </div>
  );
};
