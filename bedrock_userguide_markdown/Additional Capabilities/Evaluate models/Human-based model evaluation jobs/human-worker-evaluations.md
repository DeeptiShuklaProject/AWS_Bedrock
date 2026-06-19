

# Manage a work team for human evaluations of models in Amazon Bedrock
<a name="human-worker-evaluations"></a>

For evaluation jobs that use human workers you need to have a work team. A work team is a group of workers that *you* choose. These can be employees of your company or a group of subject-matter experts from your industry.

**Worker notifications in Amazon Bedrock**  
When you create an evaluation job in Amazon Bedrock workers are notified of their assigned job *only* when you first add them to a work team
If you delete a worker from a work team during evaluation job creation, they will lose access to *all* evaluation jobs they have been assigned too.
For any new evaluation jobs that you assign to an existing human worker, you must notify them directly and provide them the URL to the worker portal. Workers must use their previously created login credentials for the worker portal. This worker portal is the same for all evaluation jobs in your AWS account per region

You can create a human work team or manage an existing one while setting up an evaluation job workers to a *Private workforce* that is managed by Amazon SageMaker Ground Truth. Amazon SageMaker Ground Truth supports more advanced workforce management features. To learn more about managing your workforce in Amazon SageMaker Ground Truth, see [Create and manage workforces](https://docs.aws.amazon.com/sagemaker/latest/dg/sms-workforce-management.html).

You can delete workers from a work team while setting up a new evaluation job. Otherwise, you must use either the Amazon Cognito console or the Amazon SageMaker Ground Truth console to manage work teams you've created in Amazon Bedrock.

If the IAM user, group, or role has the required permissions you will see existing private workforces and work teams you created in Amazon Cognito, Amazon SageMaker Ground Truth, or Amazon Augmented AI visible when you are creating an evaluation job that uses human workers.

Amazon Bedrock supports a maximum of 50 workers per work team.

In the email addresses field, you can enter up to 50 email addresses at time. To add more workers to your evaluation job use the Amazon Cognito console or the Ground Truth console. The addresses must be separated by a comma. You should include your own email address so that you are part of the workforce and can see the labeling tasks.

## Create instructions for human workers
<a name="human-worker-evaluation-instructions"></a>

Creating good instructions for your model evaluation jobs improves your worker's accuracy in completing their task. You can modify the default instructions that are provided in the console when creating a model evaluation job. The instructions are shown to the worker on the UI page where they complete their labeling task.

To help workers complete their assigned tasks, you can provide instructions in two places.

**Provide a good description for each evaluation and rating method**  
The descriptions should provide a succinct explanation of the metrics selected. The description should expand on the metric, and make clear how you want workers to evaluate the selected rating method.

**Provide your workers overall evaluation instructions**  
These instructions are shown on the same webpage where workers complete a task. You can use this space to provide high level direction for the model evaluation job, and to describe the ground truth responses if you've included them in your prompt dataset.