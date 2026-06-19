

# Optimize and migrate prompts in Amazon Bedrock
<a name="prompt-optimization-migration"></a>

Amazon Bedrock offers prompt optimization, a model migration and optimization tool that helps you get the best performance from foundation models. Amazon Bedrock provides two prompt optimization options. 
+ [Simple optimization](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management-optimize.html) performs a fast, heuristic rewrite of a single short prompt for one model.
+ [Advanced Prompt Optimization](https://docs.aws.amazon.com/bedrock/latest/userguide/advanced-prompt-optimization-how.html) (AdvPO) allows you to optimize your prompts for any model on Bedrock while comparing your original prompts to optimized prompts across up to 5 models simultaneously. 

  You can use this if you are migrating to a new model or just want to get better performance on your current model. If you are changing models, select your current model as a baseline and up to 4 other models. If you aren't changing models, just select your current model to see before and after optimization. The optimizer takes your prompt templates (up to 10 per job), and example user inputs for variable values (up to 100 per prompt template). It also requires ground truth answers and an evaluation metric to guide the optimization. It's even compatible with multimodal inputs such as jpeg, png, or PDF. You can provide an LLM-as-a-judge rubric, a Lambda function, or short natural language steering criteria. The evaluation steers the prompt optimization. The optimizer works in an evaluation-based feedback loop to optimize the prompt and resulting model responses. It outputs the original and final prompt templates with evaluation scores, cost estimates, and latency.

## Choose an optimization method
<a name="prompt-optimization-migration-choose"></a>


|  | Simple optimization | Advanced Prompt Optimization | 
| --- | --- | --- | 
| Use case | Basic single-prompt rewrite for short prompts | Flexible, iterative optimization where your evaluation steers the prompt rewriting, for model migration and performance tuning | 
| Best for | Short prompts (approximately 1k tokens or less) | Prompt templates of any length that fits in the model's context window | 
| Input | Single prompt text | Up to 10 prompt templates with evaluation samples, including multimodal | 
| Models | 1 model | Up to 5 models compared simultaneously | 
| Evaluation | None (heuristic rewrite) | Your choice: steering criteria, LLM-as-judge rubric, or custom Lambda function | 
| Output | Rewritten prompt (instant) | Optimized templates with evaluation scores, cost estimates, and latency per model | 
| Execution | Synchronous (seconds) | Asynchronous job (15 min to hours, depending on number of prompt templates and evaluation samples) | 
| Multimodal | No | Yes (images, PDFs) | 
| Model migration | Partial: can rewrite prompts, but no side by side comparison | Yes, compare current model against candidates side by side | 