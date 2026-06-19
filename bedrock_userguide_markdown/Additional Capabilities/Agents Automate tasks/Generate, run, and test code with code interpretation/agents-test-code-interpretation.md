

# Test code interpretation in Amazon Bedrock
<a name="agents-test-code-interpretation"></a>

Before you test code interpretation in Amazon Bedrock, make sure to prepare your agent to apply the changes you’ve just made.

With code interpretation enabled, when you start to test your agent, you can optionally attach files and choose how you want the files you attach to be used by code interpretation. Depending on your use case, you can ask code interpretation to use the information in the attached files to summarize the contents of the file and to answer queries about the file content during an interactive chat conversation. Or, you can ask code interpretation to analyze the content in the attached files and provide metrics and data visualization reports.

**Attach files**

To learn how to attach files for code interpretation, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To attach files for code interpretation,**

1. If you're not already in the agent builder, do the following:

   1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

   1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

   1. Choose **Edit in Agent Builder**

   1. Expand **Additional settings** and confirm that **Code Interpreter** is enabled.

   1. Make sure agent is prepared.

1. If test window is not open, choose **Test**.

1. In the bottom of the test window, select the paper clip icon to attach files.

1. In the **Attach files** page,

   1. 

**For **Choose function**, specify the following:**
      + If you are attaching files for the agent to use to answer your queries and summarize content, choose **Attach files to chat (faster)**.
      + If you are attaching files for code interpretation to analyze the content and provide metrics, choose **Attach files to code interpreter**.

   1. 

**For **Choose upload method**, choose from where you want to upload your files:**
      + If you are uploading from your computer, choose **Choose files** and select files to attach.
      + If you are uploading from Amazon S3, choose **Browse S3**, select files, choose **Choose**, and then choose **Add**.

1. Choose **Attach**.

------
#### [ API ]

To test code interpretation, send an [InvokeAgent](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_InvokeAgent.html) request (see link for request and response formats and field details) with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt).

**To attach files for agent to use for answering your queries and summarizing the content, specify the following fields:**


****  

| Field | Short description | 
| --- | --- | 
| name | Name of the attached file. | 
| sourceType | Location of the file to be attached. Specify s3 if your file is located in Amazon S3 bucket. Specify byte\_content if your file is located on your computer. | 
| S3Location | The S3 path where your file is located. Required if the sourceType is S3. | 
| mediaType | File type of the attached file.<br />**Supported input file types**: CSV, XLS, XLSX, YAML, JSON, DOC, DOCX, HTML, MD, TXT, and PDF  | 
| data | Base64 encoded string. Max file size 10MB. If you are using SDK, you just need to provide file byte content. AWS SDK automatically encodes strings to base64. | 
| useCase | How you want the attached files to be used. Valid values: CHAT \| CODE\_INTERPRETER | 

 The following example shows the general format for specifying the required fields to attach files to chat.

```
                  
"sessionState": {
        "promptSessionAttributes": {
            "string": "string"
        },
        "sessionAttributes": {
            "string": "string"
        },
        "files": [ 
            {
                "name": "banking_data", 
                "source": { 
                    "sourceType": "S3", 
                    "s3Location": 
                        "uri": "s3Uri" 
                    }
                },
                "useCase": "CHAT" 
            },
            {
                "name": "housing_stats.csv", 
                "source": { 
                    "sourceType": "BYTE_CONTENT", 
                    "byteContent": {
                        "mediaType": "text/csv", 
                        "data": "{{file byte content}}"
                    }
                },
                "useCase": "CHAT"
            }
        ]
    }
```

The following example shows the general format for specifying the required fields to attach files for code interpretation.

```
"sessionState": {
        "promptSessionAttributes": {
            "string": "string"
        },
        "sessionAttributes": {
            "string": "string"
        },
        "files": [ 
            {
                "name": "banking_data", 
                "source": { 
                    "sourceType": "S3",
                    "s3Location": {
                        "uri": "s3Uri" 
                    }
                },
                "useCase": "CODE_INTERPRETER" 
            },
            {
                "name": "housing_stats.csv", 
                "source": { 
                    "sourceType": "BYTE_CONTENT", 
                    "byteContent": {
             "mediaType": "text/csv", 
             "data": "{{file byte content}}" 
                    }
                },
                "useCase": "CODE_INTERPRETER"
            }
        ]
    }
```

------