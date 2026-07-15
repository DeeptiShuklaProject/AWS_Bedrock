

# Examples and use cases
<a name="durable-examples"></a>

Lambda durable functions enable you to build fault-tolerant, multi-step applications using durable operations like steps and waits. With automatic checkpointing and a checkpoint-replay model, where execution restarts from the beginning after failure but skips completed checkpoints, your functions can recover from failures and resume execution without losing progress.

**Note**  
For the SDK API reference, quickstart tutorials, language-specific guides, and additional workflow patterns, see the [AWS Durable Execution SDK Developer Guide](https://docs.aws.amazon.com/durable-execution/).

## Short-lived fault-tolerant processes
<a name="durable-examples-short-lived"></a>

Use durable functions to build reliable operations that typically complete within minutes. While these processes are shorter than long-running workflows, they still benefit from automatic checkpointing and fault tolerance across distributed systems. Durable functions help ensure your multi-step processes complete successfully even when individual service calls fail, without requiring complex error handling or state management code.

Common scenarios include hotel booking systems, restaurant reservation platforms, ride-sharing trip requests, event ticket purchases, and SaaS subscription upgrades. These scenarios share common characteristics: multiple service calls that must complete together, the need for automatic retry on transient failures, and the requirement to maintain consistent state across distributed systems.

### Distributed transactions across microservices
<a name="durable-examples-distributed-transactions"></a>

Coordinate payments, inventory, and shipping across multiple services with automatic rollback on failures. Each service operation is wrapped in a step, ensuring the transaction can recover from any point if a service fails.

------
#### [ TypeScript ]

```
import { DurableContext, withDurableExecution } from "@aws/durable-execution-sdk-js";

export const handler = withDurableExecution(
  async (event: any, context: DurableContext) => {
    const { orderId, amount, items } = event;
    
    // Reserve inventory across multiple warehouses
    const inventory = await context.step("reserve-inventory", async () => {
      return await inventoryService.reserve(items);
    });
    
    // Process payment
    const payment = await context.step("process-payment", async () => {
      return await paymentService.charge(amount);
    });
    
    // Create shipment
    const shipment = await context.step("create-shipment", async () => {
      return await shippingService.createShipment(orderId, inventory);
    });
    
    return { orderId, status: 'completed', shipment };
  }
);
```

------
#### [ Python ]

```
from aws_durable_execution_sdk_python import DurableContext, durable_execution

@durable_execution
def lambda_handler(event, context: DurableContext):
    order_id = event['orderId']
    amount = event['amount']
    items = event['items']
    
    # Reserve inventory across multiple warehouses
    inventory = context.step(
        lambda _: inventory_service.reserve(items),
        name='reserve-inventory'
    )
    
    # Process payment
    payment = context.step(
        lambda _: payment_service.charge(amount),
        name='process-payment'
    )
    
    # Create shipment
    shipment = context.step(
        lambda _: shipping_service.create_shipment(order_id, inventory),
        name='create-shipment'
    )
    
    return {'orderId': order_id, 'status': 'completed', 'shipment': shipment}
```

------

If any step fails, the function automatically retries from the last successful checkpoint. The inventory reservation persists even if payment processing fails temporarily. When the function retries, it skips the completed inventory step and proceeds directly to payment processing. This eliminates duplicate reservations and ensures consistent state across your distributed system.

### Order processing with multiple steps
<a name="durable-examples-order-processing"></a>

Process orders through validation, payment authorization, inventory allocation, and fulfillment with automatic retry and recovery. Each step is checkpointed, ensuring the order progresses even if individual steps fail and retry.

------
#### [ TypeScript ]

```
import { DurableContext, withDurableExecution } from "@aws/durable-execution-sdk-js";

export const handler = withDurableExecution(
  async (event: any, context: DurableContext) => {
    const { orderId, customerId, items } = event;
    
    // Validate order details
    const validation = await context.step("validate-order", async () => {
      const customer = await customerService.validate(customerId);
      const itemsValid = await inventoryService.validateItems(items);
      return { customer, itemsValid };
    });
    
    if (!validation.itemsValid) {
      return { orderId, status: 'rejected', reason: 'invalid_items' };
    }
    
    // Authorize payment
    const authorization = await context.step("authorize-payment", async () => {
      return await paymentService.authorize(
        validation.customer.paymentMethod,
        calculateTotal(items)
      );
    });
    
    // Allocate inventory
    const allocation = await context.step("allocate-inventory", async () => {
      return await inventoryService.allocate(items);
    });
    
    // Fulfill order
    const fulfillment = await context.step("fulfill-order", async () => {
      return await fulfillmentService.createShipment({
        orderId,
        items: allocation.allocatedItems,
        address: validation.customer.shippingAddress
      });
    });
    
    return {
      orderId,
      status: 'completed',
      trackingNumber: fulfillment.trackingNumber
    };
  }
);
```

------
#### [ Python ]

```
from aws_durable_execution_sdk_python import DurableContext, durable_execution

@durable_execution
def lambda_handler(event, context: DurableContext):
    order_id = event['orderId']
    customer_id = event['customerId']
    items = event['items']
    
    # Validate order details
    def validate_order(_):
        customer = customer_service.validate(customer_id)
        items_valid = inventory_service.validate_items(items)
        return {'customer': customer, 'itemsValid': items_valid}
    
    validation = context.step(validate_order, name='validate-order')
    
    if not validation['itemsValid']:
        return {'orderId': order_id, 'status': 'rejected', 'reason': 'invalid_items'}
    
    # Authorize payment
    authorization = context.step(
        lambda _: payment_service.authorize(
            validation['customer']['paymentMethod'],
            calculate_total(items)
        ),
        name='authorize-payment'
    )
    
    # Allocate inventory
    allocation = context.step(
        lambda _: inventory_service.allocate(items),
        name='allocate-inventory'
    )
    
    # Fulfill order
    fulfillment = context.step(
        lambda _: fulfillment_service.create_shipment({
            'orderId': order_id,
            'items': allocation['allocatedItems'],
            'address': validation['customer']['shippingAddress']
        }),
        name='fulfill-order'
    )
    
    return {
        'orderId': order_id,
        'status': 'completed',
        'trackingNumber': fulfillment['trackingNumber']
    }
```

------

This pattern ensures orders never get stuck in intermediate states. If validation fails, the order is rejected before payment authorization. If payment authorization fails, inventory isn't allocated. Each step builds on the previous one with automatic retry and recovery.

**Note**  
The conditional check `if (!validation.itemsValid)` is outside a step and will re-execute during replay. This is safe because it's deterministic—it always produces the same result given the same validation object.

## Long-running processes
<a name="durable-examples-long-running"></a>

Use durable functions for processes that span hours, days, or weeks. Wait operations suspend execution without incurring compute charges, making long-running processes cost-effective. During wait periods, your function stops running and Lambda recycles the execution environment. When it's time to resume, Lambda invokes your function again and replays from the last checkpoint.

This execution model makes durable functions ideal for processes that need to pause for extended periods, whether waiting for human decisions, external system responses, scheduled processing windows, or time-based delays. You pay only for active compute time, not for waiting.

Common scenarios include document approval processes, scheduled batch processing, multi-day onboarding processes, subscription trial processes, and delayed notification systems. These scenarios share common characteristics: extended wait periods measured in hours or days, the need to maintain execution state across those waits, and cost-sensitive requirements where paying for idle compute time is prohibitive.

### Human-in-the-loop approvals
<a name="durable-examples-human-in-loop"></a>

Pause execution for document reviews, approvals, or decisions while maintaining execution state. The function waits for external callbacks without consuming resources, resuming automatically when approval is received.

This pattern is essential for processes that require human judgment or external validation. The function suspends at the callback point, incurring no compute charges while waiting. When someone submits their decision via API, Lambda invokes your function again and replays from the checkpoint, continuing with the approval result.

------
#### [ TypeScript ]

```
import { DurableContext, withDurableExecution } from "@aws/durable-execution-sdk-js";

export const handler = withDurableExecution(
  async (event: any, context: DurableContext) => {
    const { documentId, reviewers } = event;
    
    // Step 1: Prepare document for review
    const prepared = await context.step("prepare-document", async () => {
      return await documentService.prepare(documentId);
    });
    
    // Step 2: Request approval with callback
    const approval = await context.waitForCallback(
      "approval-callback",
      async (callbackId) => {
        await notificationService.sendApprovalRequest({
          documentId,
          reviewers,
          callbackId,
          expiresIn: 86400
        });
      },
      {
        timeout: { seconds: 86400 }
      }
    );
    
    // Function resumes here when approval is received
    if (approval?.approved) {
      const finalized = await context.step("finalize-document", async () => {
        return await documentService.finalize(documentId, approval.comments);
      });
      
      return {
        status: 'approved',
        documentId,
        finalizedAt: finalized.timestamp
      };
    }
    
    // Handle rejection
    await context.step("archive-rejected", async () => {
      await documentService.archive(documentId, approval?.reason);
    });
    
    return {
      status: 'rejected',
      documentId,
      reason: approval?.reason
    };
  }
);
```

------
#### [ Python ]

```
from aws_durable_execution_sdk_python import DurableContext, durable_execution, WaitConfig

@durable_execution
def lambda_handler(event, context: DurableContext):
    document_id = event['documentId']
    reviewers = event['reviewers']
    
    # Step 1: Prepare document for review
    prepared = context.step(
        lambda _: document_service.prepare(document_id),
        name='prepare-document'
    )
    
    # Step 2: Request approval with callback
    def send_approval_request(callback_id):
        notification_service.send_approval_request({
            'documentId': document_id,
            'reviewers': reviewers,
            'callbackId': callback_id,
            'expiresIn': 86400
        })
    
    approval = context.wait_for_callback(
        send_approval_request,
        name='approval-callback',
        config=WaitConfig(timeout=86400)
    )
    
    # Function resumes here when approval is received
    if approval and approval.get('approved'):
        finalized = context.step(
            lambda _: document_service.finalize(document_id, approval.get('comments')),
            name='finalize-document'
        )
        
        return {
            'status': 'approved',
            'documentId': document_id,
            'finalizedAt': finalized['timestamp']
        }
    
    # Handle rejection
    context.step(
        lambda _: document_service.archive(document_id, approval.get('reason') if approval else None),
        name='archive-rejected'
    )
    
    return {
        'status': 'rejected',
        'documentId': document_id,
        'reason': approval.get('reason') if approval else None
    }
```

------

When the callback is received and your function resumes, it replays from the beginning. The prepare-document step returns its checkpointed result instantly. The waitForCallback operation also returns instantly with the stored approval result instead of waiting again. Execution then continues to the finalization or archival steps.

### Multi-stage data pipelines
<a name="durable-examples-data-pipelines"></a>

Process large datasets through extraction, transformation, and loading phases with checkpoints between stages. Each stage can take hours to complete, and checkpoints enable the pipeline to resume from any stage if interrupted.

This pattern is ideal for ETL workflows, data migrations, or batch processing jobs where you need to process data in stages with recovery points between them. If a stage fails, the pipeline resumes from the last completed stage rather than restarting from the beginning. You can also use wait operations to pause between stages; respecting rate limits, waiting for downstream systems to be ready, or scheduling processing during off-peak hours.

------
#### [ TypeScript ]

```
import { DurableContext, withDurableExecution } from "@aws/durable-execution-sdk-js";

export const handler = withDurableExecution(
  async (event: any, context: DurableContext) => {
    const { datasetId, batchSize } = event;
    
    // Stage 1: Extract data from source
    const extracted = await context.step("extract-data", async () => {
      const records = await sourceDatabase.extractRecords(datasetId);
      return { recordCount: records.length, records };
    });
    
    // Wait 5 minutes to respect source system rate limits
    await context.wait({ seconds: 300 });
    
    // Stage 2: Transform data in batches
    const transformed = await context.step("transform-data", async () => {
      const batches = chunkArray(extracted.records, batchSize);
      const results = [];
      
      for (const batch of batches) {
        const transformed = await transformService.processBatch(batch);
        results.push(transformed);
      }
      
      return { batchCount: batches.length, results };
    });
    
    // Wait until off-peak hours (e.g., 2 AM)
    const now = new Date();
    const targetHour = 2;
    const msUntilTarget = calculateMsUntilHour(now, targetHour);
    await context.wait({ seconds: Math.floor(msUntilTarget / 1000) });
    
    // Stage 3: Load data to destination
    const loaded = await context.step("load-data", async () => {
      let loadedCount = 0;
      
      for (const result of transformed.results) {
        await destinationDatabase.loadBatch(result);
        loadedCount += result.length;
      }
      
      return { loadedCount };
    });
    
    // Stage 4: Verify and finalize
    const verified = await context.step("verify-pipeline", async () => {
      const verification = await destinationDatabase.verifyRecords(datasetId);
      await pipelineService.markComplete(datasetId, verification);
      return verification;
    });
    
    return {
      datasetId,
      recordsProcessed: extracted.recordCount,
      batchesProcessed: transformed.batchCount,
      recordsLoaded: loaded.loadedCount,
      verified: verified.success
    };
  }
);
```

------
#### [ Python ]

```
from aws_durable_execution_sdk_python import DurableContext, durable_execution
from datetime import datetime

@durable_execution
def lambda_handler(event, context: DurableContext):
    dataset_id = event['datasetId']
    batch_size = event['batchSize']
    
    # Stage 1: Extract data from source
    def extract_data(_):
        records = source_database.extract_records(dataset_id)
        return {'recordCount': len(records), 'records': records}
    
    extracted = context.step(extract_data, name='extract-data')
    
    # Wait 5 minutes to respect source system rate limits
    context.wait(Duration.from_seconds(300))
    
    # Stage 2: Transform data in batches
    def transform_data(_):
        batches = chunk_array(extracted['records'], batch_size)
        results = []
        
        for batch in batches:
            transformed = transform_service.process_batch(batch)
            results.append(transformed)
        
        return {'batchCount': len(batches), 'results': results}
    
    transformed = context.step(transform_data, name='transform-data')
    
    # Wait until off-peak hours (e.g., 2 AM)
    now = datetime.now()
    target_hour = 2
    ms_until_target = calculate_ms_until_hour(now, target_hour)
    context.wait(ms_until_target // 1000)
    
    # Stage 3: Load data to destination
    def load_data(_):
        loaded_count = 0
        
        for result in transformed['results']:
            destination_database.load_batch(result)
            loaded_count += len(result)
        
        return {'loadedCount': loaded_count}
    
    loaded = context.step(load_data, name='load-data')
    
    # Stage 4: Verify and finalize
    def verify_pipeline(_):
        verification = destination_database.verify_records(dataset_id)
        pipeline_service.mark_complete(dataset_id, verification)
        return verification
    
    verified = context.step(verify_pipeline, name='verify-pipeline')
    
    return {
        'datasetId': dataset_id,
        'recordsProcessed': extracted['recordCount'],
        'batchesProcessed': transformed['batchCount'],
        'recordsLoaded': loaded['loadedCount'],
        'verified': verified['success']
    }
```

------

Each stage is wrapped in a step, creating a checkpoint that allows the pipeline to resume from any stage if interrupted. The 5-minute wait between extract and transform respects source system rate limits without consuming compute resources, while the wait until 2 AM schedules the expensive load operation during off-peak hours.

**Note**  
The `new Date()` call and `calculateMsUntilHour()` function are outside steps and will re-execute during replay. For time-based operations that must be consistent across replays, calculate the timestamp inside a step or use it only for wait durations (which are checkpointed).

## Advanced patterns
<a name="durable-examples-advanced"></a>

Use durable functions to build complex multi-step applications that combine multiple durable operations, parallel execution, array processing, conditional logic, and polling. These patterns let you build sophisticated applications that coordinate many tasks while maintaining fault tolerance and automatic recovery.

Advanced patterns go beyond simple sequential steps. You can run operations concurrently with `parallel()`, process arrays with `map()`, wait for external conditions with `waitForCondition()`, and combine these primitives to build reliable applications. Each durable operation creates its own checkpoints, so your application can recover from any point if interrupted.

### User onboarding processes
<a name="durable-examples-user-onboarding"></a>

Guide users through registration, email verification, profile setup, and initial configuration with retry handling. This example combines sequential steps, callbacks, and conditional logic to create a complete onboarding process.

------
#### [ TypeScript ]

```
import { DurableContext, withDurableExecution } from "@aws/durable-execution-sdk-js";

export const handler = withDurableExecution(
  async (event: any, context: DurableContext) => {
    const { userId, email } = event;
    
    // Step 1: Create user account
    const user = await context.step("create-account", async () => {
      return await userService.createAccount(userId, email);
    });
    
    // Step 2: Send verification email
    await context.step("send-verification", async () => {
      return await emailService.sendVerification(email);
    });
    
    // Step 3: Wait for email verification (up to 48 hours)
    const verified = await context.waitForCallback(
      "email-verification",
      async (callbackId) => {
        await notificationService.sendVerificationLink({
          email,
          callbackId,
          expiresIn: 172800
        });
      },
      {
        timeout: { seconds: 172800 }
      }
    );
    
    if (!verified) {
      await context.step("send-reminder", async () => {
        await emailService.sendReminder(email);
      });
      
      return {
        status: "verification_timeout",
        userId,
        message: "Email verification not completed within 48 hours"
      };
    }
    
    // Step 4: Initialize user profile in parallel
    const setupResults = await context.parallel("profile-setup", [
      async (ctx: DurableContext) => {
        return await ctx.step("create-preferences", async () => {
          return await preferencesService.createDefaults(userId);
        });
      },
      
      async (ctx: DurableContext) => {
        return await ctx.step("setup-notifications", async () => {
          return await notificationService.setupDefaults(userId);
        });
      },
      
      async (ctx: DurableContext) => {
        return await ctx.step("create-welcome-content", async () => {
          return await contentService.createWelcome(userId);
        });
      }
    ]);
    
    // Step 5: Send welcome email
    await context.step("send-welcome", async () => {
      const [preferences, notifications, content] = setupResults.getResults();
      return await emailService.sendWelcome({
        email,
        preferences,
        notifications,
        content
      });
    });
    
    return {
      status: "onboarding_complete",
      userId,
      completedAt: new Date().toISOString()
    };
  }
);
```

------
#### [ Python ]

```
from aws_durable_execution_sdk_python import DurableContext, durable_execution, WaitConfig
from datetime import datetime

@durable_execution
def lambda_handler(event, context: DurableContext):
    user_id = event['userId']
    email = event['email']
    
    # Step 1: Create user account
    user = context.step(
        lambda _: user_service.create_account(user_id, email),
        name='create-account'
    )
    
    # Step 2: Send verification email
    context.step(
        lambda _: email_service.send_verification(email),
        name='send-verification'
    )
    
    # Step 3: Wait for email verification (up to 48 hours)
    def send_verification_link(callback_id):
        notification_service.send_verification_link({
            'email': email,
            'callbackId': callback_id,
            'expiresIn': 172800
        })
    
    verified = context.wait_for_callback(
        send_verification_link,
        name='email-verification',
        config=WaitConfig(timeout=172800)
    )
    
    if not verified:
        context.step(
            lambda _: email_service.send_reminder(email),
            name='send-reminder'
        )
        
        return {
            'status': 'verification_timeout',
            'userId': user_id,
            'message': 'Email verification not completed within 48 hours'
        }
    
    # Step 4: Initialize user profile in parallel
    def create_preferences(ctx: DurableContext):
        return ctx.step(
            lambda _: preferences_service.create_defaults(user_id),
            name='create-preferences'
        )
    
    def setup_notifications(ctx: DurableContext):
        return ctx.step(
            lambda _: notification_service.setup_defaults(user_id),
            name='setup-notifications'
        )
    
    def create_welcome_content(ctx: DurableContext):
        return ctx.step(
            lambda _: content_service.create_welcome(user_id),
            name='create-welcome-content'
        )
    
    setup_results = context.parallel(
        [create_preferences, setup_notifications, create_welcome_content],
        name='profile-setup'
    )
    
    # Step 5: Send welcome email
    def send_welcome(_):
        results = setup_results.get_results()
        preferences, notifications, content = results[0], results[1], results[2]
        return email_service.send_welcome({
            'email': email,
            'preferences': preferences,
            'notifications': notifications,
            'content': content
        })
    
    context.step(send_welcome, name='send-welcome')
    
    return {
        'status': 'onboarding_complete',
        'userId': user_id,
        'completedAt': datetime.now().isoformat()
    }
```

------

The process combines sequential steps with checkpoints for account creation and email sending, then pauses for up to 48 hours waiting for email verification without consuming resources. Conditional logic handles different paths based on whether verification completes or times out. Profile setup tasks run concurrently using parallel operations to reduce total execution time, and each step retries automatically on transient failures to help ensure the onboarding completes reliably.

### Chained invocations across functions
<a name="durable-examples-chained-invocations"></a>

Invoke other Lambda functions from within a durable function using `context.invoke()`. The calling function suspends while waiting for the invoked function to complete, creating a checkpoint that preserves the result. If the calling function is interrupted after the invoked function completes, it resumes with the stored result without re-invoking the function.

Use this pattern when you have specialized functions that handle specific domains (customer validation, payment processing, inventory management) and need to coordinate them in a workflow. Each function maintains its own logic and can be invoked by multiple orchestrator functions, avoiding code duplication.

------
#### [ TypeScript ]

```
import { DurableContext, withDurableExecution } from "@aws/durable-execution-sdk-js";

// Main orchestrator function
export const handler = withDurableExecution(
  async (event: any, context: DurableContext) => {
    const { orderId, customerId } = event;
    
    // Step 1: Validate customer by invoking customer service function
    const customer = await context.invoke(
      "validate-customer",
      "arn:aws:lambda:us-east-1:123456789012:function:customer-service:1",
      { customerId }
    );
    
    if (!customer.isValid) {
      return { orderId, status: "rejected", reason: "invalid_customer" };
    }
    
    // Step 2: Check inventory by invoking inventory service function
    const inventory = await context.invoke(
      "check-inventory",
      "arn:aws:lambda:us-east-1:123456789012:function:inventory-service:1",
      { orderId, items: event.items }
    );
    
    if (!inventory.available) {
      return { orderId, status: "rejected", reason: "insufficient_inventory" };
    }
    
    // Step 3: Process payment by invoking payment service function
    const payment = await context.invoke(
      "process-payment",
      "arn:aws:lambda:us-east-1:123456789012:function:payment-service:1",
      {
        customerId,
        amount: inventory.totalAmount,
        paymentMethod: customer.paymentMethod
      }
    );
    
    // Step 4: Create shipment by invoking fulfillment service function
    const shipment = await context.invoke(
      "create-shipment",
      "arn:aws:lambda:us-east-1:123456789012:function:fulfillment-service:1",
      {
        orderId,
        items: inventory.allocatedItems,
        address: customer.shippingAddress
      }
    );
    
    return {
      orderId,
      status: "completed",
      trackingNumber: shipment.trackingNumber,
      estimatedDelivery: shipment.estimatedDelivery
    };
  }
);
```

------
#### [ Python ]

```
from aws_durable_execution_sdk_python import DurableContext, durable_execution

# Main orchestrator function
@durable_execution
def lambda_handler(event, context: DurableContext):
    order_id = event['orderId']
    customer_id = event['customerId']
    
    # Step 1: Validate customer by invoking customer service function
    customer = context.invoke(
        'arn:aws:lambda:us-east-1:123456789012:function:customer-service:1',
        {'customerId': customer_id},
        name='validate-customer'
    )
    
    if not customer['isValid']:
        return {'orderId': order_id, 'status': 'rejected', 'reason': 'invalid_customer'}
    
    # Step 2: Check inventory by invoking inventory service function
    inventory = context.invoke(
        'arn:aws:lambda:us-east-1:123456789012:function:inventory-service:1',
        {'orderId': order_id, 'items': event['items']},
        name='check-inventory'
    )
    
    if not inventory['available']:
        return {'orderId': order_id, 'status': 'rejected', 'reason': 'insufficient_inventory'}
    
    # Step 3: Process payment by invoking payment service function
    payment = context.invoke(
        'arn:aws:lambda:us-east-1:123456789012:function:payment-service:1',
        {
            'customerId': customer_id,
            'amount': inventory['totalAmount'],
            'paymentMethod': customer['paymentMethod']
        },
        name='process-payment'
    )
    
    # Step 4: Create shipment by invoking fulfillment service function
    shipment = context.invoke(
        'arn:aws:lambda:us-east-1:123456789012:function:fulfillment-service:1',
        {
            'orderId': order_id,
            'items': inventory['allocatedItems'],
            'address': customer['shippingAddress']
        },
        name='create-shipment'
    )
    
    return {
        'orderId': order_id,
        'status': 'completed',
        'trackingNumber': shipment['trackingNumber'],
        'estimatedDelivery': shipment['estimatedDelivery']
    }
```

------

Each invocation creates a checkpoint in the orchestrator function. If the orchestrator is interrupted after the customer validation completes, it resumes from that checkpoint with the stored customer data, skipping the validation invocation. This prevents duplicate calls to downstream services and ensures consistent execution across interruptions.

The invoked functions can be either durable or standard Lambda functions. If you invoke a durable function, it can have its own multi-step workflow with waits and checkpoints. The orchestrator simply waits for the complete durable execution to finish, receiving the final result.

**Note**  
Cross-account invocations are not supported. All invoked functions must be in the same AWS account as the calling function.

### Batch processing with checkpoints
<a name="durable-examples-batch-processing"></a>

Process millions of records with automatic recovery from the last successful checkpoint after failures. This example demonstrates how durable functions combine `map()` operations with chunking and rate limiting to handle large-scale data processing.

------
#### [ TypeScript ]

```
import { DurableContext, withDurableExecution } from "@aws/durable-execution-sdk-js";

interface Batch {
  batchIndex: number;
  recordIds: string[];
}

export const handler = withDurableExecution(
  async (event: any, context: DurableContext) => {
    const { datasetId, batchSize = 1000 } = event;
    
    // Step 1: Get all record IDs to process
    const recordIds = await context.step("fetch-record-ids", async () => {
      return await dataService.getRecordIds(datasetId);
    });
    
    // Step 2: Split into batches
    const batches: Batch[] = [];
    for (let i = 0; i < recordIds.length; i += batchSize) {
      batches.push({
        batchIndex: Math.floor(i / batchSize),
        recordIds: recordIds.slice(i, i + batchSize)
      });
    }
    
    // Step 3: Process batches with controlled concurrency
    const batchResults = await context.map(
      "process-batches",
      batches,
      async (ctx: DurableContext, batch: Batch, index: number) => {
        const processed = await ctx.step(`batch-${batch.batchIndex}`, async () => {
          const results = [];
          for (const recordId of batch.recordIds) {
            const result = await recordService.process(recordId);
            results.push(result);
          }
          return results;
        });
        
        const validated = await ctx.step(`validate-${batch.batchIndex}`, async () => {
          return await validationService.validateBatch(processed);
        });
        
        return {
          batchIndex: batch.batchIndex,
          recordCount: batch.recordIds.length,
          successCount: validated.successCount,
          failureCount: validated.failureCount
        };
      },
      {
        maxConcurrency: 5
      }
    );
    
    // Step 4: Aggregate results
    const summary = await context.step("aggregate-results", async () => {
      const results = batchResults.getResults();
      const totalSuccess = results.reduce((sum, r) => sum + r.successCount, 0);
      const totalFailure = results.reduce((sum, r) => sum + r.failureCount, 0);
      
      return {
        datasetId,
        totalRecords: recordIds.length,
        batchesProcessed: batches.length,
        successCount: totalSuccess,
        failureCount: totalFailure,
        completedAt: new Date().toISOString()
      };
    });
    
    return summary;
  }
);
```

------
#### [ Python ]

```
from aws_durable_execution_sdk_python import DurableContext, durable_execution, MapConfig
from datetime import datetime
from typing import List, Dict

@durable_execution
def lambda_handler(event, context: DurableContext):
    dataset_id = event['datasetId']
    batch_size = event.get('batchSize', 1000)
    
    # Step 1: Get all record IDs to process
    record_ids = context.step(
        lambda _: data_service.get_record_ids(dataset_id),
        name='fetch-record-ids'
    )
    
    # Step 2: Split into batches
    batches = []
    for i in range(0, len(record_ids), batch_size):
        batches.append({
            'batchIndex': i // batch_size,
            'recordIds': record_ids[i:i + batch_size]
        })
    
    # Step 3: Process batches with controlled concurrency
    def process_batch(ctx: DurableContext, batch: Dict, index: int):
        batch_index = batch['batchIndex']
        
        def process_records(_):
            results = []
            for record_id in batch['recordIds']:
                result = record_service.process(record_id)
                results.append(result)
            return results
        
        processed = ctx.step(process_records, name=f'batch-{batch_index}')
        
        validated = ctx.step(
            lambda _: validation_service.validate_batch(processed),
            name=f'validate-{batch_index}'
        )
        
        return {
            'batchIndex': batch_index,
            'recordCount': len(batch['recordIds']),
            'successCount': validated['successCount'],
            'failureCount': validated['failureCount']
        }
    
    batch_results = context.map(
        process_batch,
        batches,
        name='process-batches',
        config=MapConfig(max_concurrency=5)
    )
    
    # Step 4: Aggregate results
    def aggregate_results(_):
        results = batch_results.get_results()
        total_success = sum(r['successCount'] for r in results)
        total_failure = sum(r['failureCount'] for r in results)
        
        return {
            'datasetId': dataset_id,
            'totalRecords': len(record_ids),
            'batchesProcessed': len(batches),
            'successCount': total_success,
            'failureCount': total_failure,
            'completedAt': datetime.now().isoformat()
        }
    
    summary = context.step(aggregate_results, name='aggregate-results')
    
    return summary
```

------

Records are split into manageable batches to avoid overwhelming memory or downstream services, then multiple batches process concurrently with `maxConcurrency` controlling the parallelism. Each batch has its own checkpoint, so failures only retry the failed batch rather than reprocessing all records. This pattern is ideal for ETL jobs, data migrations, or bulk operations where processing can take hours.

## Next steps
<a name="durable-examples-next-steps"></a>
+ Explore [basic concepts](durable-basic-concepts.md) to understand DurableContext, steps, and waits
+ Review [best practices](durable-best-practices.md) for writing deterministic code and optimizing performance
+ Learn about [testing durable functions](durable-testing.md) locally and in the cloud
+ Compare durable functions with Step Functions to understand when each approach is most effective. See [Durable functions or Step Functions](durable-step-functions.md).