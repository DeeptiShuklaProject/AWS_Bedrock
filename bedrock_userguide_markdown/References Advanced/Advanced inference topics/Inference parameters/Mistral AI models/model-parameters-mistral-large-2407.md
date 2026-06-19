

# Mistral AI Large (24.07) parameters and inference
<a name="model-parameters-mistral-large-2407"></a>

The Mistral AI chat completion API lets you create conversational applications. You can also use the Amazon Bedrock Converse API with this model. You can use tools to make function calls.

**Tip**  
You can use the Mistral AI chat completion API with the base inference operations ([InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) or [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html)). However, we recommend that you use the Converse API to implement messages in your application. The Converse API provides a unified set of parameters that work across all models that support messages. For more information, see [Inference using Converse API](conversation-inference.md).

Mistral AI models are available under the [Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0.txt). For more information about using Mistral AI models, see the [Mistral AI documentation](https://docs.mistral.ai/).

**Topics**
+ [Supported models](#mistral-supported-models-chat-completion)
+ [Request and Response Examples](#model-parameters-mistral-large-2407-request-response)

## Supported models
<a name="mistral-supported-models-chat-completion"></a>

You can use following Mistral AI models with the code examples on this page..
+ Mistral Large 2 (24.07)

You need the model ID for the model that you want to use. To get the model ID, see [Supported foundation models in Amazon Bedrock](models-supported.md). 

## Request and Response Examples
<a name="model-parameters-mistral-large-2407-request-response"></a>

------
#### [ Request ]

Mistral AI Large (24.07) invoke model example. 

```
import boto3 
import json

bedrock = session.client('bedrock-runtime', 'us-west-2') 
response = bedrock.invoke_model( 
        modelId='mistral.mistral-large-2407-v1:0', 
        body=json.dumps({
            'messages': [ 
                { 
                    'role': 'user', 
                    'content': 'which llm are you?' 
                } 
             ], 
         }) 
       ) 

print(json.dumps(json.loads(response['body']), indent=4))
```

------
#### [ Converse ]

Mistral AI Large (24.07) converse example. 

```
import boto3 
import json

bedrock = session.client('bedrock-runtime', 'us-west-2')
response = bedrock.converse( 
    modelId='mistral.mistral-large-2407-v1:0', 
    messages=[ 
        { 
            'role': 'user', 
            'content': [ 
                { 
                    'text': 'which llm are you?' 
                } 
             ] 
          } 
     ] 
  ) 

print(json.dumps(json.loads(response['body']), indent=4))
```

------
#### [ invoke\_model\_with\_response\_stream ]

Mistral AI Large (24.07) invoke\_model\_with\_response\_stream example. 

```
import boto3 
import json

bedrock = session.client('bedrock-runtime', 'us-west-2')
response = bedrock.invoke_model_with_response_stream(
    "body": json.dumps({
        "messages": [{"role": "user", "content": "What is the best French cheese?"}],
        }),
        "modelId":"mistral.mistral-large-2407-v1:0"
)

stream = response.get('body')
if stream:
        for event in stream:
            chunk=event.get('chunk')
            if chunk:
                chunk_obj=json.loads(chunk.get('bytes').decode())
                print(chunk_obj)
```

------
#### [ converse\_stream ]

Mistral AI Large (24.07) converse\_stream example. 

```
import boto3 
import json

bedrock = session.client('bedrock-runtime', 'us-west-2')
mistral_params = {
    "messages": [{
            "role": "user","content": [{"text": "What is the best French cheese? "}]
         }],
            "modelId":"mistral.mistral-large-2407-v1:0",
        }
    response = bedrock.converse_stream(**mistral_params)
    stream = response.get('stream')
    if stream:
        for event in stream:

            if 'messageStart' in event:
                print(f"\nRole: {event['messageStart']['role']}")

            if 'contentBlockDelta' in event:
                print(event['contentBlockDelta']['delta']['text'], end="")

            if 'messageStop' in event:
                print(f"\nStop reason: {event['messageStop']['stopReason']}")

            if 'metadata' in event:
                metadata = event['metadata']
                if 'usage' in metadata:
                    print("\nToken usage ... ")
                    print(f"Input tokens: {metadata['usage']['inputTokens']}")
                    print(
                        f":Output tokens: {metadata['usage']['outputTokens']}")
                    print(f":Total tokens: {metadata['usage']['totalTokens']}")
                if 'metrics' in event['metadata']:
                    print(
                        f"Latency: {metadata['metrics']['latencyMs']} milliseconds")
```

------
#### [ JSON Output ]

Mistral AI Large (24.07) JSON output example. 

```
import boto3 
import json

bedrock = session.client('bedrock-runtime', 'us-west-2')
mistral_params = {
        "body": json.dumps({
            "messages": [{"role": "user", "content": "What is the best French meal? Return the name and the ingredients in short JSON object."}]
        }),
        "modelId":"mistral.mistral-large-2407-v1:0",
    }
response = bedrock.invoke_model(**mistral_params)

body = response.get('body').read().decode('utf-8')
print(json.loads(body))
```

------
#### [ Tooling ]

Mistral AI Large (24.07) tools example. 

```
data = {
    'transaction_id': ['T1001', 'T1002', 'T1003', 'T1004', 'T1005'],
    'customer_id': ['C001', 'C002', 'C003', 'C002', 'C001'],
    'payment_amount': [125.50, 89.99, 120.00, 54.30, 210.20],
    'payment_date': ['2021-10-05', '2021-10-06', '2021-10-07', '2021-10-05', '2021-10-08'],
    'payment_status': ['Paid', 'Unpaid', 'Paid', 'Paid', 'Pending']
}

# Create DataFrame
df = pd.DataFrame(data)


def retrieve_payment_status(df: data, transaction_id: str) -> str:
    if transaction_id in df.transaction_id.values: 
        return json.dumps({'status': df[df.transaction_id == transaction_id].payment_status.item()})
    return json.dumps({'error': 'transaction id not found.'})

def retrieve_payment_date(df: data, transaction_id: str) -> str:
    if transaction_id in df.transaction_id.values: 
        return json.dumps({'date': df[df.transaction_id == transaction_id].payment_date.item()})
    return json.dumps({'error': 'transaction id not found.'})

tools = [
    {
        "type": "function",
        "function": {
            "name": "retrieve_payment_status",
            "description": "Get payment status of a transaction",
            "parameters": {
                "type": "object",
                "properties": {
                    "transaction_id": {
                        "type": "string",
                        "description": "The transaction id.",
                    }
                },
                "required": ["transaction_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "retrieve_payment_date",
            "description": "Get payment date of a transaction",
            "parameters": {
                "type": "object",
                "properties": {
                    "transaction_id": {
                        "type": "string",
                        "description": "The transaction id.",
                    }
                },
                "required": ["transaction_id"],
            },
        },
    }
]

names_to_functions = {
    'retrieve_payment_status': functools.partial(retrieve_payment_status, df=df),
    'retrieve_payment_date': functools.partial(retrieve_payment_date, df=df)
}



test_tool_input = "What's the status of my transaction T1001?"
message = [{"role": "user", "content": test_tool_input}]


def invoke_bedrock_mistral_tool():
   
    mistral_params = {
        "body": json.dumps({
            "messages": message,
            "tools": tools           
        }),
        "modelId":"mistral.mistral-large-2407-v1:0",
    }
    response = bedrock.invoke_model(**mistral_params)
    body = response.get('body').read().decode('utf-8')
    body = json.loads(body)
    choices = body.get("choices")
    message.append(choices[0].get("message"))

    tool_call = choices[0].get("message").get("tool_calls")[0]
    function_name = tool_call.get("function").get("name")
    function_params = json.loads(tool_call.get("function").get("arguments"))
    print("\nfunction_name: ", function_name, "\nfunction_params: ", function_params)
    function_result = names_to_functions[function_name](**function_params)

    message.append({"role": "tool", "content": function_result, "tool_call_id":tool_call.get("id")})
   
    new_mistral_params = {
        "body": json.dumps({
                "messages": message,
                "tools": tools           
        }),
        "modelId":"mistral.mistral-large-2407-v1:0",
    }
    response = bedrock.invoke_model(**new_mistral_params)
    body = response.get('body').read().decode('utf-8')
    body = json.loads(body)
    print(body)
invoke_bedrock_mistral_tool()
```

------