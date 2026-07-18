const fs = require('fs');

const tagRegex = /(<\/?[A-Z][A-Za-z0-9_]*(?:\s+[a-zA-Z0-9_-]+=(?:"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|\[[^\]]*\]|{(?:[^{}]|(?:{[^{}]*}))*}|{[^}]+}|\d+|true|false))*?\s*\/?>)/g;

function parseMDXContent(content) {
  const tokens = content.split(tagRegex);
  const root = { type: 'root', children: [] };
  const stack = [root];
  let count = 0;
  
  for (let i = 0; i < tokens.length; i++) {
    const token = tokens[i];
    if (!token) continue;
    
    if (token.startsWith('<') && token.endsWith('>')) {
      const isClosing = token.startsWith('</');
      const isSelfClosing = token.endsWith('/>');
      const nameMatch = token.match(/^<\/?([A-Z][A-Za-z0-9_]*)/);
      const tagName = nameMatch ? nameMatch[1] : '';
      
      console.log(`[${count++}] Parsed Tag: ${tagName} (Closing: ${isClosing}, SelfClosing: ${isSelfClosing})`);
      if (tagName === 'InteractiveExample') {
        console.log('--- InteractiveExample Raw Token ---');
        console.log(token);
        console.log('------------------------------------');
      }
      if (count >= 50) break;
    }
  }
}

const fileContent = fs.readFileSync('C:/Users/nishu/workspace/wscs_bedrock/doc_replica_product_developer/doc_replica_fullstackdeveloper/backend/languages/python.md', 'utf-8');

const idx = fileContent.indexOf('# Python for AI Agents (Beginner to Advanced)');
if (idx !== -1) {
  const section = fileContent.substring(idx);
  parseMDXContent(section);
} else {
  console.log('Section not found!');
}
