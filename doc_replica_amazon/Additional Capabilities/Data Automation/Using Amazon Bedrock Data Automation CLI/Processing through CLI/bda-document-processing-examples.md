

# Processing use cases
<a name="bda-document-processing-examples"></a>

Amazon Bedrock Data Automation allows you to process documents, images, audio, and video. through the command line interface (CLI). For each modality, the workflow consists of creating a project, invoking the analysis, and retrieving the result.

Choose the tab for your preferred method, and then follow the steps:

------
#### [ Documents ]

**Extracting data from a W2**

![Sample W2 form with standard fields, demonstrating layout and data fields that will be extracted.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/W2.png)


When processing a W2 form, an example schema would be the following:

```
{
  "class": "W2TaxForm",
  "description": "Simple schema for extracting key information from W2 tax forms",
  "properties": {
    "employerName": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "The employer's company name"
    },
    "employeeSSN": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "The employee's Social Security Number (SSN)"
    },
    "employeeName": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "The employee's full name"
    },
    "wagesAndTips": {
      "type": "number",
      "inferenceType": "explicit",
      "instruction": "Wages, tips, other compensation (Box 1)"
    },
    "federalIncomeTaxWithheld": {
      "type": "number",
      "inferenceType": "explicit",
      "instruction": "Federal income tax withheld (Box 2)"
    },
    "taxYear": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "The tax year for this W2 form"
    }
  }
}
```

The command to invoke the processing of the W2 would be similar to the following:

```
aws bedrock-data-automation-runtime invoke-data-automation-async \
  --input-configuration '{
    "s3Uri": "s3://w2-processing-bucket-301678011486/input/W2.png"
  }' \
  --output-configuration '{
    "s3Uri": "s3://w2-processing-bucket-301678011486/output/"
  }' \
  --data-automation-configuration '{
    "dataAutomationProjectArn": "Amazon Resource Name (ARN)",
    "stage": "LIVE"
  }' \
  --data-automation-profile-arn "Amazon Resource Name (ARN):data-automation-profile/default"
```

An example of the expected output is:

```
{
  "documentType": "W2TaxForm",
  "extractedData": {
    "employerName": "The Big Company",
    "employeeSSN": "123-45-6789",
    "employeeName": "Jane Doe",
    "wagesAndTips": 48500.00,
    "federalIncomeTaxWithheld": 6835.00,
    "taxYear": "2014"
  },
  "confidence": {
    "employerName": 0.99,
    "employeeSSN": 0.97,
    "employeeName": 0.99,
    "wagesAndTips": 0.98,
    "federalIncomeTaxWithheld": 0.97,
    "taxYear": 0.99
  },
  "metadata": {
    "processingTimestamp": "2025-07-23T23:15:30Z",
    "documentId": "w2-12345",
    "modelId": "amazon.titan-document-v1",
    "pageCount": 1
  }
}
```

------
#### [ Images ]

**Travel advertisement example**

![Sample image, demonstrating how users can extract information from advertisements.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/TravelAdvertisement.jpg)


An example schema for travel advertisements would be the following:

```
{
  "class": "TravelAdvertisement",
  "description": "Schema for extracting information from travel advertisement images",
  "properties": {
    "destination": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "The name of the travel destination being advertised"
    },
    "tagline": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "The main promotional text or tagline in the advertisement"
    },
    "landscapeType": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "The type of landscape shown (e.g., mountains, beach, forest, etc.)"
    },
    "waterFeatures": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "Description of any water features visible in the image (ocean, lake, river, etc.)"
    },
    "dominantColors": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "The dominant colors present in the image"
    },
    "advertisementType": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "The type of travel advertisement (e.g., destination promotion, tour package, etc.)"
    }
  }
}
```

The command to invoke the processing of the travel advertisement would be similar to the following:

```
aws bedrock-data-automation-runtime invoke-data-automation-async \
  --input-configuration '{
    "s3Uri": "s3://travel-ads-bucket-301678011486/input/TravelAdvertisement.jpg"
  }' \
  --output-configuration '{
    "s3Uri": "s3://travel-ads-bucket-301678011486/output/"
  }' \
  --data-automation-configuration '{
    "dataAutomationProjectArn": "Amazon Resource Name (ARN)",
    "stage": "LIVE"
  }' \
  --data-automation-profile-arn "Amazon Resource Name (ARN):data-automation-profile/default"
```

