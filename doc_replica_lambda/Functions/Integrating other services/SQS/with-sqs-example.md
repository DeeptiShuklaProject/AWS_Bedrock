

# Tutorial: Using Lambda with Amazon SQS
<a name="with-sqs-example"></a>

In this tutorial, you create a Lambda function that consumes messages from an [Amazon Simple Queue Service (Amazon SQS)](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html) queue. The Lambda function runs whenever a new message is added to the queue. The function writes the messages to an Amazon CloudWatch Logs stream. The following diagram shows the AWS resources you use to complete the tutorial.

![Diagram showing Amazon SQS message, Lambda function, and CloudWatch Logs stream](http://docs.aws.amazon.com/lambda/latest/dg/images/sqs_tut_resources.png)


To complete this tutorial, you carry out the following steps:

1. Create a Lambda function that writes messages to CloudWatch Logs.

1. Create an Amazon SQS queue.

1. Create a Lambda event source mapping. The event source mapping reads the Amazon SQS queue and invokes your Lambda function when a new message is added.

1. Test the setup by adding messages to your queue and monitoring the results in CloudWatch Logs.

## Prerequisites
<a name="with-sqs-prepare"></a>

### Install the AWS Command Line Interface
<a name="install_aws_cli"></a>

If you have not yet installed the AWS Command Line Interface, follow the steps at [Installing or updating the latest version of the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) to install it.

The tutorial requires a command line terminal or shell to run commands. In Linux and macOS, use your preferred shell and package manager.

**Note**  
In Windows, some Bash CLI commands that you commonly use with Lambda (such as `zip`) are not supported by the operating system's built-in terminals. To get a Windows-integrated version of Ubuntu and Bash, [install the Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10). 

## Create the execution role
<a name="with-sqs-create-execution-role"></a>

![Step 1 create the execution role](http://docs.aws.amazon.com/lambda/latest/dg/images/sqs_tut_steps1.png)


An [execution role](lambda-intro-execution-role.md) is an AWS Identity and Access Management (IAM) role that grants a Lambda function permission to access AWS services and resources. To allow your function to read items from Amazon SQS, attach the **AWSLambdaSQSQueueExecutionRole** permissions policy.

**To create an execution role and attach an Amazon SQS permissions policy**

1. Open the [Roles page](https://console.aws.amazon.com/iam/home#/roles) of the IAM console.

1. Choose **Create role**.

1. For **Trusted entity type**, choose **AWS service**.

1. For **Use case**, choose **Lambda**.

1. Choose **Next**.

1. In the **Permissions policies** search box, enter **AWSLambdaSQSQueueExecutionRole**.

1. Select the **AWSLambdaSQSQueueExecutionRole** policy, and then choose **Next**.

1. Under **Role details**, for **Role name**, enter **lambda-sqs-role**, then choose **Create role**.

After role creation, note down the Amazon Resource Name (ARN) of your execution role. You'll need it in later steps.

## Create the function
<a name="with-sqs-create-function"></a>

![Step 2 create the Lambda function](http://docs.aws.amazon.com/lambda/latest/dg/images/sqs_tut_steps2.png)


Create a Lambda function that processes your Amazon SQS messages. The function code logs the body of the Amazon SQS message to CloudWatch Logs.

This tutorial uses the Node.js 24 runtime, but we've also provided example code in other runtime languages. You can select the tab in the following box to see code for the runtime you're interested in. The JavaScript code you'll use in this step is in the first example shown in the **JavaScript** tab.

------
#### [ .NET ]

**SDK for .NET**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [Serverless examples](https://github.com/aws-samples/serverless-snippets/tree/main/integration-sqs-to-lambda) repository. 
Consuming an SQS event with Lambda using .NET.  

```
// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0
﻿using Amazon.Lambda.Core;
using Amazon.Lambda.SQSEvents;


// Assembly attribute to enable the Lambda function's JSON input to be converted into a .NET class.
[assembly: LambdaSerializer(typeof(Amazon.Lambda.Serialization.SystemTextJson.DefaultLambdaJsonSerializer))]

namespace SqsIntegrationSampleCode
{
    public async Task FunctionHandler(SQSEvent evnt, ILambdaContext context)
    {
        foreach (var message in evnt.Records)
        {
            await ProcessMessageAsync(message, context);
        }

        context.Logger.LogInformation("done");
    }

    private async Task ProcessMessageAsync(SQSEvent.SQSMessage message, ILambdaContext context)
    {
        try
        {
            context.Logger.LogInformation($"Processed message {message.Body}");

            // TODO: Do interesting work based on the new message
            await Task.CompletedTask;
        }
        catch (Exception e)
        {
            //You can use Dead Letter Queue to handle failures. By configuring a Lambda DLQ.
            context.Logger.LogError($"An error occurred");
            throw;
        }

    }
}
```

------
#### [ Go ]

**SDK for Go V2**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [Serverless examples](https://github.com/aws-samples/serverless-snippets/tree/main/integration-sqs-to-lambda) repository. 
Consuming an SQS event with Lambda using Go.  

```
// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0
package integration_sqs_to_lambda

import (
	"fmt"
	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
)

func handler(event events.SQSEvent) error {
	for _, record := range event.Records {
		err := processMessage(record)
		if err != nil {
			return err
		}
	}
	fmt.Println("done")
	return nil
}

func processMessage(record events.SQSMessage) error {
	fmt.Printf("Processed message %s\n", record.Body)
	// TODO: Do interesting work based on the new message
	return nil
}

func main() {
	lambda.Start(handler)
}
```

------
#### [ Java ]

**SDK for Java 2.x**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [Serverless examples](https://github.com/aws-samples/serverless-snippets/tree/main/integration-sqs-to-lambda) repository. 
Consuming an SQS event with Lambda using Java.  

```
// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0
import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.SQSEvent;
import com.amazonaws.services.lambda.runtime.events.SQSEvent.SQSMessage;

public class Function implements RequestHandler<SQSEvent, Void> {
    @Override
    public Void handleRequest(SQSEvent sqsEvent, Context context) {
        for (SQSMessage msg : sqsEvent.getRecords()) {
            processMessage(msg, context);
        }
        context.getLogger().log("done");
        return null;
    }

    private void processMessage(SQSMessage msg, Context context) {
        try {
            context.getLogger().log("Processed message " + msg.getBody());

            // TODO: Do interesting work based on the new message

        } catch (Exception e) {
            context.getLogger().log("An error occurred");
            throw e;
        }

    }
}
```

------
#### [ JavaScript ]

**SDK for JavaScript (v3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [Serverless examples](https://github.com/aws-samples/serverless-snippets/blob/main/integration-sqs-to-lambda) repository. 
Consuming an SQS event with Lambda using JavaScript.  

```
// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0
exports.handler = async (event, context) => {
  for (const message of event.Records) {
    await processMessageAsync(message);
  }
  console.info("done");
};

async function processMessageAsync(message) {
  try {
    console.log(`Processed message ${message.body}`);
    // TODO: Do interesting work based on the new message
    await Promise.resolve(1); //Placeholder for actual async work
  } catch (err) {
    console.error("An error occurred");
    throw err;
  }
}
```
Consuming an SQS event with Lambda using TypeScript.  

```
// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0
import { SQSEvent, Context, SQSHandler, SQSRecord } from "aws-lambda";

export const functionHandler: SQSHandler = async (
  event: SQSEvent,
  context: Context
): Promise<void> => {
  for (const message of event.Records) {
    await processMessageAsync(message);
  }
  console.info("done");
};

async function processMessageAsync(message: SQSRecord): Promise<any> {
  try {
    console.log(`Processed message ${message.body}`);
    // TODO: Do interesting work based on the new message
    await Promise.resolve(1); //Placeholder for actual async work
  } catch (err) {
    console.error("An error occurred");
    throw err;
  }
}
```

------
#### [ PHP ]

**SDK for PHP**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [Serverless examples](https://github.com/aws-samples/serverless-snippets/tree/main/integration-sqs-to-lambda) repository. 
Consuming an SQS event with Lambda using PHP.  

```
// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0
<?php

# using bref/bref and bref/logger for simplicity

use Bref\Context\Context;
use Bref\Event\InvalidLambdaEvent;
use Bref\Event\Sqs\SqsEvent;
use Bref\Event\Sqs\SqsHandler;
use Bref\Logger\StderrLogger;

require __DIR__ . '/vendor/autoload.php';

class Handler extends SqsHandler
{
    private StderrLogger $logger;
    public function __construct(StderrLogger $logger)
    {
        $this->logger = $logger;
    }

    /**
     * @throws InvalidLambdaEvent
     */
    public function handleSqs(SqsEvent $event, Context $context): void
    {
        foreach ($event->getRecords() as $record) {
            $body = $record->getBody();
            // TODO: Do interesting work based on the new message
        }
    }
}

$logger = new StderrLogger();
return new Handler($logger);
```

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [Serverless examples](https://github.com/aws-samples/serverless-snippets/tree/main/integration-sqs-to-lambda) repository. 
Consuming an SQS event with Lambda using Python.  

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
def lambda_handler(event, context):
    for message in event['Records']:
        process_message(message)
    print("done")

def process_message(message):
    try:
        print(f"Processed message {message['body']}")
        # TODO: Do interesting work based on the new message
    except Exception as err:
        print("An error occurred")
        raise err
```

------
#### [ Ruby ]

**SDK for Ruby**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [Serverless examples](https://github.com/aws-samples/serverless-snippets/tree/main/integration-sqs-to-lambda) repository. 
Consuming an SQS event with Lambda using Ruby.  

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
def lambda_handler(event:, context:)
  event['Records'].each do |message|
    process_message(message)
  end
  puts "done"
end

def process_message(message)
  begin
    puts "Processed message #{message['body']}"
    # TODO: Do interesting work based on the new message
  rescue StandardError => err
    puts "An error occurred"
    raise err
  end
end
```

------
#### [ Rust ]

**SDK for Rust**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [Serverless examples](https://github.com/aws-samples/serverless-snippets/tree/main/integration-sqs-to-lambda) repository. 
Consuming an SQS event with Lambda using Rust.  

```
// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0
use aws_lambda_events::event::sqs::SqsEvent;
use lambda_runtime::{run, service_fn, Error, LambdaEvent};

async fn function_handler(event: LambdaEvent<SqsEvent>) -> Result<(), Error> {
    event.payload.records.iter().for_each(|record| {
        // process the record
        tracing::info!("Message body: {}", record.body.as_deref().unwrap_or_default())
    });

    Ok(())
}

#[tokio::main]
async fn main() -> Result<(), Error> {
    tracing_subscriber::fmt()
        .with_max_level(tracing::Level::INFO)
        // disable printing the name of the module in every log line.
        .with_target(false)
        // disabling time is handy because CloudWatch will add the ingestion time.
        .without_time()
        .init();

    run(service_fn(function_handler)).await
}
```

------

**To create a Node.js Lambda function**

1. Create a directory for the project, and then switch to that directory.

   ```
   mkdir sqs-tutorial
   cd sqs-tutorial
   ```

1. Copy the sample JavaScript code into a new file named `index.js`.

1. Create a deployment package using the following `zip` command.

   ```
   zip function.zip index.js
   ```

1. Create a Lambda function using the [create-function](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lambda/create-function.html) AWS CLI command. For the `role` parameter, enter the ARN of the execution role that you created earlier.
**Note**  
The Lambda function and the Amazon SQS queue must be in the same AWS Region.

   ```
   aws lambda create-function --function-name ProcessSQSRecord \
   --zip-file fileb://function.zip --handler index.handler --runtime nodejs24.x \
   --role arn:aws:iam::{{111122223333}}:role/lambda-sqs-role
   ```

## Test the function
<a name="with-sqs-create-test-function"></a>

![Step 3 test the Lambda function](http://docs.aws.amazon.com/lambda/latest/dg/images/sqs_tut_steps3.png)


Invoke your Lambda function manually using the `invoke` AWS CLI command and a sample Amazon SQS event.

**To invoke the Lambda function with a sample event**

1. Save the following JSON as a file named `input.json`. This JSON simulates an event that Amazon SQS might send to your Lambda function, where `"body"` contains the actual message from the queue. In this example, the message is `"test"`.  
**Example Amazon SQS event**  

   This is a test event—you don't need to change the message or the account number.

   ```
   {
       "Records": [
           {
               "messageId": "059f36b4-87a3-44ab-83d2-661975830a7d",
               "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
               "body": "test",
               "attributes": {
                   "ApproximateReceiveCount": "1",
                   "SentTimestamp": "1545082649183",
                   "SenderId": "AIDAIENQZJOLO23YVJ4VO",
                   "ApproximateFirstReceiveTimestamp": "1545082649185"
               },
               "messageAttributes": {},
               "md5OfBody": "098f6bcd4621d373cade4e832627b4f6",
               "eventSource": "aws:sqs",
               "eventSourceARN": "arn:aws:sqs:us-east-1:111122223333:my-queue",
               "awsRegion": "us-east-1"
           }
       ]
   }
   ```

1. Run the following [invoke](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lambda/invoke.html) AWS CLI command. This command returns CloudWatch logs in the response. For more information about retrieving logs, see [Access logs with the AWS CLI](monitoring-cloudwatchlogs-view.md#monitoring-cloudwatchlogs-cli).

   ```
   aws lambda invoke --function-name ProcessSQSRecord --payload file://input.json out --log-type Tail \
   --query 'LogResult' --output text --cli-binary-format raw-in-base64-out | base64 --decode
   ```

   The **cli-binary-format** option is required if you're using AWS CLI version 2. To make this the default setting, run `aws configure set cli-binary-format raw-in-base64-out`. For more information, see [AWS CLI supported global command line options](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-options.html#cli-configure-options-list) in the *AWS Command Line Interface User Guide for Version 2*.

1. Find the `INFO` log in the response. This is where the Lambda function logs the message body. You should see logs that look like this:

   ```
   2023-09-11T22:45:04.271Z	348529ce-2211-4222-9099-59d07d837b60	INFO	Processed message test
   2023-09-11T22:45:04.288Z	348529ce-2211-4222-9099-59d07d837b60	INFO	done
   ```

## Create an Amazon SQS queue
<a name="with-sqs-configure-sqs"></a>

![Step 4 create the Amazon SQS queue](http://docs.aws.amazon.com/lambda/latest/dg/images/sqs_tut_steps4.png)


Create an Amazon SQS queue that the Lambda function can use as an event source. The Lambda function and the Amazon SQS queue must be in the same AWS Region.

**To create a queue**

1. Open the [Amazon SQS console](https://console.aws.amazon.com/sqs).

1. Choose **Create queue**.

1. Enter a name for the queue. Leave all other options at the default settings.

1. Choose **Create queue**.

After creating the queue, note down its ARN. You need this in the next step when you associate the queue with your Lambda function.

## Configure the event source
<a name="with-sqs-attach-notification-configuration"></a>

![Step 5 configure event source mapping](http://docs.aws.amazon.com/lambda/latest/dg/images/sqs_tut_steps5.png)


Connect the Amazon SQS queue to your Lambda function by creating an [event source mapping](invocation-eventsourcemapping.md). The event source mapping reads the Amazon SQS queue and invokes your Lambda function when a new message is added.

To create a mapping between your Amazon SQS queue and your Lambda function, use the [create-event-source-mapping](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lambda/create-event-source-mapping.html) AWS CLI command. Example:

```
aws lambda create-event-source-mapping --function-name ProcessSQSRecord  --batch-size 10 \
--event-source-arn arn:aws:sqs:{{us-east-1:111122223333:my-queue}}
```

To get a list of your event source mappings, use the [list-event-source-mappings](https://awscli.amazonaws.com/v2/documentation/api/2.1.29/reference/lambda/list-event-source-mappings.html) command. Example:

```
aws lambda list-event-source-mappings --function-name ProcessSQSRecord
```

## Send a test message
<a name="with-sqs-test-message"></a>

![Step 6 send test message](http://docs.aws.amazon.com/lambda/latest/dg/images/sqs_tut_steps6.png)


**To send an Amazon SQS message to the Lambda function**

1. Open the [Amazon SQS console](https://console.aws.amazon.com/sqs).

1. Choose the queue that you created earlier.

1. Choose **Send and receive messages**.

1. Under **Message body**, enter a test message, such as "this is a test message."

1. Choose **Send message**.

Lambda polls the queue for updates. When there is a new message, Lambda invokes your function with this new event data from the queue. If the function handler returns without exceptions, Lambda considers the message successfully processed and begins reading new messages in the queue. After successfully processing a message, Lambda automatically deletes it from the queue. If the handler throws an exception, Lambda considers the batch of messages not successfully processed, and Lambda invokes the function with the same batch of messages.

## Check the CloudWatch logs
<a name="with-sqs-check-logs"></a>

![Step 6 send test message](http://docs.aws.amazon.com/lambda/latest/dg/images/sqs_tut_steps7.png)


**To confirm that the function processed the message**

1. Open the [Functions page](https://console.aws.amazon.com/lambda/home#/functions) of the Lambda console.

1. Choose the **ProcessSQSRecord** function.

1. Choose **Monitor**.

1. Choose **View CloudWatch logs**.

1. In the CloudWatch console, choose the **Log stream** for the function.

1. Find the `INFO` log. This is where the Lambda function logs the message body. You should see the message that you sent from the Amazon SQS queue. Example:

   ```
   2023-09-11T22:49:12.730Z b0c41e9c-0556-5a8b-af83-43e59efeec71 INFO Processed message this is a test message.
   ```

## Clean up your resources
<a name="cleanup"></a>

You can now delete the resources that you created for this tutorial, unless you want to retain them. By deleting AWS resources that you're no longer using, you prevent unnecessary charges to your AWS account.

**To delete the execution role**

1. Open the [Roles page](https://console.aws.amazon.com/iam/home#/roles) of the IAM console.

1. Select the execution role that you created.

1. Choose **Delete**.

1. Enter the name of the role in the text input field and choose **Delete**.

**To delete the Lambda function**

1. Open the [Functions page](https://console.aws.amazon.com/lambda/home#/functions) of the Lambda console.

1. Select the function that you created.

1. Choose **Actions**, **Delete**.

1. Type **confirm** in the text input field and choose **Delete**.

**To delete the Amazon SQS queue**

1. Sign in to the AWS Management Console and open the Amazon SQS console at [https://console.aws.amazon.com/sqs/](https://console.aws.amazon.com/sqs/).

1. Select the queue you created.

1. Choose **Delete**.

1. Enter **confirm** in the text input field.

1. Choose **Delete**.