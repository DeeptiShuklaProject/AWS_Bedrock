

# Dissociation of Library from a Project
<a name="bda-library-dissociating"></a>

You can dissociate a library from a project using the [UpdateDataAutomationProject](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_data-automation_UpdateDataAutomationProject.html) API.

## AWS CLI Example:
<a name="bda-library-dissociating-cli"></a>

```
aws bedrock-data-automation update-data-automation-project \
    --project-arn "arn:aws:bedrock:us-east-1:123456789012:data-automation-project/audio-transcription-project" \
    --data-automation-libraries '[]'
```

## AWS Console Example:
<a name="bda-library-dissociating-console"></a>

1. Navigate to the "Library details" page for your library

1. Expand "Associated projects"

1. Choose the desired project

1. Choose "Dissociate project"

![Associated projects table showing one project named custom-vocab-project with its ID, ARN, and modification date.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/library-dissociate-console.png)