An example of the expected output is:

```
{
  "documentType": "TravelAdvertisement",
  "extractedData": {
    "destination": "Kauai",
    "tagline": "Travel to KAUAI",
    "landscapeType": "Coastal mountains with steep cliffs and valleys",
    "waterFeatures": "Turquoise ocean with white surf along the coastline",
    "dominantColors": "Green, blue, turquoise, brown, white",
    "advertisementType": "Destination promotion"
  },
  "confidence": {
    "destination": 0.98,
    "tagline": 0.99,
    "landscapeType": 0.95,
    "waterFeatures": 0.97,
    "dominantColors": 0.96,
    "advertisementType": 0.92
  },
  "metadata": {
    "processingTimestamp": "2025-07-23T23:45:30Z",
    "documentId": "travel-ad-12345",
    "modelId": "amazon.titan-image-v1",
    "imageWidth": 1920,
    "imageHeight": 1080
  }
}
```

------
#### [ Audio ]

**Transcribing a phone call**

An example schema for a phone call would be the following:

```
{
  "class": "AudioRecording",
  "description": "Schema for extracting information from AWS customer call recordings",
  "properties": {
    "callType": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "The type of call (e.g., technical support, account management, consultation)"
    },
    "participants": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "The number and roles of participants in the call"
    },
    "mainTopics": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "The main topics or AWS services discussed during the call"
    },
    "customerIssues": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "Any customer issues or pain points mentioned during the call"
    },
    "actionItems": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "Action items or next steps agreed upon during the call"
    },
    "callDuration": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "The duration of the call"
    },
    "callSummary": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "A brief summary of the entire call"
    }
  }
}
```

The command to invoke the processing of a phone call would be similar to the following:

```
aws bedrock-data-automation-runtime invoke-data-automation-async \
  --input-configuration '{
    "s3Uri": "s3://audio-analysis-bucket-301678011486/input/AWS_TCA-Call-Recording-2.wav"
  }' \
  --output-configuration '{
    "s3Uri": "s3://audio-analysis-bucket-301678011486/output/"
  }' \
  --data-automation-configuration '{
    "dataAutomationProjectArn": "Amazon Resource Name (ARN)",
    "stage": "LIVE"
  }' \
  --data-automation-profile-arn "Amazon Resource Name (ARN):data-automation-profile/default"
```

An example of the expected output is:

```
{
  "documentType": "AudioRecording",
  "extractedData": {
    "callType": "Technical consultation",
    "participants": "3 participants: AWS Solutions Architect, AWS Technical Account Manager, and Customer IT Director",
    "mainTopics": "AWS Bedrock implementation, data processing pipelines, model fine-tuning, and cost optimization",
    "customerIssues": "Integration challenges with existing ML infrastructure, concerns about latency for real-time processing, questions about data security compliance",
    "actionItems": [
      "AWS team to provide documentation on Bedrock data processing best practices",
      "Customer to share their current ML architecture diagrams",
      "Schedule follow-up meeting to review implementation plan",
      "AWS to provide cost estimation for proposed solution"
    ],
    "callDuration": "45 minutes and 23 seconds",
    "callSummary": "Technical consultation call between AWS team and customer regarding implementation of AWS Bedrock for their machine learning workloads. Discussion covered integration approaches, performance optimization, security considerations, and next steps for implementation planning."
  },
  "confidence": {
    "callType": 0.94,
    "participants": 0.89,
    "mainTopics": 0.92,
    "customerIssues": 0.87,
    "actionItems": 0.85,
    "callDuration": 0.99,
    "callSummary": 0.93
  },
  "metadata": {
    "processingTimestamp": "2025-07-24T00:30:45Z",
    "documentId": "audio-12345",
    "modelId": "amazon.titan-audio-v1",
    "audioDuration": "00:45:23",
    "audioFormat": "WAV",
    "sampleRate": "44.1 kHz"
  },
  "transcript": {
    "segments": [
      {
        "startTime": "00:00:03",
        "endTime": "00:00:10",
        "speaker": "Speaker 1",
        "text": "Hello everyone, thank you for joining today's call about implementing AWS Bedrock for your machine learning workloads."
      },
      {
        "startTime": "00:00:12",
        "endTime": "00:00:20",
        "speaker": "Speaker 2",
        "text": "Thanks for having us. We're really interested in understanding how Bedrock can help us streamline our document processing pipeline."
      },
      {
        "startTime": "00:00:22",
        "endTime": "00:00:35",
        "speaker": "Speaker 3",
        "text": "Yes, and specifically we'd like to discuss integration with our existing systems and any potential latency concerns for real-time processing requirements."
      }
      // Additional transcript segments would continue here
    ]
  }
}
```

