

# Details about the mortgage processing flow
<a name="getting-started-mortgage-flow-details"></a>

The visual representation of the mortgage processing flow in the AWS Management Console is as follows:

![Mortgage processing flow.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/cloudformation/mortgage-processing-flow.png)


## Steps in the flow
<a name="getting-started-mortgage-flow-steps"></a>

The following steps occur in the flow:

1. The customer's financial information from the input is sent to the `loanCalculator` Lambda function, which calculates the customer's maximum affordable loan.

1. The output from the `loanCalculator` function (`maximumAffordableLoan`) and the `loanAmount` value from the input are sent to the condition node, which is then evaluated as follows:
   + If the `loanAmount` is greater than the `maximumAffordableLoan`, the `incomeDebt` prompt is triggered and a rejection letter for the loan is generated.
   + Otherwise, the customer's financial information is sent to the `mortgageProcessingAgent` by the `processApplication` prompt. The agent applies a loan calculator function, as well as a Multiple Listing Service (MLS) lookup function to look up a DynamoDB table and assess the customer's information with respect to the MLS property specified in the input. Furthermore, the agent looks up information from a knowledge base, which contains the Fannie Mae Selling Guide. The agent uses all this information to generate a response analyzing the customer's eligibility for the requested loan amount.