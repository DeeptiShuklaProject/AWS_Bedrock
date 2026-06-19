

# Blueprint Operations CLI
<a name="bda-blueprint-operations"></a>

This guide covers Blueprint operations available through the AWS Command Line Interface (CLI) for Amazon Bedrock Data Automation (BDA).

## Creating Blueprints
<a name="create-blueprints-cli"></a>

Blueprints define the structure and properties of data you want to extract from your documents, images, audio, or video files. Use the create-blueprint command to define a new Blueprint.

The following command creates a new Blueprint tailored to extract data from a passport image.

**Syntax**

```
aws bedrock-data-automation create-blueprint \
      --blueprint-name "passport-blueprint" \
      --type "IMAGE" \
      --blueprint-stage "DEVELOPMENT" \
      --schema '{
        "class": "Passport",
        "description": "Blueprint for processing passport images",
        "properties": {
          "passport_number": {
            "type": "string",
            "inferenceType": "explicit",
            "instruction": "The passport identification number"
          },
          "full_name": {
            "type": "string",
            "inferenceType": "explicit",
            "instruction": "The full name of the passport holder"
          },
          "expiration_date": {
            "type": "string",
            "inferenceType": "explicit",
            "instruction": "The passport expiration date"
          }
        }
      }'
```

## Complete parameter reference
<a name="create-blueprint-parameters"></a>

The following table shows all available parameters for the `create-blueprint` command:


**Parameters for create-blueprint**  

| Parameter | Required | Default | Description | 
| --- | --- | --- | --- | 
| --blueprint-name | Yes | N/A | Name for the Blueprint | 
| --type | Yes | N/A | Type of content (IMAGE, DOCUMENT, AUDIO, VIDEO) | 
| --blueprint-stage | No | LIVE | Stage for the Blueprint (DEVELOPMENT or LIVE) | 
| --schema | Yes | N/A | JSON schema defining the Blueprint structure | 
| --client-token | No | Auto-generated | Unique identifier for request idempotency | 

## Viewing Blueprint configurations
<a name="view-blueprint-cli"></a>

**List all Blueprints**

Use the list-blueprints command to retrieve a list of all Blueprints associated to your account.

**Syntax**

```
aws bedrock-data-automation list-blueprints
```

**View Blueprint details**

To see detailed information about a specific Blueprint, including its schema and configuration, use the get-blueprint command.

**Syntax**

```
aws bedrock-data-automation get-blueprint \
      --blueprint-arn "Amazon Resource Name (ARN)"
```

**Inspect specific version**

When working with versioned Blueprints, use the get-blueprint command with the --blueprint-version option to view a particular version.

**Syntax**

```
      aws bedrock-data-automation get-blueprint \
      --blueprint-arn "Amazon Resource Name (ARN)" \
      --blueprint-version "version-number"
```

**Inspect specific stage**

To view Blueprints in either DEVELOPMENT or LIVE stage, use:

```
      aws bedrock-data-automation get-blueprint \
      --blueprint-arn "Amazon Resource Name (ARN)" \
      --blueprint-stage "LIVE"
```

## Editing Blueprint specifications
<a name="edit-blueprint-cli"></a>

**Update Blueprint settings**

To modify an existing Blueprint's schema or properties, use the update-blueprint command.

**Syntax**

```
aws bedrock-data-automation update-blueprint \
      --blueprint-arn "Amazon Resource Name (ARN)" \
      --schema '{
        "class": "Passport",
        "description": "Updated blueprint for processing passport images",
        "properties": {
          "passport_number": {
            "type": "string",
            "inferenceType": "explicit",
            "instruction": "The passport identification number"
          },
          "full_name": {
            "type": "string",
            "inferenceType": "explicit",
            "instruction": "The full name of the passport holder"
          },
          "expiration_date": {
            "type": "string",
            "inferenceType": "explicit",
            "instruction": "The passport expiration date"
          }
        }
      }'
```

**Note:** When updating a Blueprint, you must provide the complete schema, even for fields you're not changing.

**Promote to LIVE**

To move a Blueprint from DEVELOPMENT to LIVE stage for production, use the update-blueprint command with the --blueprint-stage option.

