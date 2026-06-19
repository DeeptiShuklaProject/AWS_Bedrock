

# Enhance model responses with model reasoning
<a name="inference-reasoning"></a>

Some foundation models are able to perform model reasoning, where they are able to take a larger, complex task and break it down into smaller, simpler steps. This process is often referred to as chain of thought (CoT) reasoning. Chain of thought reasoning can often improve model accuracy by giving the model a chance to think before it responds. Model reasoning is most useful for task such as multi-step analysis, math problems, and complex reasoning tasks. 

For example, in tackling a mathematical word problem, the model can first identify the relevant variables, then construct equations based on the given information, and finally solve those equations to reach the solution. This strategy not only minimizes errors but also makes the reasoning process more transparent and easier to follow, thereby enhancing the quality of foundation model's output.

Model reasoning is not necessary for all tasks and does come with additional overhead, including increased latency and output tokens. Simple tasks that don't need additional explanations are not good candidates for CoT reasoning.

Note that not all models allow you to configure the number of output tokens that are allocated for model reasoning.

To see which models support reasoning, please visit [models at a glance](model-cards.md) and choose the model you are interested in.