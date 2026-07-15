# Episode 6 Summary: Output Variables & Sensitive Data Filtering

Learn how to query and surface state data to other configurations (like CI/CD pipelines or dependent workspaces).

## Architectural Guidelines
- **Sensitive Output:** Mark secrets, keys, or passwords with `sensitive = true`. This prevents them from being logged to the console output during `terraform apply`.
- **State File warning:** Note that sensitive variables are still stored as plain text inside the `terraform.tfstate` file. Lock down access to your state backend.
