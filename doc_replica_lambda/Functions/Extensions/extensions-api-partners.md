

# AWS Lambda extensions partners
<a name="extensions-api-partners"></a>

AWS Lambda has partnered with several third party entities to provide extensions to integrate with your Lambda functions. The following list details third party extensions that are ready for you to use at any time.
+ [https://docs.appdynamics.com/display/PRO20X/Use+the+AppDynamics+AWS+Lambda+Extension+to+Instrument+Serverless+APM+at+Runtime](https://docs.appdynamics.com/display/PRO20X/Use+the+AppDynamics+AWS+Lambda+Extension+to+Instrument+Serverless+APM+at+Runtime) – Provides automatic instrumentation of Node.js or Python Lambda functions, providing visibility and alerting on function performance.
+ [https://axiom.co/docs/apps/lambda](https://axiom.co/docs/apps/lambda) – Provides dashboards for monitoring Lambda function performance and aggregate system-level metrics.
+ [https://docs.datadoghq.com/serverless/datadog_lambda_library/extension/](https://docs.datadoghq.com/serverless/datadog_lambda_library/extension/) – Provides comprehensive, real-time visibility to your serverless applications through the use of metrics, traces, and logs.
+ [https://www.dynatrace.com/support/help/technology-support/cloud-platforms/amazon-web-services/integrations/deploy-oneagent-as-lambda-extension/](https://www.dynatrace.com/support/help/technology-support/cloud-platforms/amazon-web-services/integrations/deploy-oneagent-as-lambda-extension/) – Provides visibility into traces and metrics, and leverages AI for automated error detection and root cause analysis across the entire application stack.
+ [https://www.elastic.co/guide/en/apm/agent/nodejs/current/lambda.html](https://www.elastic.co/guide/en/apm/agent/nodejs/current/lambda.html) – Provides Application Performance Monitoring (APM) to identify and resolve root cause issues using correlated traces, metrics, and logs.
+ [https://docs.epsagon.com/docs/environment-monitoring/lambda/intro](https://docs.epsagon.com/docs/environment-monitoring/lambda/intro) – Listens to invocation events, stores traces, and sends them in parallel to Lambda function executions.
+ [https://docs.fastly.com/signalsciences/install-guides/paas/aws-lambda/](https://docs.fastly.com/signalsciences/install-guides/paas/aws-lambda/)– Protects your Lambda functions from suspicious activity, such as injection-style attacks, account takeover via credential stuffing, malicious bots, and API abuse.
+ [https://learn.hashicorp.com/tutorials/vault/aws-lambda](https://learn.hashicorp.com/tutorials/vault/aws-lambda) – Manages secrets and makes them available for developers to use within function code, without making functions Vault aware.
+ [https://docs.honeycomb.io/getting-data-in/integrations/aws/aws-lambda/](https://docs.honeycomb.io/getting-data-in/integrations/aws/aws-lambda/) – Observability tool for debugging your app stack.
+ [https://docs.lumigo.io/docs/lambda-extensions](https://docs.lumigo.io/docs/lambda-extensions) – Profiles Lambda function invocations and collects metrics for troubleshooting issues in serverless and microservice environments.
+ [https://docs.newrelic.com/docs/serverless-function-monitoring/aws-lambda-monitoring/get-started/monitoring-aws-lambda-serverless-monitoring](https://docs.newrelic.com/docs/serverless-function-monitoring/aws-lambda-monitoring/get-started/monitoring-aws-lambda-serverless-monitoring) – Runs alongside Lambda functions, automatically collecting, enhancing, and transporting telemetry to New Relic's unified observability platform.
+ [https://docs.sedai.io/get-started/platform/optimization/aws/lambda](https://docs.sedai.io/get-started/platform/optimization/aws/lambda) – An autonomous cloud management platform, powered by AI/ML, that delivers continuous optimization for cloud operations teams to maximize cloud cost savings, performance, and availability at scale.
+ [https://docs.sentry.io/platforms/javascript/guides/aws-lambda/](https://docs.sentry.io/platforms/javascript/guides/aws-lambda/) – Diagnose, fix, and optimize performance of Lambda functions.
+ [https://www.site24x7.com/help/aws/lambda-execution-logs.html](https://www.site24x7.com/help/aws/lambda-execution-logs.html) – Achieve real-time observability into your Lambda environments
+ [https://github.com/signalfx/splunk-otel-lambda](https://github.com/signalfx/splunk-otel-lambda) – Collects high-resolution, low-latency metrics for efficient and effective monitoring of Lambda functions.
+ [https://help.sumologic.com/03Send-Data/Collect-from-Other-Data-Sources/Collect_AWS_Lambda_Logs_using_an_Extension](https://help.sumologic.com/03Send-Data/Collect-from-Other-Data-Sources/Collect_AWS_Lambda_Logs_using_an_Extension) – Provides visibility into the health and performance of serverless applications.
+ [Salt Security](https://salt.security/press-releases/salt-security-becomes-the-first-and-only-api-security-vendor-to-join-aws-lambda-ready-program?) – Simplifies API posture governance and API security for Lambda functions through automated setup and support for diverse runtimes.

## AWS managed extensions
<a name="aws-managed-extensions"></a>

AWS provides its own managed extensions, including:
+ [AWS AppConfig](https://docs.aws.amazon.com/appconfig/latest/userguide/appconfig-integration-lambda-extensions.html#appconfig-integration-lambda-extensions-enabling) – Use feature flags and dynamic data to update your Lambda functions. You can also use this extension to update other dynamic configuration, such as ops throttling and tuning. 
+ [Amazon CodeGuru Profiler](https://docs.aws.amazon.com/codeguru/latest/profiler-ug/python-lambda-layers.html) – Improves application performance and reduces cost by pinpointing an application's most expensive line of code and providing recommendations for improving code.
+ [CloudWatch Lambda Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Lambda-Insights.html) – Monitor, troubleshoot, and optimize the performance of your Lambda functions through automated dashboards.
+ [AWS Distro for OpenTelemetry (ADOT)](https://aws.amazon.com/otel) – Enables functions to send trace data to AWS monitoring services such as AWS X-Ray, and to destinations that support OpenTelemetry such as Honeycomb and Lightstep.
+ [AWS Parameters and Secrets](with-secrets-manager.md) – Securely retrieve parameters from AWS Systems Manager Parameter Store and secrets from AWS Secrets Manager in Lambda functions.

For additional extensions samples and demo projects, see [AWS Lambda Extensions](https://github.com/aws-samples/aws-lambda-extensions).