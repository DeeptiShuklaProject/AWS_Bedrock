

# Viewing and updating permissions in the execution role
<a name="permissions-executionrole-update"></a>

This topic covers how you can view and update your function's [execution role](lambda-intro-execution-role.md).

**Topics**
+ [Viewing a function's execution role](#view-execution-role)
+ [Updating a function's execution role](#update-execution-role)

## Viewing a function's execution role
<a name="view-execution-role"></a>

To view a function's execution role, use the Lambda console.

**To view a function's execution role (console)**

1. Open the [Functions page](https://console.aws.amazon.com/lambda/home#/functions) of the Lambda console.

1. Choose the name of a function.

1. Choose **Configuration**, and then choose **Permissions**.

1. Under **Execution role**, you can view the role that's currently being used as the function's execution role. For convenience, you can view all the resources and actions that the function can access under the **Resource summary** section. You can also choose a service from the dropdown list to see all permissions related to that service.

## Updating a function's execution role
<a name="update-execution-role"></a>

You can add or remove permissions from a function's execution role at any time, or configure your function to use a different role. If your function needs access to any other services or resources, you must add the necessary permissions to the execution role.

When you add permissions to your function, perform a trivial update to its code or configuration as well. This forces running instances of your function, which have outdated credentials, to stop and be replaced.

To update a function's execution role, you can use the Lambda console.

**To update a function's execution role (console)**

1. Open the [Functions page](https://console.aws.amazon.com/lambda/home#/functions) of the Lambda console.

1. Choose the name of a function.

1. Choose **Configuration**, and then choose **Permissions**.

1. Under **Execution role**, choose **Edit**.

1. If you want to update your function to use a different role as the execution role, choose the new role in the dropdown menu under **Existing role**.
**Note**  
If you want to update the permissions within an existing execution role, you can only do so in the AWS Identity and Access Management (IAM) console.

   If you want to create a new role to use as the execution role, choose **Create a new role from AWS policy templates** under **Execution role**. Then, enter a name for your new role under **Role name**, and specify any policies you want to attach to the new role under **Policy templates**.

1. Choose **Save**.