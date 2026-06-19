

# Understand how the results of your model evaluation job are saved in Amazon S3
<a name="model-evaluation-report-s3"></a>

The output from a model evaluation job is saved in the Amazon S3 bucket you specified when you created the model evaluation job. Results of model evaluation jobs are saved as JSON line files (`.jsonl`).

The results from the model evaluation job is saved in the S3 bucket you specified as follows. 
+ For model evaluation jobs that use human workers:

  `s3://{{user-specified-S3-output-path}}/{{job-name}}/{{job-uuid}}/datasets/{{dataset-name}}/{{file-uuid}}_output.jsonl` 
+ For automatic model evaluation jobs:

  `s3://{{user-specified-S3-output-path}}/{{job-name}}/{{job-uuid}}/models/{{model-id}}/taskTypes/{{task-type}}/datasets/{{dataset}}/{{file-uuid}}_output.jsonl`

For model or RAG evaluation jobs with one or more custom metrics, Amazon Bedrock also stores your metric definitions as JSON files in the output S3 bucket you specify. You can access these files by navigating to `s3://{{S3-output-bucket-name}}/{{job-name}}/{{job-uuid}}/custom_metrics`. To see the format for JSON definitions of custom metrics, see [Creating a JSON file to create a custom metric](model-evaluation-custom-metrics-prompt-formats.md#model-evaluation-custom-metrics-prompt-formats-json).

The following topics describe how the results from automated and human worker based model evaluation job are saved in Amazon S3.

## Output data from automated model evaluation jobs
<a name="model-evaluation-report-s3-automated"></a>

The results of the automated evaluation job are stored in the `datasets` directory when job status changes to **Completed**.

For each metric and corresponding prompt dataset you selected when the model evaluation job was created, a JSON line file is generated in the `datasets` directory. The file uses the following naming convention `metric_input-dataset.jsonl`.

Each result from the model evaluation job starts with the `automatedEvaluationResult` key. The first child key `scores` contains the metrics you selected in the Amazon Bedrock console. In this example, only a single metric `Accuracy` was selected. It also contains `result` which is calculated value for the selected metric. To learn more about what specific value is calculated, see [Review metrics for an automated model evaluation job in Amazon Bedrock (console)](model-evaluation-report-programmatic.md).

The second key, `inputRecord` is a copy of what you provided in your input prompt dataset.

The third key, `modelResponses` contains a list of JSON objects which contains the ARN of the model selected when you created the model evaluation job. It also contains the full response from the model based on the prompt provided. 

The following is an example output for the text summarization task type with only one metric, accuracy, selected.

```
{
"automatedEvaluationResult": {
    "scores": [{
        "metricName": "Accuracy",
        "result": 0.31920555233955383
    }]
},
"inputRecord": {
    "prompt": "Human: two bodies have been recovered from a flooded coal mine in yiyang city , central china 's henan province , as of #:## thursday morning , rescuers said . Assistant:",
    "referenceResponse": "two bodies recovered from flooded coal mine in c. china"
},
"modelResponses": [{
    "modelIdentifier": "arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-v2",
    "response": " Here are the key points I gathered from your news summary:\n\n- Two bodies have been recovered from a flooded coal mine in Yiyang City, in China's Henan province.\n\n- This happened as of Thursday morning, according to rescuers.\n\n- The location is central China's Henan province. \n\n- Yiyang City is where the flooded coal mine is located.\n\n- The coal mine was flooded, leading to the two deaths and need for rescue/recovery efforts.\n\n- This news is developing as of Thursday morning, so the death toll and rescue details may still be unfolding.\n\nPlease let me know if I have accurately summarized the key information or if you would like me to expand on any part of it."
}]
}
```

## Output data from model evaluation jobs that use human workers.
<a name="model-evaluation-report-s3-hil"></a>

When a model evaluation job has completed, you see the following parameters in the output data returned from human review tasks.


****  

| Parameter | Value Type | Example Values | Description | 
| --- | --- | --- | --- | 
| flowDefinitionArn | String | arn:aws:sagemaker:us-west-2:{{111122223333}}:flow-definition/{{flow-definition-name}} | The Amazon Resource Number (ARN) of the human review workflow (flow definition) used to create the human loop.  | 
| humanAnswers | List of JSON objects |  <pre>"answerContent": {<br />"evaluationResults": {<br />	"thumbsUpDown": [{<br />		"metricName": "Relevance",<br />		"modelResponseId": "0",<br />		"result": false<br />	}]<br />}<br />}</pre>  | A list of JSON objects that contain worker responses in `answerContent`.  | 
| `humanLoopName` | String | system-generated-hash | A system generated 40-character hex string. | 
| inputRecord | JSON object |  <pre>"inputRecord": {<br />"prompt": "What does vitamin C serum do for skin?",<br />"category": "Skincare",<br />"referenceResponse": "Vitamin C serum offers a range of benefits for the skin. Firstly, it acts....<br />}</pre>  | A JSON object that contains an entry prompt from the input dataset.  | 
| modelResponses | List of JSON objects |  <pre>"modelResponses": [{<br />"modelIdentifier": "arn:aws:bedrock:{{us-west-2}}::foundation-model/{{model-id}}",<br />"response": "the-models-response-to-the-prompt"<br />}]</pre>  | The individual responses from the models. | 
| inputContent | Object | <pre>{<br />     "additionalDataS3Uri":"s3://{{user-specified-S3-URI-path}}/datasets/{{dataset-name}}/records/{{record-number}}/human-loop-additional-data.json",<br />     "evaluationMetrics":[<br />        {<br />           "description":"testing",<br />           "metricName":"IndividualLikertScale",<br />           "ratingMethod":"IndividualLikertScale"<br />        }<br />     ],<br />     "instructions":"example instructions"<br />  }</pre> | The human loop input content required to start human loop in your S3 bucket. | 
| modelResponseIdMap | Object | <pre>{<br />     "0":"arn:aws:bedrock:us-west-2::foundation-model/{{model-id}}"<br />}</pre> | `humanAnswers.answerContent.evaluationResults` contains `modelResponseId`s. The `modelResponseIdMap` connects the `modelResponseId` to the model name. | 

<a name="code-sample-model-eval"></a>The following is an example of output data from a model evaluation job. 

```
{
"humanEvaluationResult": [{
    "flowDefinitionArn": "arn:aws:sagemaker:us-west-2:111122223333:flow-definition/flow-definition-name",
    "humanAnswers": [{
        "acceptanceTime": "2023-11-09T19:17:43.107Z",
        "answerContent": {
            "evaluationResults": {
                "thumbsUpDown": [{
                    "metricName": "Coherence",
                    "modelResponseId": "0",
                    "result": false
                }, {
                    "metricName": "Accuracy",
                    "modelResponseId": "0",
                    "result": true
                }],
                "individualLikertScale": [{
                    "metricName": "Toxicity",
                    "modelResponseId": "0",
                    "result": 1
                }]
            }
        },
        "submissionTime": "2023-11-09T19:17:52.101Z",
        "timeSpentInSeconds": 8.994,
        "workerId": "444455556666",
        "workerMetadata": {
            "identityData": {
                "identityProviderType": "Cognito",
                "issuer": "https://cognito-idp.AWS Region.amazonaws.com/AWS Region_111222",
                "sub": "c6aa8eb7-9944-42e9-a6b9-"
            }
        }
    }],



				...Additional response have been truncated for clarity...

  }],

 "humanLoopName": "b3b1c64a2166e001e094123456789012",
 "inputContent":{
     "additionalDataS3Uri":"s3://{{user-specified-S3-output-path}}/datasets/{{dataset-name}}/records/{{record-number}}/human-loop-additional-data.json",
     "evaluationMetrics":[
        {
           "description":"testing",
           "metricName":"IndividualLikertScale",
           "ratingMethod":"IndividualLikertScale"
        }
     ],
     "instructions":"some dummy instructions"
  },
  "modelResponseIdMap":{
     "0":"arn:aws:bedrock:{{AWS Region}}::foundation-model/{{model-id}}"
  }
},
"inputRecord": {
    "category": "Fitness",
    "prompt": "Human: What is High-Intensity Interval Training ? \\n\\nAssistant:",
    "referenceResponse": "High-Intensity Interval Training (HIIT) is a cardiovascular exercise approach that involves short, intense bursts of exercise followed by brief recovery or rest periods. In HIIT, you perform exercises at near-maximum effort during the high-intensity intervals, which can include activities like sprinting, cycling, jumping, or body weight exercises such as burpees or push-ups. These intense intervals are interspersed with short recovery periods to lower your heart rate before the next high-intensity bout. HIIT workouts usually consist of multiple cycles of these intervals, and the number of cycles and the length of intervals can vary. HIIT is known for its time efficiency, making it an excellent choice for those with busy schedules. It offers both aerobic and anaerobic benefits, improving cardiovascular fitness, burning calories, and promoting fat loss, all while boosting metabolism for continued calorie burning post-workout."
},
"modelResponses": [{
    "modelIdentifier": "arn:aws:bedrock:AWS Region::foundation-model/{{model-id}}",
    "response": " High-intensity interval training (HIIT) is a form of exercise that involves short bursts of intense activity alternated with recovery periods. Here are some key features of HIIT:\n\n- Alternates short periods of intense anaerobic exercise with less intense recovery periods. The high-intensity periods are typically done at 80-95% of maximum heart rate.\n\n- The duration of the intense periods can range from 5 seconds to 8 minutes, but typically are in the range of 30 seconds to 4 minutes.\n\n- The total HIIT session typically lasts between 10-30 minutes, including warm-up, recovery periods, and cool down. \n\n- Uses exercises like sprints, cycling, rowing, jumping rope, stair climbing, swimming, etc. Movements that get your heart rate up quickly.\n\n- The short, intense intervals help improve cardiovascular fitness by increasing heart rate and oxygen consumption.\n\n- HIIT burns more calories and fat than steady-state cardio in a shorter time period. It also helps build muscle strength and endurance.\n\n- Considered an efficient and effective form of exercise for fat loss and improving aerobic power. But it requires motivation to push yourself during the intense intervals.\n\n- Not suitable for beginners due to the high-intensity. Start with steady-state cardio and build up endurance before trying HIIT.\n\nIn summary, HIIT intersperses intense bursts of"
}]
}


}
```

The following table explains how the **Rating method** you selected for each metric in the Amazon Bedrock console is returned in your Amazon S3 bucket. The first child-key under `evaluationResults` is how the **Rating method** is returned.




**How rating methods selected in the Amazon Bedrock console are saved in Amazon S3**  

| Rating method selected | Saved in Amazon S3 | 
| --- | --- | 
| Likert scale - Individual | IndividualLikertScale | 
| Likert scale - Comparison | ComparisonLikertScale | 
| Choice buttons | ComparisonChoice | 
| Ordinal rank | ComparisonRank | 
| Thumbs up/down | ThumbsUpDown | 