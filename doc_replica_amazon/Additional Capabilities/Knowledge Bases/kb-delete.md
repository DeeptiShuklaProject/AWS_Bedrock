

# Delete an Amazon Bedrock knowledge base
<a name="kb-delete"></a>

You can delete or remove a knowledge base that you no longer use or need. When you delete a knowledge base, you should also carry out the following actions to fully delete all resources associated with the knowledge base.
+ Dissociate the knowledge base from any agents it's associated with.
+ Delete the vector store itself for your knowledge base.

**Note**  
The default `dataDeletionPolicy` on a newly created data source is "Delete", unless otherwise specified during data source creation. The policy applies when you delete a knowledge base or data source resource. You can update the policy to "Retain" data from your data source that's converted into vector embeddings. Note that the **vector store itself is not deleted** if you delete a knowledge base or data source resource.

Choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To delete a knowledge base**

1. Before the following steps, make sure to delete the knowledge base from any agents that it's associated with. To do this, carry out the following steps:

   1. From the left navigation pane, select **Agents**.

   1. Choose the **Name** of the agent that you want to delete the knowledge base from.

   1. A red banner appears to warn you to delete the reference to the knowledge base, which no longer exists, from the agent.

   1. Select the radio button next to the knowledge base that you want to remove. Select **More** and then choose **Delete**.

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. In the left navigation pane, choose **Knowledge bases**.

1. Choose a knowledge base or select the radio button next to a knowledge base. Then choose **Delete**.

1. Review the warnings for deleting a knowledge base. If you accept these conditions, enter **delete** in the input box and select **Delete** to confirm.
**Note**  
The **vector store itself is not deleted**, only the data. You can use the vector store's console or SDK to delete the vector store. Make sure to also check any Amazon Bedrock agents that you use with your knowledge base.

------
#### [ API ]

To delete the knowledge base, send a [DeleteKnowledgeBase](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_DeleteKnowledgeBase.html) request with a [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt).

You must also disassociate the knowledge base from any agents that it's associated with by making a [DisassociateAgentKnowledgeBase](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_DisassociateAgentKnowledgeBase.html) request with a [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt).

You must also delete the vector store itself by using the vector store's console or SDK to delete the vector store.

------