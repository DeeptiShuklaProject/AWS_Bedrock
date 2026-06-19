

# End-to-end workflow
<a name="bedrock-marketplace-end-to-end-workflow"></a>

After you've set up Amazon Bedrock Marketplace, you can use the following example code in your end-to-end workflow. If you need more context, you can read the sections that follow the code.

```
from botocore.exceptions import ClientError
import pprint
from datetime import datetime
import json
import time
import sys
import boto3
import argparse

SM_HUB_NAME = 'SageMakerPublicHub'
DELIMITER = "\n\n\n\n================================================================================================"


class Bedrock:
    def __init__(self, region_name) -> None:
        self.region_name = region_name
        self.boto3_session = boto3.session.Session()
        self.sagemaker_client = self.boto3_session.client(
            service_name='sagemaker',
            region_name=self.region_name,
        )

        self.bedrock_client = self.boto3_session.client(
            service_name='bedrock',
            region_name=self.region_name
        )
        self.endpoint_paginator = self.bedrock_client.get_paginator('list_marketplace_model_endpoints')
        self.bedrock_runtime_client = self.boto3_session.client(
            service_name='bedrock-runtime',
            region_name=self.region_name)

    def list_models(self):
        SM_RESPONSE_FIELD_NAME = 'HubContentSummaries'
        SM_HUB_CONTENT_TYPE = 'Model'

        response = self.sagemaker_client.list_hub_contents(
            MaxResults=100,
            HubName=SM_HUB_NAME,
            HubContentType=SM_HUB_CONTENT_TYPE
        )

        all_models = Bedrock.extract_bedrock_models(response[SM_RESPONSE_FIELD_NAME])

        while ("NextToken" in response) and response["NextToken"]:
            response = self.sagemaker_client.list_hub_contents(
                MaxResults=100,
                HubName=SM_HUB_NAME,
                HubContentType=SM_HUB_CONTENT_TYPE,
                NextToken=response['NextToken']
            )
            extracted_models = Bedrock.extract_bedrock_models(response[SM_RESPONSE_FIELD_NAME])
            if not extracted_models:
                # Bedrock enabled models always appear first, therefore can return when results are empty.
                return all_models
            all_models.extend(extracted_models)
            time.sleep(1)
        return all_models

    def describe_model(self, hub_name: str, hub_content_name: str):
        return self.sagemaker_client.describe_hub_content(
            HubName=hub_name,
            HubContentType='Model',
            HubContentName=hub_content_name
        )

    def list_endpoints(self):
        for response in self.endpoint_paginator.paginate():
            for endpoint in response['marketplaceModelEndpoints']:
                yield endpoint

    def list_endpoints_for_model(self, hub_content_arn: str):
        for response in self.endpoint_paginator.paginate(
                modelSourceEquals=hub_content_arn):
            for endpoint in response['marketplaceModelEndpoints']:
                yield endpoint

    # acceptEula needed only for gated models
    def create_endpoint(self, model, endpoint_config, endpoint_name: str, tags = []):
        model_arn = model['HubContentArn']
        if self._requires_eula(model=model):
            return self.bedrock_client.create_marketplace_model_endpoint(
                modelSourceIdentifier=model_arn,
                endpointConfig=endpoint_config,
                endpointName=endpoint_name,
                acceptEula=True,
                tags=tags
            )
        else:
            return self.bedrock_client.create_marketplace_model_endpoint(
                modelSourceIdentifier=model_arn,
                endpointConfig=endpoint_config,
                endpointName=endpoint_name,
                tags=tags
            )

    def delete_endpoint(self, endpoint_arn: str):
        return self.bedrock_client.delete_marketplace_model_endpoint(endpointArn=endpoint_arn)

    def describe_endpoint(self, endpoint_arn: str):
        return self.bedrock_client.get_marketplace_model_endpoint(endpointArn=endpoint_arn)['marketplaceModelEndpoint']

    def update_endpoint(self, endpoint_arn: str, endpoint_config):
        return self.bedrock_client.update_marketplace_model_endpoint(endpointArn=endpoint_arn,
                                                                 endpointConfig=endpoint_config)

    def register_endpoint(self, endpoint_arn: str, model_arn: str):
        return self.bedrock_client.register_marketplace_model_endpoint(endpointIdentifier=endpoint_arn,
                                                                       modelSourceIdentifier=model_arn)['marketplaceModelEndpoint']['endpointArn']

    def deregister_endpoint(self, endpoint_arn: str):
        return self.bedrock_client.deregister_marketplace_model_endpoint(endpointArn=endpoint_arn)

    def invoke(self, endpoint_arn: str, body):
        response = self.bedrock_runtime_client.invoke_model(modelId=endpoint_arn, body=body,
                                                            contentType='application/json')
        return json.loads(response["body"].read())

    def invoke_with_stream(self, endpoint_arn: str, body):
        return self.bedrock_runtime_client.invoke_model_with_response_stream(modelId=endpoint_arn, body=body)

    def converse(self, endpoint_arn: str, conversation):
        return self.bedrock_runtime_client.converse(modelId=endpoint_arn, messages=conversation)

    def converse_with_stream(self, endpoint_arn: str, conversation):
        return self.bedrock_runtime_client.converse_stream(modelId=endpoint_arn, messages=conversation,
                                                           inferenceConfig={"maxTokens": 4096, "temperature": 0.5,
                                                                            "topP": 0.9})

    def wait_for_endpoint(self, endpoint_arn: str):
        endpoint = self.describe_endpoint(endpoint_arn=endpoint_arn)
        while endpoint['endpointStatus'] in ['Creating', 'Updating']:
            print(
                f"Endpoint {endpoint_arn} status is still {endpoint['endpointStatus']}. Waiting 10 seconds before continuing...")
            time.sleep(10)
            endpoint = self.describe_endpoint(endpoint_arn=endpoint_arn)
        print(f"Endpoint status: {endpoint['status']}")

    def _requires_eula(self, model):
        if 'HubContentDocument' in model:
            hcd = json.loads(model['HubContentDocument'])
            if ('HostingEulaUri' in hcd) and hcd['HostingEulaUri']:
                return True
        return False

    @staticmethod
    def extract_bedrock_models(hub_content_summaries):
        models = []
        for content in hub_content_summaries:
            if ('HubContentSearchKeywords' in content) and (
                    '@capability:bedrock_console' in content['HubContentSearchKeywords']):
                print(f"ModelName: {content['HubContentDisplayName']}, modelSourceIdentifier: {content['HubContentArn']}")
                models.append(content)
        return models


def run_script(sagemaker_execution_role: str, region: str):
    # Script params
    model_arn = 'arn:aws:sagemaker:{{AWS Region}}:aws:hub-content/SageMakerPublicHub/Model/{{example-model-name}}/{{hub-content-arn}}'
    model_name = '{{example-model-name}}'
    sample_endpoint_name = f'test-ep-{datetime.now().strftime("%Y-%m-%d%H%M%S")}'
    sagemaker_execution_role = sagemaker_execution_role
    conversation = [
        {
            "role": "user",
            "content": [
                {
                    "text": "whats the best park in the US?"
                }
            ]
        }
    ]

    bedrock = Bedrock(region_name=region)

    ###
    ###  Model discovery
    ###

    # List all models - no new Bedrock Marketplace API here. Uses existing SageMaker APIs
    print(DELIMITER)
    print("All models:")
    all_models = bedrock.list_models()
    # Describe a model - no new Bedrock Marketplace API here. Uses existing SageMaker APIs
    # Examples:
    #     bedrock.describe_model("SageMakerPublicHub", "huggingface-llm-amazon-mistrallite")
    #     bedrock.describe_model("SageMakerPublicHub", "huggingface-llm-gemma-2b-instruct")
    print(DELIMITER)
    print(f'Describing model: {model_name}')
    model = bedrock.describe_model(SM_HUB_NAME, model_name)
    pprint.pprint(model)

    ## If customer wants to use a proprietary model, they need to subscribe to it first
    ## If customer wants to use a gated model, they need to accept EULA. Note: EULA Acceptance is on-creation, and needs
    ##     to be provided on every call. Cannot un-accept a EULA
    ## If customer wants to use an open weight model, they can proceed to deploy

    ###
    ###  Model deployment to create endpoints
    ###

    # # Create endpoint - uses Bedrock Marketplace API
    endpoint_arn = bedrock.create_endpoint(
        endpoint_name=sample_endpoint_name,
        endpoint_config={
            "sageMaker": {
                "initialInstanceCount": 1,
                "instanceType": "ml.g5.2xlarge",
                "executionRole": sagemaker_execution_role
                # Other fields:
                #   kmsEncryptionKey: KmsKeyId
                #   vpc: VpcConfig
            }
        },
        # Optional:
        # tags: TagList
        model=model
    )['marketplaceModelEndpoint']['endpointArn']

    # # Describe endpoint - uses Bedrock Marketplace API
    endpoint = bedrock.describe_endpoint(endpoint_arn=endpoint_arn)
    print(DELIMITER)
    print('Created endpoint:')
    pprint.pprint(endpoint)

    # Wait while endpoint is being created
    print(DELIMITER)
    bedrock.wait_for_endpoint(endpoint_arn=endpoint_arn)

    ###
    ###   Currently, customers cannot use self-hosted endpoints with Bedrock Runtime APIs and tools. They can only pass a model ID to the APIs.
    ###   Bedrock Marketplace will enable customers to use self-hosted endpoints through existing Bedrock Runtime APIs and tools
    ###   See below examples of calling invoke_model, invoke_model_with_response_stream, converse and converse_stream
    ###   Customers will be able to use the endpoints with Bedrock dev tools also (Guardrails, Model eval, Agents, Knowledge bases, Prompt flows, Prompt management) - examples not shown below
    ###

    # Prepare sample data for invoke calls by getting default payload in model metadata
    model_data = json.loads(bedrock.describe_model('SageMakerPublicHub', model_name)['HubContentDocument'])
    payload = list(model_data["DefaultPayloads"].keys())[0]
    invoke_body = model_data["DefaultPayloads"][payload]["Body"]
    invoke_content_field_name = 'generated_text'

    # Invoke model (text) - without stream - uses existing Bedrock Runtime API
    print(DELIMITER)
    print(f'Invoking model with body: {invoke_body}')
    invoke_generated_response = bedrock.invoke(endpoint_arn=endpoint_arn, body=json.dumps(invoke_body))
    print(f'Generated text:')
    print(invoke_generated_response[invoke_content_field_name])
    sys.stdout.flush()

    # Converse with model (chat) - without stream - uses existing Bedrock Runtime API
    print(DELIMITER)
    print(f'Converse model with conversation: {conversation}')
    print(bedrock.converse(endpoint_arn=endpoint_arn, conversation=conversation)['output'])

    ###
    ##  Other endpoint management operations
    ###

    # List all endpoints - uses Bedrock Marketplace API
    print(DELIMITER)
    print('Listing all endpoints')
    for endpoint in bedrock.list_endpoints():
        pprint.pprint(endpoint)

    # List endpoints for a model
    # Example: bedrock.list_endpoints_for_model(hub_content_arn='arn:aws:sagemaker:us-west-2:aws:hub-content/SageMakerPublicHub/Model/huggingface-textgeneration1-mpt-7b-storywriter-bf16/3.2.0')
    print(DELIMITER)
    print(f"Listing all endpoints for model: {model_arn}")
    for endpoint in bedrock.list_endpoints_for_model(hub_content_arn=model_arn):
        pprint.pprint(endpoint)

    # # Update endpoint - uses new API provided by Bedrock Marketplace
    updated_endpoint_arn = bedrock.update_endpoint(
        endpoint_arn=endpoint_arn,
        endpoint_config={
            "sageMaker": {
                "initialInstanceCount": 2,  # update to increase instance count
                "instanceType": "ml.g5.2xlarge",
                "executionRole": sagemaker_execution_role
                # Other fields:
                #   kmsEncryptionKey: KmsKeyId
                #   vpc: VpcConfig
            }
        # Optional:
        # tags: TagList
        }
    )['marketplaceModelEndpoint']['endpointArn']

    # Wait while endpoint is being updated
    print(DELIMITER)
    bedrock.wait_for_endpoint(endpoint_arn=updated_endpoint_arn)

    # Confirm endpoint update
    updated_endpoint = bedrock.describe_endpoint(endpoint_arn=updated_endpoint_arn)
    print(f'Updated endpoint: {updated_endpoint}')
    assert updated_endpoint['endpointConfig']['sageMaker']['initialInstanceCount'] == 2
    print(DELIMITER)
    print(f'Confirmed that updated endpoint\'s initialInstanceCount config changed from 1 to 2')

    # Wait while endpoint is being updated
    print(DELIMITER)
    bedrock.wait_for_endpoint(endpoint_arn=updated_endpoint_arn)

    # Deregister endpoint - uses Bedrock Marketplace API
    print(DELIMITER)
    print(f'De-registering endpoint: {updated_endpoint_arn}')
    bedrock.deregister_endpoint(endpoint_arn=updated_endpoint_arn)
    try:
        pprint.pprint(bedrock.describe_endpoint(endpoint_arn=updated_endpoint_arn))
    except ClientError as err:
        assert err.response['Error']['Code'] == 'ResourceNotFoundException'
        print(f"Confirmed that endpoint {updated_endpoint_arn} was de-registered")

    # Re-register endpoint - uses Bedrock Marketplace API
    print(DELIMITER)
    print(f'Registered endpoint: {bedrock.register_endpoint(endpoint_arn=updated_endpoint_arn, model_arn=model_arn)}')
    pprint.pprint(bedrock.describe_endpoint(endpoint_arn=updated_endpoint_arn))

    # Delete endpoint - uses Bedrock Marketplace API
    print(DELIMITER)
    print(f'Deleting endpoint: {updated_endpoint_arn}')
    bedrock.delete_endpoint(endpoint_arn=updated_endpoint_arn)
    try:
        pprint.pprint(bedrock.describe_endpoint(endpoint_arn=updated_endpoint_arn))
    except ClientError as err:
        assert err.response['Error']['Code'] == 'ResourceNotFoundException'
        print(f"Confirmed that endpoint {updated_endpoint_arn} was deleted")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--sagemaker-execution-role', required=True)
    parser.add_argument('--region', required=True)

    args = parser.parse_args()
    run_script(args.sagemaker_execution_role, args.region)
```