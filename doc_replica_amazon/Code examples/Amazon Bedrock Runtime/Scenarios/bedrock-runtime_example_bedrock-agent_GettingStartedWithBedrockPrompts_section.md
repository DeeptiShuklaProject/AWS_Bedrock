

# An end-to-end example showing how to create and invoke Amazon Bedrock managed prompts using an AWS SDK
<a name="bedrock-runtime_example_bedrock-agent_GettingStartedWithBedrockPrompts_section"></a>

The following code example shows how to:
+ Create a managed prompt.
+ Create a version of the prompt.
+ Invoke the prompt using the version.
+ Clean up resources (optional).

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
Create and invoke a managed prompt.  

```
import argparse
import boto3
import logging
import time

# Now import the modules
from prompt import create_prompt, create_prompt_version, delete_prompt
from run_prompt import invoke_prompt

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)



def run_scenario(bedrock_client, bedrock_runtime_client, model_id, cleanup=True):
    """
    Runs the Amazon Bedrock managed prompt scenario.
    
    Args:
        bedrock_client: The Amazon Bedrock Agent client.
        bedrock_runtime_client: The Amazon Bedrock Runtime client.
        model_id (str): The model ID to use for the prompt.
        cleanup (bool): Whether to clean up resources at the end of the scenario.
        
    Returns:
        dict: A dictionary containing the created resources.
    """
    prompt_id = None
    
    try:
        # Step 1: Create a prompt
        print("\n=== Step 1: Creating a prompt ===")
        prompt_name = f"PlaylistGenerator-{int(time.time())}"
        prompt_description = "Playlist generator"
        prompt_template = """
          Make me a {{genre}} playlist consisting of the following number of songs: {{number}}."""
        
        create_response = create_prompt(
            bedrock_client,
            prompt_name,
            prompt_description,
            prompt_template,
            model_id
        )
        
        prompt_id = create_response['id']
        print(f"Created prompt: {prompt_name} with ID: {prompt_id}")
        
        # Create a version of the prompt
        print("\n=== Creating a version of the prompt ===")
        version_response = create_prompt_version(
            bedrock_client,
            prompt_id,
            description="Initial version of the product description generator"
        )
        
        prompt_version_arn = version_response['arn']
        prompt_version = version_response['version']

        print(f"Created prompt version: {prompt_version}")
        print(f"Prompt version ARN: {prompt_version_arn}")
        
        # Step 2: Invoke the prompt directly
        print("\n=== Step 2: Invoking the prompt ===")
        input_variables = {
            "genre": "pop",
            "number": "2",
           }
        
        # Use the ARN from the create_prompt_version response
        result = invoke_prompt(
            bedrock_runtime_client,
            prompt_version_arn,  
            input_variables
        )
        # Display the playlist
        print(f"\n{result}")
    
        
        # Step 3: Clean up resources (optional)
        if cleanup:
            print("\n=== Step 3: Cleaning up resources ===")
            
            # Delete the prompt
            print(f"Deleting prompt {prompt_id}...")
            delete_prompt(bedrock_client, prompt_id)
            
            print("Cleanup complete")
        else:
            print("\n=== Resources were not cleaned up ===")
            print(f"Prompt ID: {prompt_id}")
        
   
        
    except Exception as e:
        logger.exception("Error in scenario: %s", str(e))
        
        # Attempt to clean up if an error occurred and cleanup was requested
        if cleanup and prompt_id:
            try:
                print("\nCleaning up resources after error...")
                
                # Delete the prompt
                try:
                    delete_prompt(bedrock_client, prompt_id)
                    print("Cleanup after error complete")
                except Exception as cleanup_error:
                    logger.error("Error during cleanup: %s", str(cleanup_error))
            except Exception as final_error:
                logger.error("Final error during cleanup: %s", str(final_error))
        
        # Re-raise the original exception
        raise

def main():
    """
    Entry point for the Amazon Bedrock managed prompt scenario.
    """
    parser = argparse.ArgumentParser(
        description="Run the Amazon Bedrock managed prompt scenario."
    )
    parser.add_argument(
        '--region',
        default='us-east-1',
        help="The AWS Region to use."
    )
    parser.add_argument(
        '--model-id',
        default='anthropic.claude-v2',
        help="The model ID to use for the prompt."
    )
    parser.add_argument(
        '--cleanup',
        action='store_true',
        default=True,
        help="Clean up resources at the end of the scenario."
    )
    parser.add_argument(
        '--no-cleanup',
        action='store_false',
        dest='cleanup',
        help="Don't clean up resources at the end of the scenario."
    )
    args = parser.parse_args()

    bedrock_client = boto3.client('bedrock-agent', region_name=args.region)
    bedrock_runtime_client = boto3.client('bedrock-runtime', region_name=args.region)
    
    print("=== Amazon Bedrock Managed Prompt Scenario ===")
    print(f"Region: {args.region}")
    print(f"Model ID: {args.model_id}")
    print(f"Cleanup resources: {args.cleanup}")
    
    try:
        run_scenario(
            bedrock_client,
            bedrock_runtime_client,
            args.model_id,
            args.cleanup
        )
        
    except Exception as e:
        logger.exception("Error running scenario: %s", str(e))
        
if __name__ == "__main__":
    main()
```
+ For API details, see the following topics in *AWS SDK for Python (Boto3) API Reference*.
  + [Converse](https://docs.aws.amazon.com/goto/boto3/bedrock-runtime-2023-09-30/Converse)
  + [CreatePrompt](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/CreatePrompt)
  + [CreatePromptVersion](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/CreatePromptVersion)
  + [DeletePrompt](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/DeletePrompt)

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.