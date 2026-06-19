

# Delete a RAG evaluation job in Amazon Bedrock
<a name="knowledge-base-evaluation-delete"></a>

You can delete a RAG evaluation job that you no longer want to use.

You cannot delete a knowledge base evaluation job with a status that is currently in progress of being created. You can, however, [stop the creation of a knowledge base evaluation job](knowledge-base-evaluation-stop.md).

If you delete a knowledge base evaluation job, it doesn’t automatically delete your Amazon S3 bucket that stores your prompts dataset and the bucket or directory that stores the results of the evaluation. Your IAM role for the evaluation job is also not automatically deleted.

The following example shows you how to delete a knowledge base evaluation job using the AWS CLI.

*AWS Command Line Interface*

```
aws bedrock batch-delete-evaluation-job \
 --job-identifiers '["arn:aws:bedrock:<region>:<account-id>:evaluation-job/<job-id>"]'
```