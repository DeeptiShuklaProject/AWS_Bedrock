

# Use `ListTags` with a CLI
<a name="example_lambda_ListTags_section"></a>

The following code examples show how to use `ListTags`.

------
#### [ CLI ]

**AWS CLI**  
**To retrieve the list of tags for a Lambda function**  
The following `list-tags` example displays the tags attached to the `my-function` Lambda function.  

```
aws lambda list-tags \
    --resource {{arn:aws:lambda:us-west-2:123456789012:function:my-function}}
```
Output:  

```
{
    "Tags": {
        "Category": "Web Tools",
        "Department": "Sales"
    }
}
```
For more information, see [Tagging Lambda Functions](https://docs.aws.amazon.com/lambda/latest/dg/tagging.html) in the *AWS Lambda Developer Guide*.  
+  For API details, see [ListTags](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lambda/list-tags.html) in *AWS CLI Command Reference*. 

------
#### [ PowerShell ]

**Tools for PowerShell V4**  
**Example 1: Retrieves the tags and their values currently set on the specified function.**  

```
Get-LMResourceTag -Resource "arn:aws:lambda:us-west-2:123456789012:function:MyFunction"
```
**Output:**  

```
Key        Value
---        -----
California Sacramento
Oregon     Salem
Washington Olympia
```
+  For API details, see [ListTags](https://docs.aws.amazon.com/powershell/v4/reference) in *AWS Tools for PowerShell Cmdlet Reference (V4)*. 

**Tools for PowerShell V5**  
**Example 1: Retrieves the tags and their values currently set on the specified function.**  

```
Get-LMResourceTag -Resource "arn:aws:lambda:us-west-2:123456789012:function:MyFunction"
```
**Output:**  

```
Key        Value
---        -----
California Sacramento
Oregon     Salem
Washington Olympia
```
+  For API details, see [ListTags](https://docs.aws.amazon.com/powershell/v5/reference) in *AWS Tools for PowerShell Cmdlet Reference (V5)*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Lambda with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.