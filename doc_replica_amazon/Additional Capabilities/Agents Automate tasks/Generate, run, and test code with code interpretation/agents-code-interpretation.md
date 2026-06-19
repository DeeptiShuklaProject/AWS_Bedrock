

# Generate, run, and test code for your application by enabling code interpretation
<a name="agents-code-interpretation"></a>

The code interpretation enables your agent to generate, run, and troubleshoot your application code in a secure test environment. With code interpretation you can use the agent’s foundation model to generate code for implementing basic capabilities while you focus on building generative AI applications. 

You can perform the following tasks with code interpretation in Amazon Bedrock:
+ Understand user requests for specific tasks, generate code that can perform the tasks requested by the user , execute the code, and provide the result from the code execution.
+ Understand user’s generic queries, generate and run code to provide response to the user.
+ Generate code for performing analysis, visualization, and evaluation of the data.
+ Extract information from the files uploaded by the user, process the information and answer user queries. 
+ Generate code based on the interactive conversations with the user for rapid prototyping. 

By default, the maximum number of concurrently active code interpretation per session per AWS account is 25. This means , each AWS account can have up to 25 ongoing conversations with the agents at once using code interpreter.

The following are some of the use cases where code interpretation can help by generating and running the code within an Amazon Bedrock 

1. Analyzing financial transactions from a data file such as a .csv to determine if they resulted a profit or a loss. 

1. Converting date format, such as *14th March 2020* to standard API format `YYYY-MM-DD` for file formats such as .txt or .csv

1. Performing data analysis on a spreadsheet (XLS) to calculate metrics such as quarterly/yearly company revenues or population growth rate.

To use the code interpretation in Amazon Bedrock, perform the following steps, 
+ Enable code interpretation when you build your agent. Once you’ve enabled code interpretation, you can start to use it.
+ Start using code interpretation in Amazon Bedrock by providing prompts. For example you can ask “calculate the square root of pi to 127 digits”. Code interpretation will generate and run python code to provide a response.
+ You can also attach files. You can use the information in the files to ask questions and summarize or analyze data. You can attach the files from either your computer or from Amazon S3 bucket.

**Supported Regions**

Code Interpretation for Amazon Bedrock Agents is supported in the following Regions:


****  

| Region | 
| --- | 
| US East (N.Virginia) | 
| US West (Oregon) | 
| Europe (Frankfurt) | 

**File support**

With code interpretation, you can attach files and then use the attached files to ask questions and summarize or analyze data that’s based on the content of the attached files. 

You can attach a maximum of 5 files. The total size of all the files can be up to 10 MB.
+ **Supported input file types**: CSV, XLS, XLSX, YAML, JSON, DOC, DOCX, HTML, MD, TXT, and PDF 
+ **Supported output file types**: CSV, XLS, XLSX, YAML, JSON, DOC, DOCX, HTML, MD, TXT, PDF, and PNG 