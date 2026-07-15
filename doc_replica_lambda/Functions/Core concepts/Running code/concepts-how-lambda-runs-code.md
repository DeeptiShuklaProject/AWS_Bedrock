

# Running code with Lambda
<a name="concepts-how-lambda-runs-code"></a>

When you write a Lambda function, you are creating code that will run in a unique serverless environment. Understanding how Lambda actually runs your code involves two key aspects: the programming model that defines how your code interacts with Lambda, and the execution environment lifecycle that determines how Lambda manages your code's runtime environment.

## The Lambda programming model
<a name="concepts-progmodel-overview"></a>

Programming model functions as a common set of rules for how Lambda works with your code, regardless of whether you're writing in Python, Java, or any other supported language. The programming model includes your runtime and handler.

**For standard functions:**

1. Lambda receives an event.

1. Lambda uses the runtime to prepare the event in a format your code can use.

1. The runtime sends the formatted event to your handler.

1. Your handler processes the event using the code you've written.

Essential to this model is the *handler*, where Lambda sends events to be processed by your code. Think of it as the entry point to your code. When Lambda receives an event, it passes this event and some context information to your handler. The handler then runs your code to process these events - for example, it might read a file when it's uploaded to Amazon S3, analyze an image, or update a database. Once your code finishes processing an event, the handler is ready to process the next one.

## The Lambda execution model
<a name="concepts-exec-env-overview"></a>

While the programming model defines how Lambda interacts with your code, Execution environment is where Lambda actually runs your function — it's a secure, isolated compute space created specifically for your function.

**Each environment follows a lifecycle:**

1. **Initialization:** Environment setup and code loading

1. **Invocation:** Single execution of function code

1. **Shutdown:** Environment cleanup

This environment handles important aspects of running your function. It provides your function with memory and a `/tmp` directory for temporary storage.