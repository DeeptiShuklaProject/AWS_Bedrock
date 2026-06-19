

# Delete an alias of an agent in Amazon Bedrock
<a name="agents-alias-delete"></a>

To learn how to delete an alias of an agent, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To delete an alias**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

1. To choose the alias for deletion, in the **Aliases** section, choose the option button next to the alias that you want to delete.

1. Choose **Delete**.

1. A dialog box appears warning you about the consequences of deletion. To confirm that you want to delete the alias, enter **delete** in the input field and choose **Delete**.

1. A banner appears to inform you that the alias is being deleted. When deletion is complete, a success banner appears.

------
#### [ API ]

To delete an alias of an agent, send a [DeleteAgentAlias](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_DeleteAgentAlias.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). By default, the `skipResourceInUseCheck` parameter is `false` and deletion is stopped if the resource is in use. If you set `skipResourceInUseCheck` to `true`, the resource will be deleted even if the resource is in use.

```
    def delete_agent_alias(self, agent_id, agent_alias_id):
        """
        Deletes an alias of an Amazon Bedrock agent.

        :param agent_id: The unique identifier of the agent that the alias belongs to.
        :param agent_alias_id: The unique identifier of the alias to delete.
        :return: The response from Amazon Bedrock Agents if successful, otherwise raises an exception.
        """

        try:
            response = self.client.delete_agent_alias(
                agentId=agent_id, agentAliasId=agent_alias_id
            )
        except ClientError as e:
            logger.error(f"Couldn't delete agent alias. {e}")
            raise
        else:
            return response
```

For more information, see [Hello Amazon Bedrock Agents](bedrock-agent_example_bedrock-agent_Hello_section.md).

------