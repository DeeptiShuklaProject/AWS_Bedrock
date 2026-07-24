export function parseMarkdown(mdText) {
  if (!mdText) return "";

  const lines = mdText.split("\n");
  let html = [];
  let inCodeBlock = false;
  let codeContent = [];
  let codeLanguage = "";
  let inList = false;
  let inOrderedList = false;
  let inTable = false;
  let tableRows = [];

  const flushList = () => {
    if (inList) {
      html.push("</ul>");
      inList = false;
    }
    if (inOrderedList) {
      html.push("</ol>");
      inOrderedList = false;
    }
  };

  const flushTable = () => {
    if (inTable) {
      if (tableRows.length > 0) {
        html.push("<table>");
        tableRows.forEach((row, rowIndex) => {
          const cells = row.split("|").slice(1, -1).map(c => c.trim());
          if (rowIndex === 0) {
            html.push("<thead><tr>" + cells.map(c => `<th>${parseInline(c)}</th>`).join("") + "</tr></thead>");
          } else if (rowIndex === 1 && cells.every(c => c.startsWith("-"))) {
            // It's the alignment separator line, skip
            return;
          } else {
            if (rowIndex === 2 && tableRows[1] && tableRows[1].includes("-")) {
              html.push("<tbody>");
            }
            html.push("<tr>" + cells.map(c => `<td>${parseInline(c)}</td>`).join("") + "</tr>");
          }
        });
        if (tableRows.length > 2 || (tableRows[1] && !tableRows[1].includes("-"))) {
          html.push("</tbody>");
        }
        html.push("</table>");
      }
      tableRows = [];
      inTable = false;
    }
  };

  const parseInline = (text) => {
    // 1. Strip HTML anchor bookmark tags (e.g. <a name="section-id"></a>) — they're invisible navigation targets
    let safeText = text.replace(/<a\s+name="[^"]*"\s*>\s*<\/a>/gi, '');

    // 2. Strip any remaining self-closing or empty HTML tags that shouldn't display
    safeText = safeText.replace(/<a\s+[^>]*>\s*<\/a>/gi, '');

    // 3. Escape remaining HTML entities (to avoid rendering arbitrary tags)
    safeText = safeText
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

    // 4. Inline Code: `code`
    safeText = safeText.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');

    // 5. Bold: **text**
    safeText = safeText.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");

    // 6. Italic: *text*
    safeText = safeText.replace(/\*([^*]+)\*/g, "<em>$1</em>");

    // 7. Image markdown: ![alt](src) — MUST run before link regex to avoid ![alt](src) matching as a link
    safeText = safeText.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" class="doc-img" />');

    // 8. Links: [text](url)
    safeText = safeText.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (match, linkText, url) => {
      // If the link points to a .html file, replace it with .md so our reader handles it
      let targetUrl = url;
      if (url.endsWith(".html")) {
        targetUrl = url.replace(".html", ".md");
      }
      const isExternal = url.startsWith('http://') || url.startsWith('https://') || url.startsWith('//');
      if (isExternal) {
        return `<a href="${targetUrl}" class="doc-link external-link" target="_blank" rel="noopener noreferrer">${linkText}</a>`;
      }
      return `<a href="${targetUrl}" class="doc-link">${linkText}</a>`;
    });

    return safeText;
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Handle Code Blocks
    if (line.trim().startsWith("```")) {
      if (inCodeBlock) {
        // End of code block
        html.push(`<pre><div class="code-header">${codeLanguage}</div><code class="code-block">${codeContent.join("\n")}</code></pre>`);
        codeContent = [];
        inCodeBlock = false;
      } else {
        // Start of code block
        flushList();
        flushTable();
        inCodeBlock = true;
        codeLanguage = line.trim().slice(3) || "code";
      }
      continue;
    }

    if (inCodeBlock) {
      // Escape HTML entities inside code block
      codeContent.push(line.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"));
      continue;
    }

    // Handle Tables
    if (line.trim().startsWith("|")) {
      flushList();
      inTable = true;
      tableRows.push(line);
      continue;
    } else if (inTable) {
      flushTable();
    }

    // Handle Headings
    if (line.startsWith("#")) {
      flushList();
      const match = line.match(/^(#{1,6})\s+(.*)$/);
      if (match) {
        const level = match[1].length;
        const text = match[2];
        const headingId = text
          .toLowerCase()
          .trim()
          .replace(/<[^>]*>/g, '')
          .replace(/[^\w\s-]/g, '')
          .replace(/[\s_]+/g, '-')
          .replace(/^-+|-+$/g, '');

        html.push(`<h${level} id="${headingId}">${parseInline(text)}</h${level}>`);
        continue;
      }
    }

    // Handle Blockquotes
    if (line.trim().startsWith(">")) {
      flushList();
      // Detect Github Alerts (strategic note alerts)
      const alertMatch = line.match(/^>\s+\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]/i);
      if (alertMatch) {
        const alertType = alertMatch[1].toUpperCase();
        let alertLines = [];
        i++;
        while (i < lines.length && lines[i].trim().startsWith(">")) {
          alertLines.push(lines[i].trim().slice(1).trim());
          i++;
        }
        i--; // Step back
        html.push(`<div class="alert-box alert-${alertType.toLowerCase()}">
          <div class="alert-title">${alertType}</div>
          <div class="alert-content">${parseMarkdown(alertLines.join("\n"))}</div>
        </div>`);
        continue;
      } else {
        const quoteText = line.trim().slice(1).trim();
        html.push(`<blockquote>${parseInline(quoteText)}</blockquote>`);
        continue;
      }
    }

    // Handle Unordered Lists
    if (line.trim().startsWith("- ") || line.trim().startsWith("+ ") || line.trim().startsWith("* ")) {
      if (inOrderedList) flushList();
      if (!inList) {
        html.push("<ul>");
        inList = true;
      }
      const itemText = line.trim().slice(2);
      html.push(`<li>${parseInline(itemText)}</li>`);
      continue;
    }

    // Handle Ordered Lists
    const orderedMatch = line.trim().match(/^(\d+)\.\s+(.*)$/);
    if (orderedMatch) {
      if (inList) flushList();
      if (!inOrderedList) {
        html.push("<ol>");
        inOrderedList = true;
      }
      const itemText = orderedMatch[2];
      html.push(`<li>${parseInline(itemText)}</li>`);
      continue;
    }

    // Handle Horizontal Rules
    if (line.trim() === "---" || line.trim() === "***") {
      flushList();
      html.push("<hr />");
      continue;
    }

    // Empty lines
    if (line.trim() === "") {
      flushList();
      continue;
    }

    // Paragraphs
    flushList();
    html.push(`<p>${parseInline(line)}</p>`);
  }

  // Final flushes
  flushList();
  flushTable();

  return html.join("\n");
}
