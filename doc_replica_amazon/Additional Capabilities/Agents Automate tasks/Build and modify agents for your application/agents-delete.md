

# Delete an agent
<a name="agents-delete"></a>

If you no longer need an agent, you can delete it at any time.

To learn how to delete an agent, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To delete an agent**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Agents** from the left navigation pane.

1. To delete an agent, choose the option button that's next to the agent you want to delete.

1. A dialog box appears warning you about the consequences of deletion. To confirm that you want to delete the agent, enter **delete** in the input field and then select **Delete**.

1. When deletion is complete, a success banner appears.

------
#### [ API ]

To delete an agent, send a [DeleteAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_DeleteAgent.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the `agentId`.

By default, the `skipResourceInUseCheck` parameter is `false` and deletion is stopped if the resource is in use. If you set `skipResourceInUseCheck` to `true`, the resource will be deleted even if the resource is in use.

```
    def delete_agent(self, agent_id):
        """
        Deletes an Amazon Bedrock agent.

        :param agent_id: The unique identifier of the agent to delete.
        :return: The response from Amazon Bedrock Agents if successful, otherwise raises an exception.
        """

        try:
            response = self.client.delete_agent(
                agentId=agent_id, skipResourceInUseCheck=False
            )
        except ClientError as e:
            logger.error(f"Couldn't delete agent. {e}")
            raise
        else:
            return response
```

For more information, see [Hello Amazon Bedrock Agents](bedrock-agent_example_bedrock-agent_Hello_section.md).

------