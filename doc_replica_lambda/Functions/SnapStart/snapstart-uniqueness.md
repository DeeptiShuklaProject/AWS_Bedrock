

# Handling uniqueness with Lambda SnapStart
<a name="snapstart-uniqueness"></a>

When invocations scale up on a SnapStart function, Lambda uses a single initialized snapshot to resume multiple execution environments. If your initialization code generates unique content that is included in the snapshot, then the content might not be unique when it is reused across execution environments. To maintain uniqueness when using SnapStart, you must generate unique content after initialization. This includes unique IDs, unique secrets, and entropy that's used to generate pseudorandomness.

We recommend the following best practices to help you maintain uniqueness in your code. For Java functions, Lambda also provides an open-source [SnapStart scanning tool](#snapstart-scanning) to help check for code that assumes uniqueness. If you generate unique data during the initialization phase, then you can use a [runtime hook](snapstart-runtime-hooks.md) to restore uniqueness. With runtime hooks, you can run specific code immediately before Lambda takes a snapshot or immediately after Lambda resumes a function from a snapshot.

## Avoid saving state that depends on uniqueness during initialization
<a name="snapstart-caching-unique"></a>

During the [initialization phase](lambda-runtime-environment.md#runtimes-lifecycle-ib) of your function, avoid caching data that's intended to be unique, such as generating a unique ID for logging or setting seeds for random functions. Instead, we recommend that you generate unique data or set seeds for random functions inside your function handler—or use a [runtime hook](snapstart-runtime-hooks.md).

The following examples demonstrate how to generate a UUID in the function handler.

------
#### [ Java ]

**Example – Generating a unique ID in function handler**  

```
import java.util.UUID;
  public class Handler implements RequestHandler<String, String> {
    private static UUID uniqueSandboxId = null;
    @Override
    public String handleRequest(String event, Context context) {
      if (uniqueSandboxId == null)
        uniqueSandboxId = UUID.randomUUID();
      System.out.println("Unique Sandbox Id: " + uniqueSandboxId);
      return "Hello, World!";
    }
  }
```

------
#### [ Python ]

**Example – Generating a unique ID in function handler**  

```
import json
import random
import time

unique_number = None

def lambda_handler(event, context):
    seed = int(time.time() * 1000) 
    random.seed(seed)
    global unique_number
    if not unique_number:
        unique_number = random.randint(1, 10000)
        
    print("Unique number: ", unique_number)
    
    return "Hello, World!"
```

------
#### [ .NET ]

**Example – Generating a unique ID in function handler**  

```
namespace Example;
public class SnapstartExample
{
    private Guid _myExecutionEnvironmentGuid;
    public SnapstartExample()
    {
        // This GUID is set for non-restore use cases, such as testing or if SnapStart is turned off
        _myExecutionEnvironmentGuid = new Guid();
        // Register the method which will run after each restore. You may need to update Amazon.Lambda.Core to see this
        Amazon.Lambda.Core.SnapshotRestore.RegisterAfterRestore(MyAfterRestore);
    }

    private ValueTask MyAfterRestore()
    {
        // After restoring this snapshot to a new execution environment, update the GUID
        _myExecutionEnvironmentGuid = new Guid();
        return ValueTask.CompletedTask;
    }

    public string Handler()
    {
        return $"Hello World! My Execution Environment GUID is {_myExecutionEnvironmentGuid}";
    }
}
```

------

## Use cryptographically secure pseudorandom number generators (CSPRNGs)
<a name="snapstart-csprng"></a>

If your application depends on randomness, we recommend that you use cryptographically secure random number generators (CSPRNGs). In addition to OpenSSL 1.0.2, the Lambda managed runtimes also include the following built-in CSPRNGs:
+ **Java:** `java.security.SecureRandom`
+ **Python:** `random.SystemRandom`
+ **.NET:** `System.Security.Cryptography.RandomNumberGenerator`

Software that always gets random numbers from `/dev/random` or `/dev/urandom` also maintains randomness with SnapStart.

AWS cryptography libraries automatically maintain randomness with SnapStart beginning with the minimum versions specified in the following table. If you use these libraries with your Lambda functions, make sure that you use the following minimum versions or later versions:


****  

| Library | Minimum supported version (x86) | Minimum supported version (ARM) | 
| --- | --- | --- | 
| AWS libcrypto (AWS-LC) | 1.16.0 | 1.30.0 | 
| AWS libcrypto FIPS | 2.0.13 | 2.0.13 | 

If you package the preceding cryptographic libraries with your Lambda functions as transitive dependencies through the following libraries, make sure that you use the following minimum versions or later versions:


****  

| Library | Minimum supported version (x86) | Minimum supported version (ARM) | 
| --- | --- | --- | 
| AWS SDK for Java 2.x | 2.23.20 | 2.26.12 | 
| AWS Common Runtime for Java | 0.29.8 | 0.29.25 | 
| Amazon Corretto Crypto Provider | 2.4.1 | 2.4.1 | 
| Amazon Corretto Crypto Provider FIPS | 2.4.1 | 2.4.1 | 

The following examples demonstrate how to use CSPRNGs to guarantee unique number sequences even when the function is restored from a snapshot.

------
#### [ Java ]

**Example – java.security.SecureRandom**  

```
import java.security.SecureRandom;
  public class Handler implements RequestHandler<String, String> {
    private static SecureRandom rng = new SecureRandom();
    @Override
    public String handleRequest(String event, Context context) {
      for (int i = 0; i < 10; i++) {
        System.out.println(rng.next());
      }
      return "Hello, World!";
    }
  }
```

------
#### [ Python ]

**Example – random.SystemRandom**  

```
import json
import random

secure_rng = random.SystemRandom()

def lambda_handler(event, context):
    random_numbers = [secure_rng.random() for _ in range(10)]
    
    for number in random_numbers:
        print(number)
    
    return "Hello, World!"
```

------
#### [ .NET ]

**Example – RandomNumberGenerator**  

```
using Amazon.Lambda.Core;
using System.Security.Cryptography;
[assembly: LambdaSerializer(typeof(Amazon.Lambda.Serialization.SystemTextJson.DefaultLambdaJsonSerializer))]

namespace DotnetSecureRandom;

public class Function
{
    public string FunctionHandler()
    {
        using (RandomNumberGenerator rng = RandomNumberGenerator.Create())
        {
            byte[] randomUnsignedInteger32Bytes = new byte[4];
            for (int i = 0; i < 10; i++)
            {
                rng.GetBytes(randomUnsignedInteger32Bytes);
                int randomInt32 = BitConverter.ToInt32(randomUnsignedInteger32Bytes, 0);
                Console.WriteLine("{0:G}", randomInt32);
            }
        }
        return "Hello World!";
    }
}
```

------

## SnapStart scanning tool (Java only)
<a name="snapstart-scanning"></a>

Lambda provides a scanning tool for Java to help you check for code that assumes uniqueness. The SnapStart scanning tool is an open-source [SpotBugs](https://spotbugs.github.io/) plugin that runs a static analysis against a set of rules. The scanning tool helps identify potential code implementations that might break assumptions regarding uniqueness. For installation instructions and a list of checks that the scanning tool performs, see the [aws-lambda-snapstart-java-rules](https://github.com/aws/aws-lambda-snapstart-java-rules) repository on GitHub.

To learn more about handling uniqueness with SnapStart, see [Starting up faster with AWS Lambda SnapStart](https://aws.amazon.com/blogs/compute/starting-up-faster-with-aws-lambda-snapstart/) on the AWS Compute Blog.