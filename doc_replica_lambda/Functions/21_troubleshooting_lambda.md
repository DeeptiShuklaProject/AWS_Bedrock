# Section 21 – Troubleshooting Lambda

<a name="sec-21"></a>

* **Error**: `AccessDeniedException` or `AccessDenied`
  * *Cause*: The function's execution role does not have permission to access the specified resource.
  * *Solution*: Add the required AWS actions (e.g. `s3:GetObject`) to the function's IAM policy.
* **Error**: `Task timed out after 3.00 seconds`
  * *Cause*: The code took longer to execute than the configured timeout limit.
  * *Solution*: Identify network blocks, increase database connection pools, or increase the timeout limit in the configuration settings.
* **Error**: `OutOfMemoryException` or Process Exit
  * *Cause*: Memory consumption exceeded the allocated RAM.
  * *Solution*: Increase the allocated memory in the function configuration.
* **Error**: `ModuleNotFoundError`
  * *Cause*: A third-party library is not included in the deployment package or configured in a Lambda Layer.
  * *Solution*: Verify that package directories are zipped at the root level of your archive.

---
