

# Anthropic
<a name="model-cards-anthropic"></a>

The following Anthropic models are available in Amazon Bedrock:


| **Model** | **Description** | 
| --- | --- | 
| [Claude Mythos 5](model-card-anthropic-claude-mythos-5.md) | Claude Mythos 5 is Anthropic's most capable model for cybersecurity and life sciences, including vulnerability discovery, drug design, and biodefense screening. | 
| [Claude Fable 5](model-card-anthropic-claude-fable-5.md) | Claude Fable 5 is Anthropic's next-generation model for complex knowledge work and coding, capable of sustained autonomous operation across multi-day tasks. | 
| [Claude Opus 4.8](model-card-anthropic-claude-opus-4-8.md) | Claude Opus 4.8 is an Anthropic Opus model optimized for coding, agents, and deeper reasoning in enterprise workflows. | 
| [Claude Opus 4.7](model-card-anthropic-claude-opus-4-7.md) | Claude Opus 4.7 is an Anthropic Opus model built for coding, enterprise workflows, and long-running agentic tasks. | 
| [Claude Mythos Preview](model-card-anthropic-claude-mythos-preview.md) | Claude Mythos Preview (gated research preview) is a new class of intelligence built for ambitious projects, and the world's best model for cybersecurity, autonomous coding, and long-running agents. | 
| [Claude Sonnet 4.6](model-card-anthropic-claude-sonnet-4-6.md) | Claude Sonnet 4.6 is a full upgrade of Anthropic's mid-tier model with improved coding, computer use, long-context reasoning, and agent planning with a 1M token context window. | 
| [Claude Opus 4.6](model-card-anthropic-claude-opus-4-6.md) | Claude Opus 4.6 is Anthropic's flagship model that plans more carefully, sustains agentic tasks longer, and operates reliably in massive codebases. | 
| [Claude Opus 4.5](model-card-anthropic-claude-opus-4-5.md) | Claude Opus 4.5 is Anthropic's model for coding, agents, and computer use with improvements for spreadsheets and long-running chats. | 
| [Claude Haiku 4.5](model-card-anthropic-claude-haiku-4-5.md) | Claude Haiku 4.5 is Anthropic's lightweight model optimized for speed and efficiency with strong coding and agent performance. | 
| [Claude Sonnet 4.5](model-card-anthropic-claude-sonnet-4-5.md) | Claude Sonnet 4.5 is Anthropic's model optimized for agents, coding, and computer use with significant improvements across all benchmarks. | 
| [Claude Opus 4.1](model-card-anthropic-claude-opus-4-1.md) | Claude Opus 4.1 is an upgrade to Anthropic's model with improved coding, reasoning, and agentic task capabilities. | 
| [Claude Sonnet 4](model-card-anthropic-claude-sonnet-4.md) | Claude Sonnet 4 is Anthropic's balanced model with strong coding and reasoning capabilities, improved instruction following, and extended thinking with tool use. | 
| [Claude 3.5 Haiku](model-card-anthropic-claude-3-5-haiku.md) | Claude 3.5 Haiku is Anthropic's next-generation fast model with improved coding and reasoning performance over Claude 3 Haiku at the same speed tier. | 
| [Claude 3 Haiku](model-card-anthropic-claude-3-haiku.md) | Claude 3 Haiku is Anthropic's fastest and most compact Claude 3 model, optimized for speed and efficiency in near-instant responses. | 

## Billing notes
<a name="model-cards-anthropic-billing-notes"></a>

The following billing behaviors apply specifically to Anthropic models on Amazon Bedrock:
+ **Refused requests (all Anthropic models on `bedrock-mantle`):** When a request is refused by a content classifier before inference begins, no input or output tokens are billed. Mid-stream refusals — where the classifier fires after output has begun streaming — are billed for tokens consumed before the block. Both refusal types return `stop_reason: "refusal"` in the response.