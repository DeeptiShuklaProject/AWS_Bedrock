

# Define actions in the action group
<a name="action-define"></a>

You can define action groups in one of the following ways (you can use different methods for different action groups):
+ [Set up an OpenAPI schema](agents-api-schema.md) with descriptions, structure, and parameters that define each action in the action group as an API operation. With this option, you can define actions more explicitly and map them to API operations in your system. You add the API schema to the action group in one of the following ways:
  + Upload the schema that you create to an Amazon Simple Storage Service (Amazon S3) bucket.
  + Write the schema in the inline OpenAPI schema editor in the AWS Management Console when you add the action group. This option is only available after the agent that the action group belongs to has already been created.
+ [Set up function details](agents-action-function.md) with the parameters that the agent needs to elicit from the user. With this option, you can simplify the action group creation process and set up the agent to elicit a set of parameters that you define. You can then pass the parameters on to your application and customize how to use them to carry out the action in your own systems.

Continuing the example above, you can define the `CreateBooking` action in one of the following ways:
+ Using an API schema, `CreateBooking` could be an API operation with a request body that includes fields such as `HotelName`, `LengthOfStay`, and `UserEmail` and a response body that returns a `BookingId`.
+ Using function details, `CreateBooking` could be a function defined with parameters such as `HotelName`, `LengthOfStay`, and `UserEmail`. After the values of these parameters are elicited from the user by your agent, you can then pass them to your systems.

When your agent interacts with the user, it will determine which action within an action group it needs to invoke. The agent will then elicit the parameters and other information that is necessary to complete the API request or that are marked as *required* for the function.

Select a topic to learn how to define an action group with different methods.

**Topics**
+ [Define function details for your agent's action groups in Amazon Bedrock](agents-action-function.md)
+ [Define OpenAPI schemas for your agent's action groups in Amazon Bedrock](agents-api-schema.md)