------
#### [ Video ]

**Processing a video**

An example schema for videos would be the following:

```
{
  "class": "VideoContent",
  "description": "Schema for extracting information from video content",
  "properties": {
    "title": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "The title or name of the video content"
    },
    "contentType": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "The type of content (e.g., tutorial, competition, documentary, advertisement)"
    },
    "mainSubject": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "The main subject or focus of the video"
    },
    "keyPersons": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "Key people appearing in the video (hosts, participants, etc.)"
    },
    "keyScenes": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "Description of important scenes or segments in the video"
    },
    "audioElements": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "Description of notable audio elements (music, narration, dialogue)"
    },
    "summary": {
      "type": "string",
      "inferenceType": "explicit",
      "instruction": "A brief summary of the video content"
    }
  }
}
```

The command to invoke the processing of the video would be similar to the following:

```
aws bedrock-data-automation-runtime invoke-data-automation-async \
  --input-configuration '{
    "s3Uri": "s3://video-analysis-bucket-301678011486/input/MakingTheCut.mp4",
    "assetProcessingConfiguration": {
      "video": {
        "segmentConfiguration": {
          "timestampSegment": {
            "startTimeMillis": 0,
            "endTimeMillis": 300000
          }
        }
      }
    }
  }' \
  --output-configuration '{
    "s3Uri": "s3://video-analysis-bucket-301678011486/output/"
  }' \
  --data-automation-configuration '{
    "dataAutomationProjectArn": "Amazon Resource Name (ARN)",
    "stage": "LIVE"
  }' \
  --data-automation-profile-arn "Amazon Resource Name (ARN):data-automation-profile/default"
```

An example of the expected output is:

```
{
  "documentType": "VideoContent",
  "extractedData": {
    "title": "Making the Cut",
    "contentType": "Fashion design competition",
    "mainSubject": "Fashion designers competing to create the best clothing designs",
    "keyPersons": "Heidi Klum, Tim Gunn, and various fashion designer contestants",
    "keyScenes": [
      "Introduction of the competition and contestants",
      "Design challenge announcement",
      "Designers working in their studios",
      "Runway presentation of designs",
      "Judges' critique and elimination decision"
    ],
    "audioElements": "Background music, host narration, contestant interviews, and design feedback discussions",
    "summary": "An episode of 'Making the Cut' fashion competition where designers compete in a challenge to create innovative designs. The episode includes the challenge announcement, design process, runway presentation, and judging."
  },
  "confidence": {
    "title": 0.99,
    "contentType": 0.95,
    "mainSubject": 0.92,
    "keyPersons": 0.88,
    "keyScenes": 0.90,
    "audioElements": 0.87,
    "summary": 0.94
  },
  "metadata": {
    "processingTimestamp": "2025-07-24T00:15:30Z",
    "documentId": "video-12345",
    "modelId": "amazon.titan-video-v1",
    "videoDuration": "00:45:23",
    "analyzedSegment": "00:00:00 - 00:05:00",
    "resolution": "1920x1080"
  },
  "transcript": {
    "segments": [
      {
        "startTime": "00:00:05",
        "endTime": "00:00:12",
        "speaker": "Heidi Klum",
        "text": "Welcome to Making the Cut, where we're searching for the next great global fashion brand."
      },
      {
        "startTime": "00:00:15",
        "endTime": "00:00:25",
        "speaker": "Tim Gunn",
        "text": "Designers, for your first challenge, you'll need to create a look that represents your brand and can be sold worldwide."
      }
      // Additional transcript segments would continue here
    ]
  }
}
```

------