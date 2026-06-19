

# Create a flow with a condition node
<a name="flows-ex-condition"></a>

The following image shows a flow with one condition node returns one of three possible values based on the condition that is fulfilled:

![Example of using a condition node with two conditions.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/flows/flows-condition.png)


**To build and test this flow in the console:**

1. Create a flow by following the instructions at [Create your first flow in Amazon Bedrock](flows-get-started.md).

1. Delete the **Prompt** node in the center pane.

1. Set up the condition node by doing the following:

   1. From the **Flow builder** left pane, select the **Nodes** tab.

   1. Drag a **Condition** node into your flow in the center pane.

   1. Select the **Configure** tab in the **Flow builder** pane.

   1. Expand the **Inputs** section. Configure the inputs as follows:  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/flows-ex-condition.html)

      This configuration means that the condition node expects a JSON object that contains the fields `retailPrice`, `marketPrice`, and `type`.

   1. Configure the conditions by doing the following:

      1. In the **Conditions** section, optionally change the name of the condition. Then add the following condition in the **Condition** text box: **(retailPrice > 10) and (type == "produce")**.

      1. Add a second condition by choosing **Add condition**. Optionally change the name of the second condition. Then add the following condition in the **Condition** text box: **(retailPrice < marketPrice)**.

1. Choose the **Flow input** node and select the **Configure** tab. Select **Object** as the **Type**. This means that flow invocation will expect to receive a JSON object.

1. Add flow output nodes so that you have three in total. Configure them as follows in the **Configure** tab of the **Flow builder** pane of each flow output node:

   1. Set the input type of the first flow output node as **String** and the expression as **$.data.action[0]** to return the first value in the array in the `action` field of the incoming object.

   1. Set the input type of the second flow output node as **String** and the expression as **$.data.action[1]** to return the second value in the array in the `action` field of the incoming object.

   1. Set the input type of the third flow output node as **String** and the expression as **$.data.action[2]** to return the third value in the array in the `action` field of the incoming object.

1. Connect the first condition to the first flow output node, the second condition to the second flow output node, and the default condition to the third flow output node.

1. Connect the inputs and outputs in all the nodes to complete the flow by doing the following:

   1. Drag a connection from the output node of the **Flow input** node to the **retailPrice** input in the condition node.

   1. Drag a connection from the output node of the **Flow input** node to the **marketPrice** input in the condition node.

   1. Drag a connection from the output node of the **Flow input** node to the **type** input in the condition node.

   1. Drag a connection from the output of the **Flow input** node to the **document** input in each of the three output nodes.

1. Choose **Save** to save your flow. Your flow should now be prepared for testing.

1. Test your flow by entering the following JSON objects is the **Test flow** pane on the right. Choose **Run** for each input:

   1. The following object fulfills the first condition (the `retailPrice` is more than 10 and the `type` is "produce") and returns the first value in `action` ("don't buy"):

      ```
      {
          "retailPrice": 11, 
          "marketPrice": 12, 
          "type": "produce", 
          "action": ["don't buy", "buy", "undecided"]
      }
      ```
**Note**  
Even though both the first and second conditions are fulfilled, the first condition takes precedence since it comes first.

   1. The following object fulfills the second condition (the `retailPrice` is less than the `marketPrice`) and returns the second value in `action` ("buy"):

      ```
      {
          "retailPrice": 11, 
          "marketPrice": 12, 
          "type": "meat", 
          "action": ["don't buy", "buy", "undecided"]
      }
      ```

   1. The following object fulfills neither the first condition (the `retailPrice` is more than 10, but the `type` is not "produce") nor the second condition (the `retailPrice` isn't less than the `marketPrice`), so the third value in `action` ("undecided") is returned:

      ```
      {
          "retailPrice": 11, 
          "marketPrice": 11, 
          "type": "meat", 
          "action": ["don't buy", "buy", "undecided"]
      }
      ```