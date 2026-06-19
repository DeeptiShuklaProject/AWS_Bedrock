

# Deploy your guardrail
<a name="guardrails-deploy"></a>

When you're ready to deploy your guardrail to production, you create a version of it and invoke the version of the guardrail in your application. A version is a snapshot of your guardrail that you create at a point in time when you are iterating on the working draft of the guardrail. Create versions of your guardrail when you are satisfied with a set of configurations. 

You can use the test window (for more information, see [Test your guardrail](guardrails-test.md)) to compare how different versions of your guardrail perform when evaluating the input prompts and model responses, and generating controlled responses for the final output. When you use versions, you can switch between different configurations for your guardrail, and update your application with the most appropriate version for your use case.

The following topics discuss how to create a version of your guardrail when it's ready for deployment, view information about it, and delete it when you no longer want to use it.

**Note**  
Guardrail versions are not considered resources and do not have an ARN. IAM Policies that apply to a guardrail apply to all of its versions.

**Topics**
+ [Create a version of a guardrail](guardrails-versions-create.md)
+ [View information about guardrail versions](guardrails-versions-view.md)
+ [Delete a version of a guardrail](guardrails-versions-delete.md)