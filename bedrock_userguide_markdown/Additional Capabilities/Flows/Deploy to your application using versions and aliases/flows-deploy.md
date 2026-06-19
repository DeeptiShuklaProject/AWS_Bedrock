

# Deploy a flow to your application using versions and aliases
<a name="flows-deploy"></a>

When you first create a flow, a working draft version (`DRAFT`) and a test alias (`TSTALIASID`) that points to the working draft version are created. When you make changes to your flow, the changes apply to the working draft, and so it is the latest version of your flow. You iterate on your working draft until you're satisfied with the behavior of your flow. Then, you can set up your flow for deployment by creating *versions* of your flow.

A *version* is a snapshot that preserves the resource as it exists at the time it was created. You can continue to modify the working draft and create versions of your flow as necessary. Amazon Bedrock creates versions in numerical order, starting from 1. Versions are immutable because they act as a snapshot of your flow at the time you created it. To make updates to a flow that you've deployed to production, you must create a new version from the working draft and make calls to the alias that points to that version.

To deploy your flow, you must create an *alias* that points to a version of your flow. Then, you make `InvokeFlow` requests to that alias. With aliases, you can switch efficiently between different versions of your flow without keeping track of the version. For example, you can change an alias to point to a previous version of your flow if there are changes that you need to revert quickly.

The following topics describe how to create versions and aliases of your flow.

**Topics**
+ [Create a version of a flow in Amazon Bedrock](flows-version-create.md)
+ [View information about versions of flows in Amazon Bedrock](flows-version-view.md)
+ [Delete a version of a flow in Amazon Bedrock](flows-version-delete.md)
+ [Create an alias of a flow in Amazon Bedrock](flows-alias-create.md)
+ [View information about aliases of flows in Amazon Bedrock](flows-alias-view.md)
+ [Modify an alias of a flow in Amazon Bedrock](flows-alias-modify.md)
+ [Delete an alias of a flow in Amazon Bedrock](flows-alias-delete.md)