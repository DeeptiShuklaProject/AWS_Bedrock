

# Differences in thinking across model versions
<a name="claude-messages-thinking-differences"></a>

The Messages API handles thinking differently across Claude 3.7 Sonnet and Claude 4 models, primarily in redaction and summarization behavior. The following table summarizes those differences.


| Feature | Claude 3.7 Sonnet | Claude 4 Models | 
| --- | --- | --- | 
| Thinking output | Returns the full thinking output | Returns summarized thinking | 
| Redaction handling | Uses `redacted_thinking` blocks | Redacts and encrypts full thinking, returned in a `signature` field | 
| Interleaved thinking | Not supported | Supported with a beta header | 