

# Evaluate the performance of Amazon Bedrock resources
<a name="evaluation"></a>

Use Amazon Bedrock evaluations to evaluate the performance and effectiveness of Amazon Bedrock models and knowledge bases, as well as models and Retrieval Augmented Generation (RAG) sources outside of Amazon Bedrock. Amazon Bedrock can compute performance metrics such as the semantic robustness of a model and the correctness of a knowledge base in retrieving information and generating responses. For model evaluations, you can also use a team of human workers to rate and provide their input for the evaluation.

Automatic evaluations, including evaluations that use Large Language Models (LLMs), produce computed scores and metrics that help you assess the effectiveness of a model and knowledge base. Human-based evaluations use a team of people who provide their ratings and preferences in relation to certain metrics.

**Overview: Programmatic model evaluation jobs**  
Programmatic model evaluation jobs allow you to quickly evaluate a model's ability to perform a task. You can either provide your own custom prompt dataset that you've tailored to a specific use case, or you can use an available built-in dataset. 

**Overview: Model evaluation jobs that use human workers**  
Model evaluation jobs that use human workers allow you to bring human input to the model evaluation process. They can be employees of your company or a group of subject-matter experts from your industry.

**Overview: Model evaluation jobs that use a judge model**  
Model evaluation jobs that use a judge model allow you to quickly evaluate a model's responses via using a second LLM. The second LLM scores the response and provides an explanation for each response.

**Overview of RAG evaluations that use Large Language Models (LLMs)**  
LLM-based evaluations compute performance metrics for the knowledge base. The metrics reveal if a RAG source or Amazon Bedrock Knowledge Base is able to retrieve highly relevant information and generate useful, appropriate responses. You provide a dataset that contains the prompts or user queries for evaluating how a knowledge base retrieves information and generates responses for those given queries. The dataset must also include ‘ground truth’ or the expected retrieved texts and responses for the queries so that the evaluation can check if your knowledge base is aligned with what’s expected.

Use the following topic to learn more about creating your first model evaluation job.

Model evaluation jobs support using the following types of Amazon Bedrock models:
+ Foundation models
+ Amazon Bedrock Marketplace models
+ Customized foundation models
+ Imported foundation models
+ Prompt routers
+ Models that you have purchased Provisioned Throughput

**Topics**
+ [Supported Regions and models for model evaluation](evaluation-support.md)
+ [Creating an automatic model evaluation job in Amazon Bedrock](evaluation-automatic.md)
+ [Creating a model evaluation job that use human workers in Amazon Bedrock](evaluation-human.md)
+ [Evaluate model performance using another LLM as a judge](evaluation-judge.md)
+ [Evaluate the performance of RAG sources using Amazon Bedrock evaluations](evaluation-kb.md)
+ [Required Cross Origin Resource Sharing (CORS) permissions on S3 buckets](model-evaluation-security-cors.md)
+ [Review model evaluation job reports and metrics in Amazon Bedrock](model-evaluation-report.md)
+ [Data management and encryption in Amazon Bedrock evaluation job](evaluation-data-management.md)
+ [CloudTrail management events in model evaluation jobs](cloudtrail-events-in-model-evaluations.md)