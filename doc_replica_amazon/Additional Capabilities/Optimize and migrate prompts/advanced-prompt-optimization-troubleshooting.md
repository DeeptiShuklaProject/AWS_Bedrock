

# Troubleshooting
<a name="advanced-prompt-optimization-troubleshooting"></a>


| Error | Cause | Fix | 
| --- | --- | --- | 
| No inference API is accessible for model | Model access not enabled or IAM permission missing | Enable model access in Bedrock console; verify IAM policy includes bedrock:InvokeModelWithResponseStream | 
| Input file is empty | S3 object has 0 bytes | Verify the input JSONL file has content | 
| File is not valid JSONL | Malformed JSON in input file | Validate each line is valid JSON | 
| AccessDenied on S3 | IAM role lacks S3 permissions | Add s3:GetObject for input path and s3:PutObject for output path | 
| ValidationException: multiple evaluation methods | Provided both steeringCriteria AND customLLMJConfig or Lambda | Use only ONE evaluation method per template | 
| ValidationException: missing label | Missing customEvaluationMetricLabel when using LLMJ or Lambda | Add the customEvaluationMetricLabel field | 
| Silent failure: inputVariables | Multiple keys in one inputVariables object | Use one key per object in the array | 
| ValidationException: placeholder mismatch | inputVariables keys don't match {{placeholders}} in template | Ensure keys exactly match placeholder names | 
| ValidationException: wrong bracket syntax | Used {variable} instead of {{variable}} | Use double curly brackets | 