const fs = require('fs');

const content = fs.readFileSync("c:\\Users\\nishu\\workspace\\wscs_bedrock\\doc_replica_product_developer\\doc_replica_fullstackdeveloper\\backend\\languages\\go.md", 'utf8');

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

const nodes = parseMDXContent(content);

// Let's filter nodes to find InteractiveExample nodes
function findInteractiveExample(nodeList) {
  const result = [];
  for (const node of nodeList) {
    if (node.type === 'InteractiveExample') {
      result.push(node);
    }
    if (node.children && node.children.length > 0) {
      result.push(...findInteractiveExample(node.children));
    }
  }
  return result;
}

const examples = findInteractiveExample(nodes);
console.log(`Found ${examples.length} InteractiveExample nodes:`);
console.log(JSON.stringify(examples, null, 2));
