

# Define function details for your agent's action groups in Amazon Bedrock
<a name="agents-action-function"></a>

When you create an action group in Amazon Bedrock, you can define function details to specify the parameters that the agent needs to invoke from the user. Function details consist of a list of parameters, defined by their name, data type (for a list of supported data types, see [ParameterDetail](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ParameterDetail.html)), and whether they are required. The agent uses these configurations to determine what information it needs to elicit from the user.

For example, you might define a function called **BookHotel** that contains parameters that the agent needs to invoke from the user to book a hotel for the user. You might define the following parameters for the function:


****  

| Parameter | Description | Type | Required | 
| --- | --- | --- | --- | 
| HotelName | The name of the hotel | string | Yes | 
| CheckinDate | The date to check in | string | Yes | 
| NumberOfNights | The number of nights to stay | integer | No | 
| Email | An email address to contact the user | string | Yes | 
| AllowMarketingEmails | Whether to allow promotional emails to be sent to the user | boolean | Yes | 

Defining this set of parameters would help the agent determine that it must minimally elicit the name of the hotel that the user wants to book, the check-in date, the user's email address, and whether they want to allow promotional emails to be sent to their email.

If the user says **"I want to book Hotel X for tomorrow"**, the agent would determine the parameters `HotelName` and `CheckinDate`. It would then follow up with the user on the remaining parameters with questions such as:
+ "What is your email address?"
+ "Do you want to allow the hotel to send you promotional emails?"

Once the agent determines all the required parameters, it then sends them to a Lambda function that you define to carry out the action or returns them in the response of the agent invocation.

To learn how to define a function while creating the action group, see [Add an action group to your agent in Amazon Bedrock](agents-action-add.md).