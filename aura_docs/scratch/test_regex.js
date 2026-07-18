const tagRegex = /(<\/?[A-Z][A-Za-z0-9_]*(?:\s+[a-zA-Z0-9_-]+=(?:"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|\[[^\]]*\]|{(?:[^{}]|(?:{[^{}]*}))*}|{[^}]+}|\d+|true|false))*?\s*\/?>)/g;

const tag = `<InteractiveExample 
  initialCode="prompt_input = \\"Search for AWS Bedrock pricing\\"\\nsession_ttl_seconds = 28800\\nprint(f'Prompt: {prompt_input}')\\nprint(f'Session TTL: {session_ttl_seconds}s'" 
  instruction="Run this interactive python example and see the console output."
/>`;

console.log('Matches:', tag.match(tagRegex));
