

# Associating Library with a Project
<a name="bda-library-associating"></a>

To use custom vocabulary, associate your library with a BDA project. This can be done in two ways:

## Option 1: Create Project with Library:
<a name="bda-library-associating-option1"></a>

**AWS CLI Example:**

```
aws bedrock-data-automation create-data-automation-project \
    --project-name "audio-transcription-project" \
    --standard-output-configuration '{
        "audio": {
            "extraction": {
                "category": {
                    "state": "ENABLED",
                    "types": ["TRANSCRIPTION"]
                }
            }
        }
    }' \
    --data-automation-libraries '[{
        "libraryArn": "arn:aws:bedrock:us-east-1:123456789012:data-automation-library/healthcare-vocabulary"
    }]'
```

**AWS Console Example:**

1. Navigate to the Bedrock "Data Automation" page

1. Create a project

1. Navigate to the project detail page

1. Choose "Associated library" tab

1. Choose "Associate a library" button

1. Choose a library by selecting the radio button next to it and choose the "Associate library" button

![Create library dialog with fields for library name, description, KMS key, and tags.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/library-associate-from-project-console.png)


## Option 2: Update Existing Project with library:
<a name="bda-library-associating-option2"></a>

```
aws bedrock-data-automation update-data-automation-project \
    --project-arn "arn:aws:bedrock:us-east-1:123456789012:data-automation-project/audio-transcription-project" \
    --data-automation-libraries '[{
        "libraryArn": "arn:aws:bedrock:us-east-1:123456789012:data-automation-library/healthcare-vocabulary"
    }]'
```

**AWS Console Example:**

1. Navigate to the "Library details" page for your library

1. Expand "Associated projects"

1. Choose "Associate projects"

1. Choose the projects to associate and choose "Associate project"

![Associated projects table showing no projects with Associate projects button available.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/library-associate-from-library-console.png)
