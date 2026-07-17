# Section 18 – Environment Variables

<a name="sec-18"></a>

Environment variables allow decoupling database URLs, credentials, and configuration flags from your application code.

### Reading Environment Variables
```python
import os

# Retrieve credentials
db_endpoint = os.environ.get('DB_ENDPOINT')
db_password = os.environ.get('DB_PASSWORD')
```

> [!IMPORTANT]
> **Best Practice**: Never commit plaintext API keys or passwords directly as environment variables. For sensitive credentials, store keys in **AWS Secrets Manager** and retrieve them dynamically at runtime.

---