**Syntax**

```
aws bedrock-data-automation update-blueprint \
      --blueprint-arn "Amazon Resource Name (ARN)" \
      --blueprint-stage "LIVE"
```

**Blueprint versioning**

Create a new version of your Blueprint to preserve its current state before making significant changes using the create-blueprint-version command.

**Syntax**

```
aws bedrock-data-automation create-blueprint-version \
      --blueprint-arn "Amazon Resource Name (ARN)"
```

## Managing Blueprint tags
<a name="tag-management-cli"></a>

Tags help users organize and categorize Blueprints for simplified management.

**Add tags**

Apply metadata to your Blueprint by adding tags.

**Syntax**

```
aws bedrock-data-automation tag-resource \
      --resource-arn "Amazon Resource Name (ARN)" \
      --tags '{"Department":"Finance","Project":"PassportProcessing"}'
```

**Remove tags**

Remove specific tags from your Blueprint with the untag-resource command.

**Syntax**

```
aws bedrock-data-automation untag-resource \
      --resource-arn "Amazon Resource Name (ARN)" \
      --tag-keys '["Department","Project"]'
```

**View tags**

List all tags associated with your Blueprint using the list-tags-for-resource command.

**Syntax**

```
aws bedrock-data-automation list-tags-for-resource \
      --resource-arn "Amazon Resource Name (ARN)"
```

## Deleting Blueprints
<a name="delete-blueprint-cli"></a>

**Delete an entire Blueprint**

Use the delete-blueprint command to permanently remove a Blueprint and all its versions.

**Syntax**

```
aws bedrock-data-automation delete-blueprint \
          --blueprint-arn "Amazon Resource Name (ARN)"
```

**Caution:** This command permanently deletes a Blueprint and cannot recover it.

**Important:** You cannot delete a Blueprint that's currently in use by any projects. Before deleting, ensure the Blueprint isn't referenced in any project's custom output configuration.

## Blueprint Optimization
<a name="blueprint-optimization-cli"></a>

### Invoking Blueprint Optimization
<a name="invoking-blueprint-optimization"></a>

Start an asynchronous blueprint optimization job to improve blueprint's instructions of each of your blueprint fields and result accuracy.

**Syntax**

```
aws bedrock-data-automation invoke-blueprint-optimization-async \
    --blueprint blueprintArn="arn:aws:bedrock:<region>:<account_id>:blueprint/<blueprint_id>",stage="DEVELOPMENT" \
    --samples '[
        {
            "assetS3Object": {
                "s3Uri": "s3://my-optimization-bucket/samples/document1.pdf"
            },
            "groundTruthS3Object": {
                "s3Uri": "s3://my-optimization-bucket/ground-truth/document1-expected.json"
            }
        }
    ]' \
    --output-configuration s3Object='{s3Uri="s3://my-optimization-bucket/results/optimization-output"}' \
    --data-automation-profile-arn "Amazon Resource Name (ARN):data-automation-profile/default"
```

### Checking Blueprint Optimization Status
<a name="checking-blueprint-optimization-status"></a>

Monitor the progress and results of a blueprint optimization job.

**Syntax**

```
aws bedrock-data-automation get-blueprint-optimization-status \
    --invocation-arn "arn:aws:bedrock:<region>:<account_id>:blueprint-optimization-invocation/opt-12345abcdef"
```

Use this command to track the optimization job status. The response includes the current status (Created, InProgress, Success, ServiceError, or ClientError) and output configuration details when completed.

### Copying Blueprint Stages
<a name="copying-blueprint-stages"></a>

Copy a Blueprint from one stage to another

**Syntax**

```
aws bedrock-data-automation copy-blueprint-stage \
    --blueprint-arn "arn:aws:bedrock:<region>:<account_id>:blueprint/<blueprint_id>" \
    --source-stage "DEVELOPMENT" \
    --target-stage "LIVE"
```

**Caution:** This command copies the entire Blueprint configuration from the source stage to the target stage, overwriting any existing configuration in the target stage.

**Important:** Ensure the Blueprint is thoroughly tested in the source stage before copying to production (LIVE) stage. This operation cannot be easily undone.